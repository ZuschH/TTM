"""Read-only SQLite queries shared by the TMM web API and its tests."""

from __future__ import annotations

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
                              printf('0x%04X', v.register_address) AS register_address,
                              v.raw_value, v.value, v.unit
                       FROM latest_values AS v
                       LEFT JOIN latest_poll_cycles AS p
                         ON p.inverter = v.inverter AND p.slave_id = v.slave_id
                       ORDER BY v.inverter, v.metric"""
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
        disk = shutil.disk_usage(self.database.parent)
        observed_seconds = 0.0
        activity_oldest = min(value for value in (oldest, cycle_bounds[0]) if value is not None) if oldest or cycle_bounds[0] else None
        activity_newest = max(value for value in (newest, cycle_bounds[1]) if value is not None) if newest or cycle_bounds[1] else None
        if activity_oldest and activity_newest:
            first = datetime.fromisoformat(activity_oldest.replace("Z", "+00:00"))
            last = datetime.fromisoformat(activity_newest.replace("Z", "+00:00"))
            observed_seconds = max(0.0, (last - first).total_seconds())
        data_bytes = files["database"] + files["wal"]
        growth_bytes_per_second = data_bytes / observed_seconds if observed_seconds >= 300 else None
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
            "growth_bytes_per_second": growth_bytes_per_second,
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

    def export_rows(
        self,
        metric: str | None = None,
        inverter: str | None = None,
        start: str | None = None,
        end: str | None = None,
        limit: int = 250000,
    ):
        clauses = []
        parameters: list[Any] = []
        if metric:
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
                         raw_value, value, unit
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
