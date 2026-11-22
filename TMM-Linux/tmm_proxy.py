"""Deterministic two-port Modbus RTU forwarding and observation for TMM."""

from __future__ import annotations

import logging
import json
import queue
import sqlite3
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

try:
    import serial
except ImportError:  # pragma: no cover - reported at runtime
    serial = None

LOG = logging.getLogger("tmm.proxy")
MIN_SCHEDULED_GAP_SECONDS = 0.005


def adapter_serial(device: str) -> str:
    """Extract the human-manageable USB serial suffix from a by-id path."""
    name = Path(device).name
    marker = "_USB_UART_"
    if marker in name:
        return name.split(marker, 1)[1].split("-if", 1)[0]
    return name or device


def configured_endpoint_status(bridge: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, str]], dict[str, bool]]:
    """Report configured serial endpoints and identify adapters absent from the host."""
    endpoints: list[dict[str, Any]] = []
    for identifier, role in (("hmi", "HMI / upstream"), ("drive", "Inverter / downstream")):
        endpoint = bridge.get(f"{identifier}_port", {})
        if not isinstance(endpoint, dict):
            endpoint = {}
        device = str(endpoint.get("device", ""))
        endpoints.append({
            "id": identifier,
            "role": role,
            "device": device,
            "adapter_serial": adapter_serial(device),
            "present": bool(device) and Path(device).exists(),
            "baudrate": int(endpoint.get("baudrate", 19200)),
            "parity": str(endpoint.get("parity", "E")).upper(),
            "stopbits": int(endpoint.get("stopbits", 1)),
        })
    device_paths = [item["device"] for item in endpoints if item["device"]]
    missing_adapters = [
        {"id": item["id"], "role": item["role"], "device": item["device"]}
        for item in endpoints if item["device"] and not item["present"]
    ]
    checks = {
        "two_endpoints": len(device_paths) == 2,
        "distinct_endpoints": len(set(device_paths)) == 2,
        "stable_device_paths": bool(device_paths) and all(path.startswith("/dev/serial/by-id/") and path.count("/dev/serial/by-id/") == 1 for path in device_paths),
        "devices_present": len(device_paths) == 2 and all(item["present"] for item in endpoints),
    }
    return endpoints, missing_adapters, checks


