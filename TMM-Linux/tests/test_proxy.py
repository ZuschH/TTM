import sqlite3
import tempfile
import unittest
from pathlib import Path

from tmm_monitor import crc16
from tmm_proxy import ModbusProxy, ProxyLog, expected_frame_length, frame_crc_valid, validate_proxy_config
from tmm_web_data import MonitorRepository


def with_crc(payload: bytes) -> bytes:
    return payload + crc16(payload).to_bytes(2, "little")


class FakePort:
    def __init__(self, incoming: bytes):
        self.incoming = bytearray(incoming)
        self.written = bytearray()
        self.timeout = 0.1
        self.is_open = True

    def read(self, size: int) -> bytes:
        data = bytes(self.incoming[:size]); del self.incoming[:size]
        return data

    def write(self, data: bytes) -> int:
        self.written.extend(data); return len(data)

    def flush(self): pass
    def reset_input_buffer(self): pass
    def close(self): self.is_open = False


def proxy_config() -> dict:
    return {
        "storage": {"database": "/tmp/not-used.sqlite3"},
        "communication_bridge": {
            "enabled": True, "mode": "transparent_proxy",
            "hmi_port": {"device": "/dev/serial/by-id/usb-hmi", "baudrate": 19200, "parity": "E"},
            "drive_port": {"device": "/dev/serial/by-id/usb-drive", "baudrate": 19200, "parity": "E"},
        },
    }


class ProxyTests(unittest.TestCase):
    def test_request_and_response_are_forwarded_byte_identically(self):
        request = with_crc(bytes.fromhex("01 03 fd 00 00 01"))
        response = with_crc(bytes.fromhex("01 03 02 13 88"))
        ports = {
            "/dev/serial/by-id/usb-hmi": FakePort(request),
            "/dev/serial/by-id/usb-drive": FakePort(response),
        }
        proxy = ModbusProxy(proxy_config(), lambda **settings: ports[settings["port"]])
        proxy.open()
        received_request, received_response, latency, outcome = proxy.forward_once()
        self.assertEqual(received_request, request)
        self.assertEqual(received_response, response)
        self.assertEqual(bytes(ports["/dev/serial/by-id/usb-drive"].written), request)
        self.assertEqual(bytes(ports["/dev/serial/by-id/usb-hmi"].written), response)
        self.assertGreaterEqual(latency, 0)
        self.assertEqual(outcome, "ok")

    def test_invalid_crc_is_forwarded_but_marked(self):
        self.assertFalse(frame_crc_valid(bytes.fromhex("01 03 00 00")))

    def test_partial_known_request_is_not_sent_to_drive(self):
        partial = bytes.fromhex("01 03 fd 00")
        ports = {
            "/dev/serial/by-id/usb-hmi": FakePort(partial),
            "/dev/serial/by-id/usb-drive": FakePort(b""),
        }
        proxy = ModbusProxy(proxy_config(), lambda **settings: ports[settings["port"]])
        proxy.open()
        request, response, latency, outcome = proxy.forward_once()
        self.assertEqual(request, partial)
        self.assertEqual(response, b"")
        self.assertIsNone(latency)
        self.assertEqual(outcome, "partial_request")
        self.assertEqual(ports["/dev/serial/by-id/usb-drive"].written, b"")

    def test_variable_write_request_length_is_recognized(self):
        frame = bytes.fromhex("01 10 00 10 00 02 04 00 01 00 02 00 00")
        self.assertEqual(expected_frame_length(frame, response=False), 13)

    def test_proxy_requires_two_distinct_stable_devices(self):
        config = proxy_config()
        config["communication_bridge"]["drive_port"]["device"] = "/dev/ttyUSB1"
        with self.assertRaisesRegex(ValueError, "/dev/serial/by-id"):
            validate_proxy_config(config)
        config = proxy_config()
        config["communication_bridge"]["hmi_port"]["device"] = "/dev/serial/by-id/usb-hmi/dev/serial/by-id/usb-hmi"
        with self.assertRaisesRegex(ValueError, "/dev/serial/by-id"):
            validate_proxy_config(config)

    def test_proxy_transaction_is_persisted(self):
        request = with_crc(bytes.fromhex("01 06 00 01 00 02"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "measurements.sqlite3"
            log = ProxyLog(path)
            log.store("2026-10-13T10:00:00+00:00", "2026-10-13T10:00:00.010+00:00",
                      request, request, 10.0, "ok")
            log.close()
            row = sqlite3.connect(path).execute(
                "SELECT slave_id,function_code,request_crc_valid,response_crc_valid,outcome FROM modbus_proxy_transactions"
            ).fetchone()
        self.assertEqual(row, (1, 6, 1, 1, "ok"))

    def test_proxy_diagnostics_do_not_include_historical_poll_failures(self):
        request = with_crc(bytes.fromhex("01 03 fd 00 00 01"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "measurements.sqlite3"
            log = ProxyLog(path)
            from datetime import datetime, timezone
            observed = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
            log.store(observed, observed, request, with_crc(bytes.fromhex("01 03 02 13 88")), 8.5, "ok")
            log.close()
            diagnostics = MonitorRepository(path).proxy_diagnostics(60)
        self.assertEqual(diagnostics["transactions"], 1)
        self.assertEqual(diagnostics["forwarded"], 1)
        self.assertEqual(diagnostics["errors"], 0)
        self.assertEqual(diagnostics["average_latency_ms"], 8.5)

    def test_proxy_diagnostics_report_passively_adopted_measurements(self):
        request = with_crc(bytes.fromhex("01 03 fd 00 00 02"))
        response = with_crc(bytes.fromhex("01 03 04 13 88 00 01"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "measurements.sqlite3"
            log = ProxyLog(path)
            from datetime import datetime, timezone
            observed = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
            log.store(observed, observed, request, response, 8.5, "ok", observed_samples=2)
            log.close()
            diagnostics = MonitorRepository(path).proxy_diagnostics(60)
        self.assertEqual(diagnostics["passive_transactions"], 1)
        self.assertEqual(diagnostics["passive_samples"], 2)


if __name__ == "__main__":
    unittest.main()
