"""Read-only SQLite queries shared by the TMM web API and its tests."""

from __future__ import annotations

import json
import sqlite3
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote


class MonitorRepository:
    def __init__(self, database: Path):
        self.database = database

    def _connect(self) -> sqlite3.Connection:
        if not self.database.is_file():
            raise FileNotFoundError(self.database)
        uri = f"file:{quote(str(self.database))}?mode=ro"
        # Starlette advances synchronous StreamingResponse iterators in its worker
        # pool. Consecutive chunks may therefore run on different threads. This
        # connection is read-only and each iterator is advanced sequentially, so
        # allowing that hand-off is safe and prevents truncated CSV downloads.
        connection = sqlite3.connect(uri, uri=True, timeout=2.0, check_same_thread=False)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA query_only=ON")
        connection.execute("PRAGMA busy_timeout=2000")
        return connection

    @staticmethod
    def _rows(cursor: sqlite3.Cursor) -> list[dict[str, Any]]:
        return [dict(row) for row in cursor.fetchall()]

    def last_cycle(self) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                """SELECT id, observed_at, inverter, slave_id, successful_reads,
                          failed_reads, error
                   FROM poll_cycles ORDER BY id DESC LIMIT 1"""
            ).fetchone()
            return dict(row) if row else None

    def last_cycles(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            return self._rows(
                connection.execute(
                    """SELECT cycle_id AS id, observed_at, inverter, slave_id,
                              successful_reads, failed_reads, error
                       FROM latest_poll_cycles ORDER BY inverter"""
                )
            )

    def latest_samples(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            return self._rows(
                connection.execute(
                    """SELECT COALESCE(p.observed_at, v.observed_at) AS observed_at,
                              v.inverter, v.slave_id, v.metric,
                              v.metric_label,
                              printf('0x%04X', v.register_address) AS register_address,
                              v.raw_value, v.value, v.unit
                       FROM latest_values AS v
                       LEFT JOIN latest_poll_cycles AS p
                         ON p.inverter = v.inverter AND p.slave_id = v.slave_id
                       ORDER BY v.inverter, v.metric"""
                )
            )

    def recorded_metrics(self) -> list[dict[str, Any]]:
        """Return one selector entry for every metric retained in this recording.

        This deliberately queries ``samples`` rather than ``latest_values``:
        an offline inverter has no fresh latest value, but its recorded trends
        must remain accessible in the dashboard.
        """
        with self._connect() as connection:
            return self._rows(
                connection.execute(
                    """SELECT inverter, slave_id, metric, metric_label, unit,
                              MIN(value) AS minimum_value, MAX(value) AS maximum_value,
                              MAX(observed_at) AS observed_at
                       FROM samples
                       GROUP BY inverter, slave_id, metric, metric_label, unit
                       ORDER BY inverter, metric_label, metric"""
                )
            )

    def history(
        self,
        metric: str,
        inverter: str | None = None,
        start: str | None = None,
        end: str | None = None,
        limit: int = 1000,
    ) -> list[dict[str, Any]]:
        clauses = ["metric = ?"]
        parameters: list[Any] = [metric]
        if inverter:
            clauses.append("inverter = ?")
            parameters.append(inverter)
        if start:
            clauses.append("observed_at >= ?")
            parameters.append(start)
        if end:
            clauses.append("observed_at <= ?")
            parameters.append(end)
        parameters.append(limit)
        sql = f"""SELECT observed_at, metric, raw_value, value, unit
                  FROM samples WHERE {' AND '.join(clauses)}
                  ORDER BY id DESC LIMIT ?"""
        with self._connect() as connection:
            rows = self._rows(connection.execute(sql, parameters))
        rows.reverse()
        return rows

    def recent_history(self, metric: str, inverter: str, limit: int = 3600) -> list[dict[str, Any]]:
        """Recent ordered values for local engineering estimates."""
        with self._connect() as connection:
            rows = self._rows(connection.execute(
                """SELECT observed_at, value FROM samples
                   WHERE metric = ? AND inverter = ? ORDER BY id DESC LIMIT ?""",
                (metric, inverter, limit),
            ))
        rows.reverse()
        return rows

    def poll_cycles(self, limit: int = 100) -> list[dict[str, Any]]:
        with self._connect() as connection:
            return self._rows(
                connection.execute(
                    """SELECT id, observed_at, inverter, slave_id, successful_reads,
                              failed_reads, error, duration_ms, transactions, retries,
                              estimated_bus_ms
                       FROM poll_cycles ORDER BY id DESC LIMIT ?""",
                    (limit,),
                )
            )

    def communication_diagnostics(self, window_seconds: int = 60) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        cutoff = (now - timedelta(seconds=window_seconds)).isoformat(timespec="milliseconds")
        with self._connect() as connection:
            row = connection.execute(
                """SELECT COALESCE(SUM(cycles), 0) AS cycles, MIN(minute) AS oldest_observed_at,
                          COALESCE(SUM(samples), 0) AS samples,
                          COALESCE(SUM(failed_reads), 0) AS failed_reads,
                          COALESCE(SUM(transactions), 0) AS transactions,
                          COALESCE(SUM(retries), 0) AS retries,
                          COALESCE(SUM(total_duration_ms) / NULLIF(SUM(cycles), 0), 0) AS average_cycle_ms,
                          COALESCE(MAX(maximum_duration_ms), 0) AS maximum_cycle_ms,
                          COALESCE(SUM(estimated_bus_ms), 0) AS estimated_bus_ms
                   FROM diagnostic_minutes WHERE minute >= ?""",
                (cutoff[:19],),
            ).fetchone()
        data = dict(row)
        data["window_seconds"] = window_seconds
        oldest = data.pop("oldest_observed_at")
        elapsed = min(window_seconds, max(1.0, (now - datetime.fromisoformat(f"{oldest}+00:00")).total_seconds())) if oldest else window_seconds
        data["observed_window_seconds"] = elapsed
        data["samples_per_second"] = data["samples"] / elapsed
        data["bus_utilization_percent"] = min(100.0, data["estimated_bus_ms"] / (elapsed * 10.0))
        data["success_percent"] = (
            100.0 * data["samples"] / (data["samples"] + data["failed_reads"])
            if data["samples"] + data["failed_reads"] else 0.0
        )
        return data

    def proxy_diagnostics(self, window_seconds: int = 60) -> dict[str, Any]:
        """Summarize only traffic produced by the transparent proxy."""
        now = datetime.now(timezone.utc)
        cutoff = (now - timedelta(seconds=window_seconds)).isoformat(timespec="milliseconds")
        with self._connect() as connection:
            exists = connection.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='modbus_proxy_transactions'"
            ).fetchone()
            if not exists:
                return {"window_seconds": window_seconds, "transactions": 0, "forwarded": 0,
                        "errors": 0, "crc_errors": 0, "timeouts": 0, "partial_requests": 0,
                        "passive_samples": 0, "passive_transactions": 0,
                        "tmm_poll_transactions": 0, "tmm_poll_successes": 0, "tmm_poll_errors": 0,
                        "transactions_per_second": 0.0, "average_latency_ms": 0.0,
                        "maximum_latency_ms": 0.0, "last_transaction_at": None,
                        "last_outcome": None, "age_seconds": None}
            columns = {item[1] for item in connection.execute(
                "PRAGMA table_info(modbus_proxy_transactions)"
            )}
            passive_samples = "observed_samples" if "observed_samples" in columns else "0"
            row = connection.execute(
                f"""SELECT SUM(CASE WHEN origin='hmi' THEN 1 ELSE 0 END) AS transactions,
                          SUM(CASE WHEN origin='hmi' AND outcome IN ('ok','broadcast') THEN 1 ELSE 0 END) AS forwarded,
                          SUM(CASE WHEN origin='hmi' AND outcome NOT IN ('ok','broadcast') THEN 1 ELSE 0 END) AS errors,
                          SUM(CASE WHEN origin='hmi' AND outcome IN ('crc_error','request_crc_error') THEN 1 ELSE 0 END) AS crc_errors,
                          SUM(CASE WHEN origin='hmi' AND outcome='response_timeout' THEN 1 ELSE 0 END) AS timeouts,
                          SUM(CASE WHEN origin='hmi' AND outcome='partial_request' THEN 1 ELSE 0 END) AS partial_requests,
                          COALESCE(SUM(CASE WHEN origin='hmi' THEN {passive_samples} ELSE 0 END),0) AS passive_samples,
                          SUM(CASE WHEN origin='hmi' AND {passive_samples} > 0 THEN 1 ELSE 0 END) AS passive_transactions,
                          COALESCE(AVG(CASE WHEN origin='hmi' THEN latency_ms END),0) AS average_latency_ms,
                          COALESCE(MAX(CASE WHEN origin='hmi' THEN latency_ms END),0) AS maximum_latency_ms,
                          SUM(CASE WHEN origin='tmm' THEN 1 ELSE 0 END) AS tmm_poll_transactions,
                          SUM(CASE WHEN origin='tmm' AND outcome='tmm_poll_ok' THEN 1 ELSE 0 END) AS tmm_poll_successes,
                          SUM(CASE WHEN origin='tmm' AND outcome!='tmm_poll_ok' THEN 1 ELSE 0 END) AS tmm_poll_errors
                   FROM modbus_proxy_transactions WHERE request_at >= ?""", (cutoff,)
            ).fetchone()
            latest = connection.execute(
                "SELECT request_at,outcome FROM modbus_proxy_transactions WHERE origin='hmi' ORDER BY id DESC LIMIT 1"
            ).fetchone()
        data = {key: (value or 0) for key, value in dict(row).items()}
        data["window_seconds"] = window_seconds
        data["transactions_per_second"] = float(data["transactions"]) / window_seconds
        data["last_transaction_at"] = latest["request_at"] if latest else None
        data["last_outcome"] = latest["outcome"] if latest else None
        data["age_seconds"] = max(0.0, (now - datetime.fromisoformat(latest["request_at"].replace("Z", "+00:00"))).total_seconds()) if latest else None
        return data

    def proxy_transactions(self, limit: int = 50) -> list[dict[str, Any]]:
        """Return recent raw proxy exchanges for the RTU evidence logbook."""
        with self._connect() as connection:
            exists = connection.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='modbus_proxy_transactions'"
            ).fetchone()
            if not exists:
                return []
            columns = {item[1] for item in connection.execute(
                "PRAGMA table_info(modbus_proxy_transactions)"
            )}
            passive_samples = "observed_samples" if "observed_samples" in columns else "0 AS observed_samples"
            return self._rows(connection.execute(
                f"""SELECT id,request_at,response_at,request_hex,response_hex,
                          request_crc_valid,response_crc_valid,latency_ms,outcome,origin,{passive_samples}
                   FROM modbus_proxy_transactions ORDER BY id DESC LIMIT ?""",
                (limit,),
            ))

    def communication_history(self, metric: str, limit: int = 1000) -> list[dict[str, Any]]:
        """Return compact per-minute communication quality trends."""
        with self._connect() as connection:
            rows = self._rows(connection.execute(
                """SELECT minute AS observed_at, SUM(cycles) AS cycles, SUM(samples) AS samples,
                          SUM(failed_reads) AS failed_reads, SUM(retries) AS retries,
                          SUM(total_duration_ms) AS total_duration_ms,
                          MAX(maximum_duration_ms) AS maximum_duration_ms,
                          SUM(estimated_bus_ms) AS estimated_bus_ms
                   FROM diagnostic_minutes GROUP BY minute ORDER BY minute DESC LIMIT ?""",
                (limit,),
            ))
        rows.reverse()
        result: list[dict[str, Any]] = []
        for row in rows:
            cycles = max(1, int(row["cycles"])); samples = float(row["samples"]); failed = float(row["failed_reads"])
            values = {
                "communication.samples_per_second": (samples / 60.0, "samples/s"),
                "communication.average_cycle_ms": (float(row["total_duration_ms"]) / cycles, "ms"),
                "communication.maximum_cycle_ms": (float(row["maximum_duration_ms"]), "ms"),
                "communication.bus_utilization_percent": (min(100.0, float(row["estimated_bus_ms"]) / 600.0), "%"),
                "communication.retries": (float(row["retries"]), "count"),
                "communication.success_percent": (100.0 * samples / (samples + failed) if samples + failed else 0.0, "%"),
            }
            if metric in values:
                value, unit = values[metric]
                result.append({"observed_at": f"{row['observed_at']}+00:00", "metric": metric, "raw_value": round(value * 1_000_000), "value": value, "unit": unit})
        return result

    def metrics(self) -> list[str]:
        with self._connect() as connection:
            return [
                row[0]
                for row in connection.execute(
                    "SELECT DISTINCT metric FROM latest_values ORDER BY metric"
                ).fetchall()
            ]

    def inverters(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            return self._rows(
                connection.execute(
                    """SELECT inverter AS name, slave_id, MAX(observed_at) AS last_seen
                       FROM poll_cycles GROUP BY inverter, slave_id ORDER BY inverter"""
                )
            )

    def storage_info(self) -> dict[str, Any]:
        files = {}
        total = 0
        for label, path in (
            ("database", self.database),
            ("wal", Path(f"{self.database}-wal")),
            ("shared_memory", Path(f"{self.database}-shm")),
        ):
            size = path.stat().st_size if path.exists() else 0
            files[label] = size
            total += size
        with self._connect() as connection:
            stats = connection.execute(
                "SELECT sample_count, cycle_count, oldest_sample, newest_sample FROM storage_stats WHERE singleton=1"
            ).fetchone()
            sample_count, cycle_count, oldest, newest = stats
            cycle_bounds = connection.execute("SELECT MIN(observed_at), MAX(observed_at) FROM poll_cycles").fetchone()
            recording = connection.execute(
                "SELECT created_at FROM recording_info WHERE singleton=1"
            ).fetchone()
            recording_created_at = str(recording[0]) if recording else ""
            try:
                growth_samples = connection.execute(
                    """SELECT observed_at,
                              COALESCE(used_bytes,database_bytes) AS used_bytes,
                              COALESCE(allocated_bytes,database_bytes) AS allocated_bytes,
                              COALESCE(reusable_bytes,0) AS reusable_bytes
                       FROM storage_growth_samples
                       WHERE observed_at >= ? ORDER BY observed_at DESC LIMIT 1441""",
                    (recording_created_at,),
                ).fetchall()
            except sqlite3.OperationalError:
                growth_samples = []
        disk = shutil.disk_usage(self.database.parent)
        observed_seconds = 0.0
        activity_oldest = min(value for value in (oldest, cycle_bounds[0]) if value is not None) if oldest or cycle_bounds[0] else None
        activity_newest = max(value for value in (newest, cycle_bounds[1]) if value is not None) if newest or cycle_bounds[1] else None
        if activity_oldest and activity_newest:
            first = datetime.fromisoformat(activity_oldest.replace("Z", "+00:00"))
            last = datetime.fromisoformat(activity_newest.replace("Z", "+00:00"))
            observed_seconds = max(0.0, (last - first).total_seconds())
        growth_bytes_per_second = None
        growth_observed_seconds = 0.0
        if len(growth_samples) >= 2:
            latest = growth_samples[0]
            earliest = growth_samples[-1]
            first_time = datetime.fromisoformat(earliest["observed_at"].replace("Z", "+00:00"))
            last_time = datetime.fromisoformat(latest["observed_at"].replace("Z", "+00:00"))
            growth_observed_seconds = max(0.0, (last_time - first_time).total_seconds())
            if growth_observed_seconds >= 300:
                used_growth = max(0, int(latest["used_bytes"]) - int(earliest["used_bytes"]))
                growth_bytes_per_second = used_growth / growth_observed_seconds
        latest_reusable_bytes = int(growth_samples[0]["reusable_bytes"]) if growth_samples else 0
        return {
            "bytes": total,
            "files": files,
            "sample_count": sample_count,
            "cycle_count": cycle_count,
            "oldest_sample": oldest,
            "newest_sample": newest,
            "filesystem_total_bytes": disk.total,
            "filesystem_free_bytes": disk.free,
            "observed_seconds": observed_seconds,
            "growth_observed_seconds": growth_observed_seconds,
            "growth_bytes_per_second": growth_bytes_per_second,
            "sqlite_reusable_bytes": latest_reusable_bytes,
        }

    def recording_info(self) -> dict[str, Any]:
        with self._connect() as connection:
            try:
                row = connection.execute(
                    "SELECT reference, created_at FROM recording_info WHERE singleton = 1"
                ).fetchone()
            except sqlite3.OperationalError:
                row = None
        return dict(row) if row else {"reference": "", "created_at": None}

    def thermal_protection(self) -> dict[str, Any]:
        with self._connect() as connection:
            try:
                row = connection.execute(
                    "SELECT observed_at,state,temperature_celsius,interval_factor FROM thermal_protection WHERE singleton=1"
                ).fetchone()
            except sqlite3.OperationalError:
                row = None
        return dict(row) if row else {"state": "normal", "interval_factor": 1, "temperature_celsius": None, "observed_at": None}

    def thermal_events(self, limit: int = 250000) -> list[dict[str, Any]]:
        with self._connect() as connection:
            try:
                return self._rows(connection.execute(
                    "SELECT observed_at,state,temperature_celsius,interval_factor,detail FROM thermal_events ORDER BY id ASC LIMIT ?",
                    (limit,),
                ))
            except sqlite3.OperationalError:
                return []

    def milestones(self, start: str | None = None, end: str | None = None, limit: int = 1000) -> list[dict[str, Any]]:
        clauses: list[str] = []; parameters: list[Any] = []
        if start:
            clauses.append("observed_at >= ?"); parameters.append(start)
        if end:
            clauses.append("observed_at <= ?"); parameters.append(end)
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        parameters.append(limit)
        with self._connect() as connection:
            try:
                rows = self._rows(connection.execute(
                    f"""SELECT id,observed_at,rule_id,rule_revision,rule_name,event_type,severity,
                        source,metric,value,unit,operator,target_value,snapshot_json
                        FROM milestones {where} ORDER BY id DESC LIMIT ?""", parameters
                ))
            except sqlite3.OperationalError:
                return []
        rows.reverse()
        for row in rows:
            try: row["snapshot"] = json.loads(row.pop("snapshot_json"))
            except (json.JSONDecodeError, TypeError): row["snapshot"] = {}
        return rows

    def condition_states(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            try:
                return self._rows(connection.execute(
                    "SELECT rule_id,active,pending_since,last_value,last_observed_at FROM condition_states ORDER BY rule_id"
                ))
            except sqlite3.OperationalError:
                return []

    def export_rows(
        self,
        metric: str | None = None,
        metrics: list[str] | None = None,
        inverter: str | None = None,
        start: str | None = None,
        end: str | None = None,
        limit: int = 250000,
    ):
        clauses = []
        parameters: list[Any] = []
        if metrics:
            clauses.append(f"metric IN ({','.join('?' for _ in metrics)})")
            parameters.extend(metrics)
        elif metric:
            clauses.append("metric = ?")
            parameters.append(metric)
        if inverter:
            clauses.append("inverter = ?")
            parameters.append(inverter)
        if start:
            clauses.append("observed_at >= ?")
            parameters.append(start)
        if end:
            clauses.append("observed_at <= ?")
            parameters.append(end)
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        parameters.append(limit)
        sql = f"""SELECT observed_at, inverter, slave_id, metric,
                         printf('0x%04X', register_address) AS register_address,
                         raw_value, value, unit, metric_label
                  FROM samples {where} ORDER BY id ASC LIMIT ?"""
        connection = self._connect()
        try:
            cursor = connection.execute(sql, parameters)
            while True:
                rows = cursor.fetchmany(1000)
                if not rows:
                    break
                for row in rows:
                    yield tuple(row)
        finally:
            connection.close()