def crc16(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return crc


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def validate_proxy_config(config: dict[str, Any]) -> dict[str, Any]:
    bridge = config.get("communication_bridge")
    if not isinstance(bridge, dict) or not bridge.get("enabled", False):
        raise ValueError("communication_bridge is not enabled")
    if bridge.get("mode", "transparent_proxy") != "transparent_proxy":
        raise ValueError("communication_bridge.mode must be transparent_proxy")
    endpoints = []
    for name in ("hmi_port", "drive_port"):
        endpoint = bridge.get(name)
        if not isinstance(endpoint, dict):
            raise ValueError(f"communication_bridge.{name} is missing")
        device = str(endpoint.get("device", ""))
        if not device.startswith("/dev/serial/by-id/") or device.count("/dev/serial/by-id/") != 1:
            raise ValueError(f"communication_bridge.{name}.device must use /dev/serial/by-id")
        normalized = dict(endpoint)
        normalized.update(
            device=device,
            baudrate=int(endpoint.get("baudrate", 19200)),
            bytesize=int(endpoint.get("bytesize", 8)),
            parity=str(endpoint.get("parity", "E")).upper(),
            stopbits=float(endpoint.get("stopbits", 1)),
        )
        if normalized["baudrate"] <= 0 or normalized["parity"] not in {"E", "N", "O"}:
            raise ValueError(f"invalid serial format for communication_bridge.{name}")
        endpoints.append(normalized)
    if endpoints[0]["device"] == endpoints[1]["device"]:
        raise ValueError("HMI and drive ports must use different serial adapters")
    result = dict(bridge)
    result["hmi_port"], result["drive_port"] = endpoints
    result["response_timeout_seconds"] = float(bridge.get("response_timeout_seconds", 0.75))
    result["idle_read_timeout_seconds"] = float(bridge.get("idle_read_timeout_seconds", 0.1))
    if result["response_timeout_seconds"] <= 0 or result["idle_read_timeout_seconds"] <= 0:
        raise ValueError("proxy timeouts must be greater than zero")
    scheduled = bridge.get("scheduled_polling", {})
    if scheduled is not None and not isinstance(scheduled, dict):
        raise ValueError("communication_bridge.scheduled_polling must be an object")
    if isinstance(scheduled, dict) and scheduled.get("enabled", False):
        idle_guard = float(scheduled.get("idle_guard_seconds", 0.02))
        poll_timeout = float(scheduled.get("response_timeout_seconds", 0.1))
        minimum_gap = float(scheduled.get("minimum_gap_seconds", 0.02))
        if (idle_guard < MIN_SCHEDULED_GAP_SECONDS or not 0.02 <= poll_timeout <= 0.25
                or minimum_gap < MIN_SCHEDULED_GAP_SECONDS):
            raise ValueError("scheduled proxy polling requires idle guard >= 0.005 s, timeout 0.02..0.25 s, and gap >= 0.005 s")
        # The forwarding loop must wake up before the requested quiet window
        # expires; otherwise sub-100-ms slots would never become observable.
        result["idle_read_timeout_seconds"] = min(
            result["idle_read_timeout_seconds"], idle_guard
        )
    return result


def frame_crc_valid(frame: bytes) -> bool:
    return len(frame) >= 4 and crc16(frame[:-2]) == int.from_bytes(frame[-2:], "little")


def looks_like_modbus_request(frame: bytes) -> bool:
    """Return true only for a complete, CRC-valid Modbus RTU master request."""
    if len(frame) < 4 or frame[0] > 247 or not frame_crc_valid(frame):
        return False
    expected = expected_frame_length(frame, response=False)
    return expected is not None and len(frame) == expected


def expected_frame_length(frame: bytes, *, response: bool) -> int | None:
    if len(frame) < 2: return None
    function = frame[1]
    if response and function & 0x80: return 5
    if response and function in {5, 6, 15, 16}: return 8
    if response and function == 22: return 10
    if response and function in {1, 2, 3, 4, 23}: return 5 + frame[2] if len(frame) >= 3 else None
    if not response and function in {1, 2, 3, 4, 5, 6}: return 8
    if not response and function == 22: return 10
    if not response and function in {15, 16}: return 9 + frame[6] if len(frame) >= 7 else None
    if not response and function == 23: return 13 + frame[10] if len(frame) >= 11 else None
    return None


def _read_exact(port: Any, size: int) -> bytes:
    data = bytearray()
    while len(data) < size:
        chunk = port.read(size - len(data))
        if not chunk:
            break
        data.extend(chunk)
    return bytes(data)


def read_rtu_frame(port: Any, timeout: float, *, response: bool, gap_seconds: float) -> bytes:
    """Read one RTU ADU, using function length where known and silence otherwise."""
    port.timeout = timeout
    prefix = _read_exact(port, 2)
    if len(prefix) < 2:
        return prefix
    function = prefix[1]
    if response and function & 0x80:
        return prefix + _read_exact(port, 3)
    fixed = ({5: 8, 6: 8, 15: 8, 16: 8, 22: 10} if response
             else {1: 8, 2: 8, 3: 8, 4: 8, 5: 8, 6: 8, 22: 10})
    if function in fixed:
        return prefix + _read_exact(port, fixed[function] - 2)
    if response and function in {1, 2, 3, 4, 23}:
        header = _read_exact(port, 1)
        return prefix + header + (_read_exact(port, header[0] + 2) if header else b"")
    if not response and function in {15, 16}:
        header = _read_exact(port, 5)
        return prefix + header + (_read_exact(port, header[4] + 2) if len(header) == 5 else b"")
    if not response and function == 23:
        header = _read_exact(port, 9)
        return prefix + header + (_read_exact(port, header[8] + 2) if len(header) == 9 else b"")
    data = bytearray(prefix)
    port.timeout = gap_seconds
    while True:
        chunk = port.read(256)
        if not chunk:
            break
        data.extend(chunk)
    return bytes(data)


class ProxyLog:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path)
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA synchronous=NORMAL")
        self.connection.executescript("""
            CREATE TABLE IF NOT EXISTS modbus_proxy_transactions (
                id INTEGER PRIMARY KEY, request_at TEXT NOT NULL, response_at TEXT,
                slave_id INTEGER, function_code INTEGER, request_hex TEXT NOT NULL,
                response_hex TEXT, request_crc_valid INTEGER NOT NULL,
                response_crc_valid INTEGER, latency_ms REAL, outcome TEXT NOT NULL,
                origin TEXT NOT NULL DEFAULT 'hmi',
                observed_samples INTEGER NOT NULL DEFAULT 0
            );
            CREATE INDEX IF NOT EXISTS proxy_transactions_time
                ON modbus_proxy_transactions(request_at);
        """)
        columns = {row[1] for row in self.connection.execute("PRAGMA table_info(modbus_proxy_transactions)")}
        if "origin" not in columns:
            self.connection.execute("ALTER TABLE modbus_proxy_transactions ADD COLUMN origin TEXT NOT NULL DEFAULT 'hmi'")
        if "observed_samples" not in columns:
            self.connection.execute("ALTER TABLE modbus_proxy_transactions ADD COLUMN observed_samples INTEGER NOT NULL DEFAULT 0")
        self.connection.commit()

    def store(self, request_at: str, response_at: str | None, request: bytes,
              response: bytes, latency_ms: float | None, outcome: str, origin: str = "hmi",
              observed_samples: int = 0) -> None:
        try:
            self.connection.execute(
            """INSERT INTO modbus_proxy_transactions
               (request_at,response_at,slave_id,function_code,request_hex,response_hex,
                request_crc_valid,response_crc_valid,latency_ms,outcome,origin,observed_samples)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (request_at, response_at, request[0] if request else None,
             request[1] if len(request) > 1 else None, request.hex(" "),
             response.hex(" ") if response else None, int(frame_crc_valid(request)),
             int(frame_crc_valid(response)) if response else None, latency_ms, outcome, origin,
                max(0, int(observed_samples))),
            )
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise

    def close(self) -> None:
        self.connection.close()

    def prune_before(self, cutoff: str, limit: int = 1000) -> int:
        cursor = self.connection.execute(
            """DELETE FROM modbus_proxy_transactions WHERE id IN (
                   SELECT id FROM modbus_proxy_transactions
                   WHERE request_at < ? ORDER BY id LIMIT ?
               )""", (cutoff, max(1, int(limit)))
        )
        self.connection.commit()
        return cursor.rowcount


class ProxyPersistenceWorker:
    """Keep SQLite, decoding, and retention outside the serial forwarding path."""

    def __init__(self, config: dict[str, Any], queue_size: int | None = None):
        self.config = config
        self.retention_days = float(config.get("storage", {}).get("retention_days", 0))
        if queue_size is None:
            queue_size = int(config.get("communication_bridge", {}).get("persistence_queue_size", 65536))
        self.queue: queue.Queue[tuple[str, str | None, bytes, bytes, float | None, str]] = queue.Queue(
            maxsize=max(4096, min(262144, int(queue_size)))
        )
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run, name="tmm-proxy-persistence", daemon=True)
        self.enqueued = 0
        self.processed = 0
        self.dropped = 0
        self.failed = 0
        self.lock_retries = 0
        self.maximum_depth = 0
        self.last_error = ""
        self.last_error_at = ""
        self.last_success_at = ""
        self.thread.start()

    def submit(self, request_at: str, response_at: str | None, request: bytes,
               response: bytes, latency_ms: float | None, outcome: str) -> bool:
        try:
            self.queue.put_nowait((request_at, response_at, request, response, latency_ms, outcome))
        except queue.Full:
            self.dropped += 1
            if self.dropped == 1 or self.dropped % 100 == 0:
                LOG.error("proxy persistence queue full; dropped %d diagnostic transaction(s) without delaying forwarding", self.dropped)
            return False
        self.enqueued += 1
        self.maximum_depth = max(self.maximum_depth, self.queue.qsize())
        return True

    def status(self) -> dict[str, Any]:
        return {
            "queued": self.queue.qsize(), "maximum_depth": self.maximum_depth,
            "capacity": self.queue.maxsize,
            "enqueued": self.enqueued, "processed": self.processed,
            "dropped": self.dropped, "failed": self.failed, "lock_retries": self.lock_retries,
            "last_error": self.last_error, "last_error_at": self.last_error_at,
            "last_success_at": self.last_success_at,
        }

    def _retry_database_lock(self, operation: Callable[[], Any]) -> Any:
        delay = 0.02
        while True:
            try:
                return operation()
            except sqlite3.OperationalError as error:
                if "locked" not in str(error).lower() and "busy" not in str(error).lower():
                    raise
                self.lock_retries += 1
                self.last_error = str(error)
                self.last_error_at = utc_now()
                if self.lock_retries == 1 or self.lock_retries % 100 == 0:
                    LOG.warning("proxy persistence waiting for database maintenance lock (%d retries)", self.lock_retries)
                time.sleep(delay)
                delay = min(0.5, delay * 1.5)

    def close(self) -> None:
        self.stop_event.set()
        self.thread.join(timeout=10.0)
        if self.thread.is_alive():
            LOG.error("proxy persistence worker did not stop within 10 seconds")

    def _run(self) -> None:
        log: ProxyLog | None = None
        observer: ScheduledProxyPoller | None = None
        next_cleanup = time.monotonic() + 3600
        try:
            log = ProxyLog(Path(self.config["storage"]["database"]))
            # HMI priority mode permits passive decoding only.  An old config
            # cannot re-enable injected downstream traffic in this revision.
            observer_config = json.loads(json.dumps(self.config))
            scheduled = observer_config.setdefault("communication_bridge", {}).setdefault("scheduled_polling", {})
            scheduled["enabled"] = False
            scheduled["passive_decode"] = bool(scheduled.get("passive_decode", True))
            observer = ScheduledProxyPoller(observer_config)
            recording_identity = observer.database.recording_identity() if observer.database is not None else None
            next_recording_check = 0.0
            while not self.stop_event.is_set() or not self.queue.empty():
                now = time.monotonic()
                if observer.database is not None and now >= next_recording_check:
                    next_recording_check = now + 0.5
                    current_identity = self._retry_database_lock(observer.database.recording_identity)
                    if current_identity != recording_identity:
                        recording_identity = current_identity
                        observer.database.reset_runtime_state()
                        LOG.info("proxy measurement baseline reset for new recording generation")
                task = None
                try:
                    task = self.queue.get(timeout=0.1)
                except queue.Empty:
                    pass
                if task is not None:
                    request_at, response_at, request, response, latency, outcome = task
                    try:
                        observed = self._retry_database_lock(lambda: observer.observe_hmi_read(
                            request_at, request, response, latency, outcome
                        ))
                        self._retry_database_lock(lambda: log.store(
                            request_at, response_at, request, response, latency, outcome,
                            observed_samples=observed
                        ))
                        self.processed += 1
                        self.last_error = ""
                        self.last_success_at = utc_now()
                    except Exception as error:
                        self.failed += 1
                        self.last_error = str(error)
                        self.last_error_at = utc_now()
                        LOG.error("deferred proxy persistence failed without delaying forwarding: %s", error)
                    finally:
                        self.queue.task_done()
                if self.retention_days > 0 and time.monotonic() >= next_cleanup and self.queue.empty():
                    cutoff = (datetime.now(timezone.utc) - timedelta(days=self.retention_days)).isoformat(timespec="milliseconds")
                    deleted = log.prune_before(cutoff, 1000)
                    if deleted:
                        LOG.info("deferred proxy retention cleanup: deleted %d transaction(s)", deleted)
                        next_cleanup = time.monotonic() + 1.0
                    else:
                        next_cleanup = time.monotonic() + 3600
        except Exception as error:
            self.last_error = str(error)
            LOG.error("proxy persistence worker unavailable; serial forwarding remains active: %s", error)
        finally:
            if observer is not None:
                observer.close()
            if log is not None:
                log.close()


class ModbusProxy:
    def __init__(self, config: dict[str, Any], serial_factory: Callable[..., Any] | None = None):
        self.settings = validate_proxy_config(config)
        if serial_factory is None:
            if serial is None:
                raise RuntimeError("pyserial is not installed")
            serial_factory = serial.Serial
        self.serial_factory = serial_factory
        self.hmi: Any | None = None
        self.drive: Any | None = None
        self.last_request_at: str | None = None
        self.last_upstream_activity = time.monotonic()
        self.upstream_requests_seen = 0
        self.unexpected_drive_bursts = 0
        self.reversed_request_candidates = 0
        self.reversed_candidate_started = 0.0

    @staticmethod
    def _gap(endpoint: dict[str, Any]) -> float:
        parity_bits = 0 if endpoint["parity"] == "N" else 1
        character_bits = 1 + endpoint["bytesize"] + parity_bits + endpoint["stopbits"]
        return max(0.001, 3.5 * character_bits / endpoint["baudrate"])

    def _open(self, endpoint: dict[str, Any]) -> Any:
        return self.serial_factory(
            port=endpoint["device"], baudrate=endpoint["baudrate"],
            bytesize=endpoint["bytesize"], parity=endpoint["parity"],
            stopbits=endpoint["stopbits"], timeout=self.settings["idle_read_timeout_seconds"],
            write_timeout=self.settings["response_timeout_seconds"],
        )

    def open(self) -> None:
        self.close()
        self.hmi = self._open(self.settings["hmi_port"])
        try:
            self.drive = self._open(self.settings["drive_port"])
        except Exception:
            self.hmi.close(); self.hmi = None
            raise
        self.hmi.reset_input_buffer(); self.drive.reset_input_buffer()
        self.last_upstream_activity = time.monotonic()
        self.upstream_requests_seen = 0
        self.unexpected_drive_bursts = 0
        self.reversed_request_candidates = 0
        self.reversed_candidate_started = 0.0
        LOG.info("transparent proxy active: %s <-> %s", self.settings["hmi_port"]["device"], self.settings["drive_port"]["device"])

    def close(self) -> None:
        for name in ("hmi", "drive"):
            port = getattr(self, name)
            if port is not None:
                try: port.close()
                finally: setattr(self, name, None)

    def observe_drive_side_request(self) -> bytes:
        """Detect master requests arriving on the configured slave-side adapter."""
        if self.drive is None or int(getattr(self.drive, "in_waiting", 0) or 0) <= 0:
            return b""
        previous_timeout = self.drive.timeout
        try:
            self.drive.timeout = self._gap(self.settings["drive_port"])
            data = bytearray(self.drive.read(max(1, int(self.drive.in_waiting))))
            while True:
                chunk = self.drive.read(max(1, int(getattr(self.drive, "in_waiting", 0) or 1)))
                if not chunk:
                    break
                data.extend(chunk)
        finally:
            self.drive.timeout = previous_timeout
        frame = bytes(data)
        if len(frame) < 4:
            return b""
        now = time.monotonic()
        if not self.reversed_candidate_started or now - self.reversed_candidate_started > 10.0:
            self.reversed_candidate_started = now
            self.unexpected_drive_bursts = 0
            self.reversed_request_candidates = 0
        self.unexpected_drive_bursts += 1
        if looks_like_modbus_request(frame):
            self.reversed_request_candidates += 1
        return frame

    def reversal_suspected(self) -> bool:
        """Use strict frame evidence first, then repeated wrong-side activity."""
        return self.reversed_request_candidates >= 2 or (
            self.upstream_requests_seen == 0 and self.unexpected_drive_bursts >= 3
        )

    def forward_once(self) -> tuple[bytes, bytes, float | None, str] | None:
        if self.hmi is None or self.drive is None:
            self.open()
        request = read_rtu_frame(
            self.hmi, self.settings["idle_read_timeout_seconds"], response=False,
            gap_seconds=self._gap(self.settings["hmi_port"]),
        )
        if not request:
            return None
        self.last_upstream_activity = time.monotonic()
        self.upstream_requests_seen += 1
        self.last_request_at = utc_now()
        expected = expected_frame_length(request, response=False)
        if len(request) < 4 or (expected is not None and len(request) != expected):
            return request, b"", None, "partial_request"
        if not frame_crc_valid(request):
            return request, b"", None, "request_crc_error"
        request_started = time.monotonic()
        self.drive.write(request); self.drive.flush()
        if request[0] == 0:
            return request, b"", (time.monotonic() - request_started) * 1000, "broadcast"
        response = read_rtu_frame(
            self.drive, self.settings["response_timeout_seconds"], response=True,
            gap_seconds=self._gap(self.settings["drive_port"]),
        )
        latency = (time.monotonic() - request_started) * 1000
        if response:
            self.hmi.write(response); self.hmi.flush()
            outcome = "ok" if frame_crc_valid(request) and frame_crc_valid(response) else "crc_error"
            return request, response, latency, outcome
        return request, b"", latency, "response_timeout"


def _write_runtime_status(path: Path, state: str, error: str = "", wiring: dict[str, Any] | None = None,
                          diagnostics: dict[str, Any] | None = None) -> None:
    """Publish proxy state without allowing diagnostics I/O to stop forwarding."""
    try:
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps({"state": state, "error": error, "updated_at": utc_now(),
                                         "wiring": wiring, "diagnostics": diagnostics}), encoding="utf-8")
        temporary.replace(path)
    except OSError as status_error:
        LOG.warning("could not publish proxy runtime status: %s", status_error)


class ScheduledProxyPoller:
    """Harvest HMI reads and optionally insert a read in a verified idle window."""

    def __init__(self, config: dict[str, Any]):
        bridge = config.get("communication_bridge", {})
        settings = bridge.get("scheduled_polling", {}) if isinstance(bridge, dict) else {}
        if not isinstance(settings, dict):
            settings = {}
        self.enabled = bool(settings.get("enabled", False))
        self.passive_decode = bool(settings.get("passive_decode", True))
        self.idle_guard = max(MIN_SCHEDULED_GAP_SECONDS, float(settings.get("idle_guard_seconds", 0.02)))
        self.response_timeout = min(0.25, max(0.02, float(settings.get("response_timeout_seconds", 0.1))))
        self.minimum_gap = max(MIN_SCHEDULED_GAP_SECONDS, float(settings.get("minimum_gap_seconds", 0.02)))
        self.next_allowed = time.monotonic() + self.idle_guard
        self.entries: list[dict[str, Any]] = []
        self.devices: list[Any] = []
        self.database: Any | None = None
        self.monitor: Any | None = None
        self.successes = 0
        self.errors = 0
        self.passive_transactions = 0
        self.passive_samples = 0
        if not self.enabled and not self.passive_decode:
            return
        try:
            import tmm_monitor as monitor
            self.monitor = monitor
            self.database = monitor.Database(
                Path(config["storage"]["database"]),
                config["storage"].get("change_logging"),
                str(config.get("recording", {}).get("reference", "")).strip(),
                monitor.condition_rules(config),
            )
            intervals_config = config.get("polling", {}).get("intervals", {})
            legacy = float(config.get("polling", {}).get("interval_seconds", 1.0))
            intervals = {
                "fast": float(intervals_config.get("fast", legacy)),
                "normal": float(intervals_config.get("normal", legacy)),
                "diagnostic": float(intervals_config.get("diagnostic", 5.0)),
                "information": float(intervals_config.get("information", 3600.0)),
            }
            self.devices = monitor.configured_devices(config)
            if self.enabled:
                due = time.monotonic() + self.idle_guard
                for device in self.devices:
                    for register in device.registers:
                        self.entries.append({
                            "device": device,
                            "register": register,
                            "interval": max(self.minimum_gap, intervals[register.sampling]),
                            "due": due,
                        })
                        due += self.minimum_gap
        except Exception as exception:
            LOG.error("proxy measurement observer disabled without stopping forwarding: %s", exception)
            self.close()
            self.enabled = False
            self.passive_decode = False
            self.entries = []
            self.devices = []
            self.monitor = None
        LOG.info("proxy measurement observer active: passive HMI decoding %s; scheduled polling %s (%d register(s))",
                 "enabled" if self.passive_decode else "disabled",
                 "enabled" if self.entries else "disabled", len(self.entries))

    def close(self) -> None:
        if self.database is not None:
            self.database.close()
            self.database = None

    def status(self) -> dict[str, Any]:
        return {"enabled": self.enabled, "passive_decode": self.passive_decode,
                "registers": len(self.entries), "successes": self.successes, "errors": self.errors,
                "passive_transactions": self.passive_transactions, "passive_samples": self.passive_samples}

    def observe_hmi_read(self, observed_at: str, request: bytes, response: bytes,
                         latency_ms: float | None, outcome: str) -> int:
        """Store configured registers contained in a valid HMI read response.

        This path never writes to a serial port. Any decoding or SQLite failure is
        deliberately isolated from the transparent forwarding path.
        """
        if (not self.passive_decode or self.monitor is None or self.database is None
                or outcome != "ok" or len(request) != 8 or request[1] not in {3, 4}
                or not frame_crc_valid(request) or not frame_crc_valid(response)):
            return 0
        try:
            slave_id = request[0]
            start = int.from_bytes(request[2:4], "big")
            count = int.from_bytes(request[4:6], "big")
            if not 1 <= count <= 125 or len(response) != 5 + count * 2:
                return 0
            if response[:3] != bytes((slave_id, request[1], count * 2)):
                return 0
            matches = [device for device in self.devices if device.slave_id == slave_id]
            if len(matches) != 1:
                return 0
            device = matches[0]
            values = [int.from_bytes(response[offset:offset + 2], "big")
                      for offset in range(3, 3 + count * 2, 2)]
            samples = [
                (register, values[register.address - start])
                for register in device.registers
                if start <= register.address < start + count
            ]
            if not samples:
                return 0
            samples = self.monitor.add_derived_samples(device, samples)
            stats = self.monitor.PollStats(duration_ms=float(latency_ms or 0), transactions=0)
            self.database.store_cycle(observed_at, device.name, device.slave_id, samples, [], stats)
            self.passive_transactions += 1
            sample_count = sum(1 for register, _ in samples if not register.derived)
            self.passive_samples += sample_count
            return sample_count
        except Exception as exception:
            if isinstance(exception, sqlite3.OperationalError) and (
                "locked" in str(exception).lower() or "busy" in str(exception).lower()
            ):
                raise
            LOG.warning("passive HMI response decoding failed without interrupting forwarding: %s", exception)
            return 0

    def poll_once(self, proxy: ModbusProxy, log: ProxyLog) -> bool:
        if not self.enabled or not self.entries or proxy.hmi is None or proxy.drive is None:
            return False
        now = time.monotonic()
        if now < self.next_allowed or now - proxy.last_upstream_activity < self.idle_guard:
            return False
        if int(getattr(proxy.hmi, "in_waiting", 0) or 0) or int(getattr(proxy.drive, "in_waiting", 0) or 0):
            return False
        entry = min(self.entries, key=lambda item: item["due"])
        if entry["due"] > now:
            return False
        device, register = entry["device"], entry["register"]
        request = self.monitor.read_request(device.slave_id, register.address, 1)
        request_at = utc_now()
        started = time.monotonic()
        response = b""
        error = ""
        previous_timeout = proxy.drive.timeout
        try:
            proxy.drive.timeout = self.response_timeout
            proxy.drive.write(request); proxy.drive.flush()
            response = read_rtu_frame(proxy.drive, self.response_timeout, response=True,
                                      gap_seconds=proxy._gap(proxy.settings["drive_port"]))
            values = self.monitor.parse_read_responses(response, device.slave_id, 1)
            latency = (time.monotonic() - started) * 1000
            stats = self.monitor.PollStats(duration_ms=latency, transactions=1)
            self.database.store_cycle(request_at, device.name, device.slave_id, [(register, values[0])], [], stats)
            self.successes += 1
            outcome = "tmm_poll_ok"
        except Exception as exception:
            latency = (time.monotonic() - started) * 1000
            error = f"{register.key} (0x{register.address:04X}): {exception}"
            stats = self.monitor.PollStats(duration_ms=latency, transactions=1)
            self.database.store_cycle(request_at, device.name, device.slave_id, [], [error], stats)
            self.errors += 1
            outcome = "tmm_poll_timeout" if not response else "tmm_poll_error"
        finally:
            proxy.drive.timeout = previous_timeout
        log.store(request_at, utc_now() if response else None, request, response, latency, outcome, origin="tmm")
        entry["due"] = now + entry["interval"]
        self.next_allowed = time.monotonic() + self.minimum_gap
        if error:
            LOG.warning("scheduled proxy poll failed: %s", error)
        return True


def run_proxy(config: dict[str, Any], stop: Any, once: bool = False) -> int:
    heartbeat = Path("/run/tmm/proxy-active")
    status_path = Path("/run/tmm/proxy-status.json")
    heartbeat.parent.mkdir(parents=True, exist_ok=True)
    try:
        proxy = ModbusProxy(config)
    except (TypeError, ValueError, RuntimeError) as error:
        _write_runtime_status(status_path, "offline", str(error))
        LOG.error("invalid transparent proxy configuration: %s", error)
        if once: return 2
        while not stop.wait(2.0): pass
        return 2
    persistence = ProxyPersistenceWorker(config)
    configured_scheduled = config.get("communication_bridge", {}).get("scheduled_polling", {})
    if isinstance(configured_scheduled, dict) and configured_scheduled.get("enabled", False):
        LOG.warning("scheduled proxy polling suppressed: HMI-priority mode permits passive observation only")
    reconnect_delay = max(0.25, float(config.get("polling", {}).get("reconnect_delay_seconds", 2.0)))
    wiring_diagnostic: dict[str, Any] | None = None
    _write_runtime_status(status_path, "starting")
    try:
        while not stop.is_set():
            try:
                proxy.open()
                heartbeat.touch()
                _write_runtime_status(status_path, "active", wiring=wiring_diagnostic)
                next_heartbeat = time.monotonic() + 1.0
                while not stop.is_set():
                    transaction = proxy.forward_once()
                    if transaction is not None:
                        proxy.last_upstream_activity = time.monotonic()
                    if transaction is None:
                        unexpected = proxy.observe_drive_side_request()
                        if unexpected and proxy.reversal_suspected():
                            evidence = "valid_master_requests" if proxy.reversed_request_candidates >= 2 else "repeated_wrong_side_activity"
                            wiring_diagnostic = {
                                "state": "adapters_swapped_suspected",
                                "observed_on": "drive",
                                "evidence": evidence,
                                "candidate_requests": proxy.reversed_request_candidates,
                                "unexpected_bursts": proxy.unexpected_drive_bursts,
                                "last_frame": unexpected.hex(" "),
                                "updated_at": utc_now(),
                            }
                            LOG.error("serial adapters may be swapped: repeated Modbus master requests received on configured drive port")
                    if time.monotonic() >= next_heartbeat:
                        heartbeat.touch()
                        _write_runtime_status(status_path, "active", wiring=wiring_diagnostic,
                                              diagnostics={"persistence": persistence.status(),
                                                           "scheduled_polling_suppressed": True})
                        next_heartbeat = time.monotonic() + 1.0
                    if transaction is None:
                        if once: return 0
                        continue
                    request, response, latency, outcome = transaction
                    request_at = proxy.last_request_at or utc_now()
                    response_at = utc_now() if response else None
                    persistence.submit(request_at, response_at, request, response, latency, outcome)
                    if outcome not in {"ok", "broadcast"}:
                        LOG.warning("proxy transaction %s: slave=%s function=%s", outcome,
                                    request[0] if request else "?", request[1] if len(request) > 1 else "?")
                    if once: return 0 if response or outcome == "broadcast" else 1
            except Exception as error:
                proxy.close()
                try: heartbeat.unlink()
                except FileNotFoundError: pass
                _write_runtime_status(status_path, "offline", str(error))
                LOG.error("transparent proxy unavailable; retrying in %.2f s: %s", reconnect_delay, error)
                if once: return 2
                stop.wait(reconnect_delay)
    finally:
        proxy.close(); persistence.close()
        try: heartbeat.unlink()
        except FileNotFoundError: pass
        _write_runtime_status(status_path, "stopped")
        LOG.info("transparent proxy stopped")
    return 0
