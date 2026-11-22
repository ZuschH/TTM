#!/usr/bin/env python3
"""Read-only Toshiba Modbus Monitor (TMM) RTU collector."""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import signal
import sqlite3
import threading
import time
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

from tmm_decode import terminal_signal_bits
from tmm_conditions import ConditionEvaluator, condition_rules
from tmm_profiles import profile
from tmm_addons import SequentAddon, configured_addons

try:
    import serial
except ImportError:  # Allows protocol/database tests without the runtime dependency.
    serial = None  # type: ignore[assignment]


# Vendor drivers open the same /dev/i2c-1 device independently.  The kernel
# serialises individual ioctl calls, but a complete card read often consists of
# several register operations and is not transactional.  One shared lock keeps
# stacked Sequent cards from interleaving such sequences under high-rate input
# sampling.
ADDON_I2C_LOCK = threading.Lock()

LOG = logging.getLogger("tmm")

DEFAULT_CHANGE_THRESHOLDS = {
    "output_frequency": 0.05,
    "frequency_setpoint": 0.05,
    "output_current": 0.1,
    "dc_input_voltage": 0.1,
    "output_voltage": 0.1,
    "braking_resistor_load": 1.0,
    "fm_analog_output": 0.5,
    "inverter_internal_temperature": 1.0,
    "power_board_temperature": 1.0,
    "speed_feedback": 0.05,
    "speed_feedback_filtered": 0.05,
    "torque": 0.1,
    "torque_command": 0.1,
    "torque_current": 0.1,
    "exciting_current": 0.1,
    "motor_overload_factor": 0.1,
    "inverter_overload_factor": 0.1,
    "motor_load_factor": 1.0,
    "inverter_load_factor": 1.0,
    "input_power": 0.01,
    "output_power": 0.01,
    "calculated_motor_speed": 1.0,
    "machine_speed": 1.0,
    "actual_output_current": 0.1,
    "actual_output_voltage": 1.0,
    "actual_motor_torque": 0.1,
    "mechanical_power": 0.01,
}

# These values drive the persistent safety indicator in the web dashboard.
# They remain polled even if their ordinary measurement channel is Off: an
# operator must never lose a warning simply to reduce the visible channel set.
# They are kept out of history unless the channel is explicitly set to Record.
ALWAYS_MONITORED_ALERT_METRICS = {
    "operating_status", "trip_code", "alarm_information_1", "alarm_information_2",
    "output_current", "dc_input_voltage", "braking_resistor_load",
    "inverter_internal_temperature", "power_board_temperature",
}

MODBUS_UNREADABLE_VF_AS1 = {
    0x0257, 0x0258, 0x0436, 0x0437, 0x0457, 0x0459,
    0x0480, 0x0481, 0x0482, 0x0483, 0x0484, 0x0485, 0x0486,
    0x0487, 0x0488, 0x0493, 0x0497, 0x0642, 0x0666, 0x0667,
    0x0668, 0xFB35, 0xFB44, 0xFB47, 0xFB55, 0xFB56, 0xFC15,
    0xFC17, 0xFC18, 0xFC46, 0xFC49, 0xFC50, 0xFC51, 0xFC52,
    0xFC89, 0xFF07, 0xFF48, 0xFF49, 0xFF50, 0xFF51, 0xFF58,
}
PCM_SPECIAL_VF_AS1 = set(range(0x0792, 0x07A0))


def parameter_safety_class(address: int, pcm_flag: int, model: str) -> str:
    if model == "VF-AS1" and address in MODBUS_UNREADABLE_VF_AS1:
        return "unsupported"
    if address >= 0xFA00:
        return "monitor"
    if 0x0800 <= address <= 0x0808:
        return "communication"
    if model == "VF-AS1" and address in PCM_SPECIAL_VF_AS1:
        return "special"
    if pcm_flag == 0:
        return "special"
    return "candidate"


class ProtocolError(Exception):
    """A malformed, incomplete, or Modbus exception response."""


class ModbusException(ProtocolError):
    """A valid Modbus exception response returned by the inverter."""


class PortRecoveryRequired(RuntimeError):
    """Ask the Windows Service supervisor for a clean process restart."""


def crc16(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return crc


def read_request(slave_id: int, address: int, count: int = 1) -> bytes:
    if not 1 <= slave_id <= 247:
        raise ValueError("slave_id must be between 1 and 247")
    if not 0 <= address <= 0xFFFF:
        raise ValueError("register address must fit in 16 bits")
    if not 1 <= count <= 125:
        raise ValueError("register count must be between 1 and 125")
    payload = bytes((slave_id, 0x03)) + address.to_bytes(2, "big") + count.to_bytes(2, "big")
    return payload + crc16(payload).to_bytes(2, "little")


def write_request(slave_id: int, address: int, value: int) -> bytes:
    if not 1 <= slave_id <= 247 or not 0 <= address <= 0xFFFF or not 0 <= value <= 0xFFFF:
        raise ValueError("invalid Modbus word-write request")
    payload = bytes((slave_id, 0x06)) + address.to_bytes(2, "big") + value.to_bytes(2, "big")
    return payload + crc16(payload).to_bytes(2, "little")


def parse_write_response(response: bytes, slave_id: int, address: int, value: int) -> None:
    if len(response) == 5 and response[0] == slave_id and response[1] == 0x86:
        if crc16(response[:-2]) != int.from_bytes(response[-2:], "little"):
            raise ProtocolError("CRC error in Modbus write exception response")
        raise ModbusException(f"Modbus exception 0x{response[2]:02X}")
    expected = bytes((slave_id, 0x06)) + address.to_bytes(2, "big") + value.to_bytes(2, "big")
    if len(response) != 8 or response[:-2] != expected or crc16(response[:-2]) != int.from_bytes(response[-2:], "little"):
        raise ProtocolError("unexpected Modbus write response")


def parse_read_response(response: bytes, slave_id: int) -> int:
    if len(response) == 5 and response[0] == slave_id and response[1] == 0x83:
        if crc16(response[:-2]) != int.from_bytes(response[-2:], "little"):
            raise ProtocolError("CRC error in Modbus exception response")
        raise ModbusException(f"Modbus exception 0x{response[2]:02X}")
    if len(response) != 7:
        raise ProtocolError(f"expected 7 response bytes, received {len(response)}")
    if crc16(response[:-2]) != int.from_bytes(response[-2:], "little"):
        raise ProtocolError("CRC error")
    if response[:3] != bytes((slave_id, 0x03, 0x02)):
        raise ProtocolError(f"unexpected response header {response[:3].hex(' ')}")
    return int.from_bytes(response[3:5], "big")


def parse_read_responses(response: bytes, slave_id: int, count: int) -> list[int]:
    if len(response) == 5 and response[0] == slave_id and response[1] == 0x83:
        parse_read_response(response, slave_id)
    expected = 5 + count * 2
    if len(response) != expected:
        raise ProtocolError(f"expected {expected} response bytes, received {len(response)}")
    if crc16(response[:-2]) != int.from_bytes(response[-2:], "little"):
        raise ProtocolError("CRC error")
    if response[:3] != bytes((slave_id, 0x03, count * 2)):
        raise ProtocolError(f"unexpected response header {response[:3].hex(' ')}")
    return [int.from_bytes(response[3 + offset:5 + offset], "big") for offset in range(0, count * 2, 2)]


@dataclass(frozen=True)
class Register:
    key: str
    address: int
    scale: float
    unit: str
    sampling: str = "normal"
    derived: bool = False
    record_history: bool = True
    label: str = ""


COMMUNICATION_REGISTER = Register("communication_status", 0xFFFF, 1, "raw", "fast")


@dataclass(frozen=True)
class Device:
    name: str
    model: str
    slave_id: int
    registers: list[Register]
    decoder: str | None = None
    max_read_words: int = 1
    machine_speed_factor: float | None = None
    machine_speed_unit: str = "rpm"
    rated_output_current_a: float | None = None
    rated_output_voltage_v: float | None = None
    motor_rated_power_kw: float | None = None
    motor_rated_speed_rpm: float | None = None
    bus_id: str = "default"


@dataclass
class PollStats:
    duration_ms: float = 0.0
    transactions: int = 0
    retries: int = 0
    estimated_bus_ms: float = 0.0


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    required = ("polling", "storage")
    missing = [key for key in required if key not in config]
    if "serial" not in config and "serial_buses" not in config:
        missing.append("serial or serial_buses")
    if missing:
        raise ValueError(f"missing configuration keys: {', '.join(missing)}")
    if "inverters" not in config and ("inverter" not in config or "registers" not in config):
        raise ValueError("configure either 'inverters' or legacy 'inverter' plus 'registers'")
    configured_addons(config)
    configured_serial_buses(config)
    return config


def configured_serial_buses(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Normalize legacy one-port and new named multi-port configurations."""
    raw = config.get("serial_buses")
    named_buses = raw is not None
    if raw is None:
        raw = [{"id": "default", **config.get("serial", {"device": "/dev/serial/by-id/unconfigured"})}]
    if not isinstance(raw, list) or not raw:
        raise ValueError("serial_buses must contain at least one bus")
    result: dict[str, dict[str, Any]] = {}
    devices: set[str] = set()
    for item in raw:
        if not isinstance(item, dict):
            raise ValueError("every serial bus must be an object")
        identifier = str(item.get("id", "")).strip()
        device = str(item.get("device", "")).strip()
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", identifier) or identifier in result:
            raise ValueError(f"invalid or duplicate serial bus id: {identifier!r}")
        if named_buses and not device.startswith("/dev/serial/by-id/"):
            raise ValueError(f"serial bus {identifier} must use /dev/serial/by-id")
        if device in devices:
            raise ValueError(f"serial adapter assigned to more than one bus: {device}")
        parity = str(item.get("parity", "E")).upper()
        if parity not in {"E", "N", "O"}:
            raise ValueError(f"invalid parity for serial bus {identifier}")
        baudrate = int(item.get("baudrate", 19200))
        stopbits = int(item.get("stopbits", 1))
        bytesize = int(item.get("bytesize", 8))
        timeout = float(item.get("timeout_seconds", 0.75))
        if baudrate <= 0 or stopbits not in {1, 2} or bytesize not in {7, 8} or timeout <= 0:
            raise ValueError(f"invalid communication settings for serial bus {identifier}")
        settings = dict(item)
        settings.update(id=identifier, device=device, baudrate=baudrate, parity=parity,
                        stopbits=stopbits, bytesize=bytesize, timeout_seconds=timeout)
        result[identifier] = settings
        devices.add(device)
    return result


def configured_registers(config: dict[str, Any]) -> list[Register]:
    result = []
    seen = set()
    for item in config["registers"]:
        key = str(item["key"])
        if key in seen:
            raise ValueError(f"duplicate register key: {key}")
        seen.add(key)
        address_value = item["address"]
        address = int(address_value, 0) if isinstance(address_value, str) else int(address_value)
        sampling = str(item.get("sampling", "normal"))
        if sampling not in {"fast", "normal", "diagnostic", "information"}:
            raise ValueError(f"invalid sampling class for {key}: {sampling}")
        result.append(Register(key, address, float(item.get("scale", 1)), str(item.get("unit", "raw")), sampling))
    if not result:
        raise ValueError("at least one register must be configured")
    return result


def configured_devices(config: dict[str, Any]) -> list[Device]:
    entries = config.get("inverters")
    if entries is None:
        legacy = dict(config["inverter"])
        legacy["model"] = legacy.get("model", "VF-AS1")
        legacy["registers"] = config["registers"]
        entries = [legacy]
    devices = []
    configured_thresholds = config.get("alerts", {}).get("metrics", {})
    alert_metrics = set(ALWAYS_MONITORED_ALERT_METRICS)
    if isinstance(configured_thresholds, dict):
        for key, threshold in configured_thresholds.items():
            if threshold is None:
                alert_metrics.discard(str(key))
            else:
                alert_metrics.add(str(key))
    buses = configured_serial_buses(config)
    slave_ids = set()
    names = set()
    for entry in entries:
        if not entry.get("enabled", True):
            continue
        name = str(entry["name"])
        if name in names:
            raise ValueError(f"duplicate inverter name: {name}")
        names.add(name)
        slave_id = int(entry["slave_id"])
        if not 1 <= slave_id <= 247:
            raise ValueError(f"invalid slave_id for {name}: {slave_id}")
        bus_id = str(entry.get("bus_id", next(iter(buses))))
        if bus_id not in buses:
            raise ValueError(f"unknown serial bus for {name}: {bus_id}")
        if (bus_id, slave_id) in slave_ids:
            raise ValueError(f"duplicate slave_id {slave_id} on serial bus {bus_id}")
        slave_ids.add((bus_id, slave_id))
        selected_profile = profile(str(entry.get("model", "VF-AS1")))
        if entry.get("replace_profile_registers", False):
            register_config = entry.get("registers", [])
        else:
            merged = {item["key"]: item for item in selected_profile["registers"]}
            merged.update({item["key"]: item for item in entry.get("registers", [])})
            register_config = list(merged.values())
        registers = configured_registers({"registers": register_config})
        channels_declared = "channels" in entry
        channel_modes = entry.get("channels", {})
        if not isinstance(channel_modes, dict):
            raise ValueError(f"channels for {name} must be an object")
        invalid_modes = {
            str(key): value for key, value in channel_modes.items()
            if value not in {"off", "live", "record"}
        }
        if invalid_modes:
            raise ValueError(f"invalid channel mode for {name}: {invalid_modes}")
        hidden_live_cards = set(entry.get("hidden_live_cards", []))
        def selected_mode(register: Register) -> str:
            default_mode = "off" if channels_declared else "record"
            return str(channel_modes.get(register.key, "record" if register.key in hidden_live_cards else default_mode))
        registers = [
            replace(register, record_history=selected_mode(register) == "record")
            for register in registers
            if selected_mode(register) != "off" or register.key == "operating_status" or register.key in alert_metrics
        ]
        max_read_words = int(entry.get("max_read_words", selected_profile.get("max_read_words", 1)))
        if not 1 <= max_read_words <= 125:
            raise ValueError(f"invalid max_read_words for {name}: {max_read_words}")
        engineering = entry.get("engineering", {})
        factor_value = engineering.get("machine_speed_factor")
        machine_speed_factor = None if factor_value is None else float(factor_value)
        if machine_speed_factor is not None and machine_speed_factor <= 0:
            raise ValueError(f"machine_speed_factor for {name} must be greater than zero")
        machine_speed_unit = str(engineering.get("machine_speed_unit", "rpm")).strip()
        if not machine_speed_unit:
            raise ValueError(f"machine_speed_unit for {name} must not be empty")
        current_value = engineering.get("rated_output_current_a")
        rated_output_current_a = None if current_value is None else float(current_value)
        voltage_value = engineering.get("rated_output_voltage_v")
        rated_output_voltage_v = None if voltage_value is None else float(voltage_value)
        if rated_output_current_a is not None and rated_output_current_a <= 0:
            raise ValueError(f"rated_output_current_a for {name} must be greater than zero")
        if rated_output_voltage_v is not None and rated_output_voltage_v <= 0:
            raise ValueError(f"rated_output_voltage_v for {name} must be greater than zero")
        power_value = engineering.get("motor_rated_power_kw")
        motor_rated_power_kw = None if power_value is None else float(power_value)
        speed_value = engineering.get("motor_rated_speed_rpm")
        motor_rated_speed_rpm = None if speed_value is None else float(speed_value)
        if (motor_rated_power_kw is None) != (motor_rated_speed_rpm is None):
            raise ValueError(f"motor rated power and speed for {name} must be configured together")
        if motor_rated_power_kw is not None and (motor_rated_power_kw <= 0 or motor_rated_speed_rpm <= 0):
            raise ValueError(f"motor rated power and speed for {name} must be greater than zero")
        devices.append(Device(
            name, selected_profile["model"], slave_id, registers,
            selected_profile["decoder"], max_read_words,
            machine_speed_factor, machine_speed_unit,
            rated_output_current_a, rated_output_voltage_v,
            motor_rated_power_kw, motor_rated_speed_rpm,
            bus_id,
        ))
    if not devices:
        raise ValueError("at least one enabled inverter must be configured")
    return devices


class Database:
    def __init__(self, path: Path, change_logging: dict[str, Any] | None = None, recording_reference: str = "", conditions: list[Any] | None = None):
        self.change_logging = change_logging or {"enabled": False}
        path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path)
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA synchronous=NORMAL")
        self.connection.execute("PRAGMA wal_autocheckpoint=128")
        self.connection.execute("PRAGMA journal_size_limit=1048576")
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS poll_cycles (
                id INTEGER PRIMARY KEY,
                observed_at TEXT NOT NULL,
                inverter TEXT NOT NULL,
                slave_id INTEGER NOT NULL,
                successful_reads INTEGER NOT NULL,
                failed_reads INTEGER NOT NULL,
                error TEXT,
                duration_ms REAL NOT NULL DEFAULT 0,
                transactions INTEGER NOT NULL DEFAULT 0,
                retries INTEGER NOT NULL DEFAULT 0,
                estimated_bus_ms REAL NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS samples (
                id INTEGER PRIMARY KEY,
                cycle_id INTEGER NOT NULL REFERENCES poll_cycles(id),
                observed_at TEXT NOT NULL,
                inverter TEXT NOT NULL,
                slave_id INTEGER NOT NULL,
                metric TEXT NOT NULL,
                metric_label TEXT NOT NULL DEFAULT '',
                register_address INTEGER NOT NULL,
                raw_value INTEGER NOT NULL,
                value REAL NOT NULL,
                unit TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS samples_metric_time
                ON samples(metric, observed_at);
            CREATE INDEX IF NOT EXISTS samples_history
                ON samples(metric, inverter, id);
            CREATE INDEX IF NOT EXISTS samples_observed_at
                ON samples(observed_at);
            CREATE INDEX IF NOT EXISTS poll_cycles_observed_at
                ON poll_cycles(observed_at);
            CREATE TABLE IF NOT EXISTS latest_values (
                inverter TEXT NOT NULL, slave_id INTEGER NOT NULL, metric TEXT NOT NULL,
                observed_at TEXT NOT NULL, register_address INTEGER NOT NULL,
                raw_value INTEGER NOT NULL, value REAL NOT NULL, unit TEXT NOT NULL,
                metric_label TEXT NOT NULL DEFAULT '',
                PRIMARY KEY (inverter, slave_id, metric)
            ) WITHOUT ROWID;
            CREATE TABLE IF NOT EXISTS latest_poll_cycles (
                inverter TEXT NOT NULL, slave_id INTEGER NOT NULL, cycle_id INTEGER NOT NULL,
                observed_at TEXT NOT NULL, successful_reads INTEGER NOT NULL,
                failed_reads INTEGER NOT NULL, error TEXT,
                PRIMARY KEY (inverter, slave_id)
            ) WITHOUT ROWID;
            CREATE TABLE IF NOT EXISTS storage_stats (
                singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
                sample_count INTEGER NOT NULL, cycle_count INTEGER NOT NULL,
                oldest_sample TEXT, newest_sample TEXT
            );
            CREATE TABLE IF NOT EXISTS storage_growth_samples (
                observed_at TEXT PRIMARY KEY,
                database_bytes INTEGER NOT NULL,
                allocated_bytes INTEGER,
                used_bytes INTEGER,
                reusable_bytes INTEGER
            ) WITHOUT ROWID;
            CREATE TABLE IF NOT EXISTS logged_values (
                inverter TEXT NOT NULL, slave_id INTEGER NOT NULL, metric TEXT NOT NULL,
                raw_value INTEGER NOT NULL, value REAL NOT NULL, unit TEXT NOT NULL,
                logged_at TEXT NOT NULL,
                PRIMARY KEY (inverter, slave_id, metric)
            ) WITHOUT ROWID;
            CREATE TABLE IF NOT EXISTS diagnostic_minutes (
                minute TEXT NOT NULL, inverter TEXT NOT NULL, slave_id INTEGER NOT NULL,
                cycles INTEGER NOT NULL, samples INTEGER NOT NULL, failed_reads INTEGER NOT NULL,
                transactions INTEGER NOT NULL, retries INTEGER NOT NULL,
                total_duration_ms REAL NOT NULL, maximum_duration_ms REAL NOT NULL,
                estimated_bus_ms REAL NOT NULL,
                PRIMARY KEY (minute, inverter, slave_id)
            ) WITHOUT ROWID;
            CREATE TABLE IF NOT EXISTS recording_info (
                singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
                reference TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS parameter_changes (
                id INTEGER PRIMARY KEY, changed_at TEXT NOT NULL, inverter TEXT NOT NULL,
                slave_id INTEGER NOT NULL, register_address INTEGER NOT NULL,
                old_raw_value INTEGER NOT NULL, new_raw_value INTEGER NOT NULL,
                verified_raw_value INTEGER NOT NULL, result TEXT NOT NULL,
                source_backup TEXT NOT NULL DEFAULT '', target_sha256 TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS thermal_events (
                id INTEGER PRIMARY KEY, observed_at TEXT NOT NULL, state TEXT NOT NULL,
                temperature_celsius REAL NOT NULL, interval_factor INTEGER NOT NULL,
                detail TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS thermal_events_observed_at ON thermal_events(observed_at);
            CREATE TABLE IF NOT EXISTS thermal_protection (
                singleton INTEGER PRIMARY KEY CHECK (singleton = 1), observed_at TEXT NOT NULL,
                state TEXT NOT NULL, temperature_celsius REAL NOT NULL, interval_factor INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS milestones (
                id INTEGER PRIMARY KEY, observed_at TEXT NOT NULL, rule_id TEXT NOT NULL,
                rule_revision INTEGER NOT NULL, rule_name TEXT NOT NULL, event_type TEXT NOT NULL,
                severity TEXT NOT NULL, source TEXT NOT NULL, metric TEXT NOT NULL,
                value REAL NOT NULL, unit TEXT NOT NULL, operator TEXT NOT NULL,
                target_value REAL NOT NULL, snapshot_json TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS milestones_observed_at ON milestones(observed_at);
            CREATE INDEX IF NOT EXISTS milestones_rule_time ON milestones(rule_id, observed_at);
            CREATE TABLE IF NOT EXISTS condition_states (
                rule_id TEXT PRIMARY KEY, signature TEXT NOT NULL, active INTEGER NOT NULL,
                pending_since TEXT, last_value REAL, last_observed_at TEXT
            ) WITHOUT ROWID;
            """
        )
        self.connection.execute(
            "INSERT OR IGNORE INTO recording_info(singleton, reference, created_at) VALUES (1, ?, ?)",
            (recording_reference, utc_now()),
        )
        columns = {row[1] for row in self.connection.execute("PRAGMA table_info(poll_cycles)")}
        for name, definition in (
            ("duration_ms", "REAL NOT NULL DEFAULT 0"),
            ("transactions", "INTEGER NOT NULL DEFAULT 0"),
            ("retries", "INTEGER NOT NULL DEFAULT 0"),
            ("estimated_bus_ms", "REAL NOT NULL DEFAULT 0"),
        ):
            if name not in columns:
                self.connection.execute(f"ALTER TABLE poll_cycles ADD COLUMN {name} {definition}")
        for table in ("samples", "latest_values"):
            columns = {row[1] for row in self.connection.execute(f"PRAGMA table_info({table})")}
            if "metric_label" not in columns:
                self.connection.execute(f"ALTER TABLE {table} ADD COLUMN metric_label TEXT NOT NULL DEFAULT ''")
        parameter_change_columns = {row[1] for row in self.connection.execute("PRAGMA table_info(parameter_changes)")}
        for name, definition in (("source_backup", "TEXT NOT NULL DEFAULT ''"), ("target_sha256", "TEXT NOT NULL DEFAULT ''")):
            if name not in parameter_change_columns:
                self.connection.execute(f"ALTER TABLE parameter_changes ADD COLUMN {name} {definition}")
        growth_columns = {row[1] for row in self.connection.execute("PRAGMA table_info(storage_growth_samples)")}
        for name in ("allocated_bytes", "used_bytes", "reusable_bytes"):
            if name not in growth_columns:
                self.connection.execute(f"ALTER TABLE storage_growth_samples ADD COLUMN {name} INTEGER")
        if self.connection.execute("SELECT 1 FROM storage_stats WHERE singleton = 1").fetchone() is None:
            self.connection.execute(
                """INSERT INTO storage_stats
                   SELECT 1, (SELECT COUNT(*) FROM samples), (SELECT COUNT(*) FROM poll_cycles),
                          (SELECT MIN(observed_at) FROM samples), (SELECT MAX(observed_at) FROM samples)"""
            )
        self.connection.commit()
        self.last_storage_growth_sample = float("-inf")
        self._record_storage_growth_sample(utc_now(), force=True)
        persisted_logged = {
            (row[0], row[1], row[2]): (row[3], row[4], row[5], row[6])
            for row in self.connection.execute(
                "SELECT inverter, slave_id, metric, raw_value, value, unit, logged_at FROM logged_values"
            )
        }
        self.last_live = {
            (row[0], row[1], row[2]): (row[3], row[4], row[5])
            for row in self.connection.execute(
                "SELECT inverter, slave_id, metric, raw_value, register_address, unit FROM latest_values"
            )
        }
        # A fresh collector process starts a new observable recording session.
        # Its first successful reads form a complete baseline even when the
        # values are unchanged from the previous process.  Persisted values can
        # still be reused explicitly for installations that prefer continuity
        # across restarts over session snapshots.
        initial_snapshot = bool(self.change_logging.get("initial_snapshot_on_start", True))
        self.last_logged = {} if self.change_logging.get("enabled", False) and initial_snapshot else persisted_logged
        # The last physically observed sample is intentionally separate from
        # last_logged: change logging may skip many steady cycles.
        self.last_observed: dict[tuple[str, int, str], tuple[int, str]] = {}
        self.last_cycle_history: dict[tuple[str, int], float] = {}
        self.communication_failures: dict[tuple[str, int], int] = {}
        self.last_communication_state: dict[tuple[str, int], int] = {}
        self.last_diagnostic_cleanup = 0.0
        self.condition_evaluator = ConditionEvaluator(self.connection, list(conditions or []))

    def _record_storage_growth_sample(self, observed_at: str, force: bool = False) -> None:
        """Sample allocated, occupied, and reusable SQLite pages."""
        now_monotonic = time.monotonic()
        if not force and now_monotonic - self.last_storage_growth_sample < 60.0:
            return
        page_count = int(self.connection.execute("PRAGMA page_count").fetchone()[0])
        freelist_count = int(self.connection.execute("PRAGMA freelist_count").fetchone()[0])
        page_size = int(self.connection.execute("PRAGMA page_size").fetchone()[0])
        allocated_bytes = page_count * page_size
        reusable_bytes = freelist_count * page_size
        used_bytes = max(0, allocated_bytes - reusable_bytes)
        with self.connection:
            self.connection.execute(
                """INSERT OR REPLACE INTO storage_growth_samples
                   (observed_at,database_bytes,allocated_bytes,used_bytes,reusable_bytes)
                   VALUES (?,?,?,?,?)""",
                (observed_at, allocated_bytes, allocated_bytes, used_bytes, reusable_bytes),
            )
        self.last_storage_growth_sample = now_monotonic

    def recording_identity(self) -> tuple[str, str]:
        row = self.connection.execute(
            "SELECT reference, created_at FROM recording_info WHERE singleton=1"
        ).fetchone()
        return (str(row[0]), str(row[1])) if row else ("", "")

    def reset_runtime_state(self) -> None:
        """Forget process-local baselines after another connection resets the recording."""
        self.last_logged.clear()
        self.last_live.clear()
        self.last_observed.clear()
        self.last_cycle_history.clear()
        self.communication_failures.clear()
        self.last_communication_state.clear()
        self.condition_evaluator.latest.clear()

    def configure_condition_rules(self, rules: list[Any]) -> None:
        self.condition_evaluator.configure(rules)

    def _communication_sample(
        self, inverter: str, slave_id: int, samples: list[tuple[Register, int]], errors: list[str]
    ) -> tuple[Register, int] | None:
        key = (inverter, slave_id)
        unreachable_after = max(1, int(self.change_logging.get(
            "communication_unreachable_after_transport_errors",
            self.change_logging.get("communication_unreachable_after_cycles", 3),
        )))
        # Reachability is deliberately independent from register support.  A
        # valid Modbus exception proves that the drive answered on the bus and
        # is therefore not a transport failure.  Successful values do not hide
        # failures of the other register groups: after a drive is switched off,
        # a long poll can otherwise finish with one late successful read during
        # power-up and incorrectly classify the whole outage as online.
        transport_errors = [error for error in errors if "Modbus exception" not in error]
        if not transport_errors:
            self.communication_failures[key] = 0
            state = 2
        else:
            failures = self.communication_failures.get(key, 0) + len(transport_errors)
            self.communication_failures[key] = failures
            state = 0 if failures >= unreachable_after else 1
        if self.last_communication_state.get(key) == state:
            return None
        self.last_communication_state[key] = state
        return COMMUNICATION_REGISTER, state

    def _samples_to_log(
        self, inverter: str, slave_id: int, samples: list[tuple[Register, int]]
    ) -> list[tuple[Register, int]]:
        samples = [(register, raw) for register, raw in samples if register.record_history]
        if not self.change_logging.get("enabled", False):
            return samples
        default_delta = float(self.change_logging.get("default_analog_delta", 0.1))
        thresholds = {**DEFAULT_CHANGE_THRESHOLDS, **self.change_logging.get("thresholds", {})}
        selected = []
        for register, raw in samples:
            previous = self.last_logged.get((inverter, slave_id, register.key))
            value = raw * register.scale
            if previous is None:
                selected.append((register, raw))
            elif register.unit == "raw":
                if raw != previous[0]:
                    selected.append((register, raw))
            elif abs(value - float(previous[1])) >= float(thresholds.get(register.key, default_delta)):
                selected.append((register, raw))
        return selected

    def store_cycle(
        self,
        observed_at: str,
        inverter: str,
        slave_id: int,
        samples: list[tuple[Register, int]],
        errors: list[str],
        stats: PollStats | None = None,
    ) -> None:
        stats = stats or PollStats()
        successful_reads = sum(1 for register, _ in samples if not register.derived)
        previous_communication_state = self.last_communication_state.get((inverter, slave_id))
        communication_sample = self._communication_sample(inverter, slave_id, samples, errors)
        # A recovery is a new trustworthy measurement boundary. Persist every
        # value received in that cycle even when it equals the pre-outage value;
        # offline viewers can then resume curves without carrying stale values
        # across an unavailable interval.
        recovered = previous_communication_state in (0, 1) and communication_sample is not None and communication_sample[1] == 2
        if recovered:
            self.last_logged = {
                key: value for key, value in self.last_logged.items()
                if key[:2] != (inverter, slave_id)
            }
            self.last_observed = {
                key: value for key, value in self.last_observed.items()
                if key[:2] != (inverter, slave_id)
            }
        logged_samples = self._samples_to_log(inverter, slave_id, samples)
        if communication_sample is not None:
            logged_samples.append(communication_sample)
        history_samples = [(register, raw, observed_at) for register, raw in logged_samples]
        if self.change_logging.get("enabled", False):
            # A sparse analogue history must express a step, not a diagonal
            # interpolation from the last stored change. Insert the actual
            # preceding cycle as a support point immediately before the new
            # changed value. Raw/status values retain their normal semantics.
            for register, raw in logged_samples:
                previous = self.last_observed.get((inverter, slave_id, register.key))
                if (register.unit != "raw" and previous is not None and previous[0] != raw
                        and previous[1] < observed_at):
                    history_samples.insert(0, (register, previous[0], previous[1]))
        live_samples = samples + ([communication_sample] if communication_sample is not None else [])
        changed_live_samples = [
            (register, raw) for register, raw in live_samples
            if self.last_live.get((inverter, slave_id, register.key))
            != (raw, register.address, register.unit)
        ]
        cycle_key = (inverter, slave_id)
        heartbeat = float(self.change_logging.get("successful_cycle_interval_seconds", 60.0))
        now_monotonic = time.monotonic()
        store_history_cycle = bool(
            logged_samples or errors or now_monotonic - self.last_cycle_history.get(cycle_key, float("-inf")) >= heartbeat
        )
        with self.connection:
            cycle_id = 0
            if store_history_cycle:
                cursor = self.connection.execute(
                    """INSERT INTO poll_cycles
                       (observed_at, inverter, slave_id, successful_reads, failed_reads, error,
                        duration_ms, transactions, retries, estimated_bus_ms)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (observed_at, inverter, slave_id, successful_reads, len(errors), "; ".join(errors) or None,
                     stats.duration_ms, stats.transactions, stats.retries, stats.estimated_bus_ms),
                )
                cycle_id = int(cursor.lastrowid)
            self.connection.executemany(
                """INSERT INTO samples
                   (cycle_id, observed_at, inverter, slave_id, metric, metric_label,
                    register_address, raw_value, value, unit)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                [
                    (
                        cycle_id,
                        sample_time,
                        inverter,
                        slave_id,
                        register.key,
                        register.label,
                        register.address,
                        raw,
                        raw * register.scale,
                        register.unit,
                    )
                    for register, raw, sample_time in history_samples
                ],
            )
            self.connection.execute(
                """INSERT INTO latest_poll_cycles
                   (inverter, slave_id, cycle_id, observed_at, successful_reads, failed_reads, error)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(inverter, slave_id) DO UPDATE SET
                     cycle_id=CASE WHEN excluded.cycle_id > 0 THEN excluded.cycle_id ELSE latest_poll_cycles.cycle_id END,
                     observed_at=excluded.observed_at,
                     successful_reads=excluded.successful_reads, failed_reads=excluded.failed_reads,
                     error=excluded.error""",
                (inverter, slave_id, cycle_id, observed_at, successful_reads, len(errors), "; ".join(errors) or None),
            )
            self.connection.executemany(
                """INSERT INTO latest_values
                   (inverter, slave_id, metric, observed_at, register_address, raw_value, value, unit, metric_label)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(inverter, slave_id, metric) DO UPDATE SET
                     observed_at=excluded.observed_at, register_address=excluded.register_address,
                     raw_value=excluded.raw_value, value=excluded.value, unit=excluded.unit,
                     metric_label=excluded.metric_label""",
                [(inverter, slave_id, register.key, observed_at, register.address, raw,
                  raw * register.scale, register.unit, register.label) for register, raw in changed_live_samples],
            )
            for register, raw in live_samples:
                self.condition_evaluator.evaluate(
                    observed_at, inverter, register.key, raw * register.scale, register.unit
                )
            self.connection.executemany(
                """INSERT INTO logged_values
                   (inverter, slave_id, metric, raw_value, value, unit, logged_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(inverter, slave_id,metric) DO UPDATE SET
                     raw_value=excluded.raw_value, value=excluded.value,
                     unit=excluded.unit, logged_at=excluded.logged_at""",
                [(inverter, slave_id, register.key, raw, raw * register.scale, register.unit, observed_at)
                 for register, raw in logged_samples],
            )
            # Communication quality is useful as a trend, but must remain a
            # compact aggregate rather than another per-poll raw time series.
            minute = f"{observed_at[:16]}:00"
            self.connection.execute(
                """INSERT INTO diagnostic_minutes
                   (minute, inverter, slave_id, cycles, samples, failed_reads, transactions,
                    retries, total_duration_ms, maximum_duration_ms, estimated_bus_ms)
                   VALUES (?, ?, ?, 1, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(minute, inverter, slave_id) DO UPDATE SET
                     cycles=cycles+1, samples=samples+excluded.samples,
                     failed_reads=failed_reads+excluded.failed_reads,
                     transactions=transactions+excluded.transactions, retries=retries+excluded.retries,
                     total_duration_ms=total_duration_ms+excluded.total_duration_ms,
                     maximum_duration_ms=MAX(maximum_duration_ms, excluded.maximum_duration_ms),
                     estimated_bus_ms=estimated_bus_ms+excluded.estimated_bus_ms""",
                (minute, inverter, slave_id, successful_reads, len(errors), stats.transactions,
                 stats.retries, stats.duration_ms, stats.duration_ms, stats.estimated_bus_ms),
            )
            if store_history_cycle:
                self.connection.execute(
                    "UPDATE storage_stats SET cycle_count=cycle_count + 1 WHERE singleton=1"
                )
            if logged_samples:
                self.connection.execute(
                    """UPDATE storage_stats SET sample_count=sample_count + ?,
                       oldest_sample=COALESCE(oldest_sample, ?), newest_sample=? WHERE singleton=1""",
                    (len(history_samples), observed_at, observed_at),
                )
        for register, raw in logged_samples:
            self.last_logged[(inverter, slave_id, register.key)] = (
                raw, raw * register.scale, register.unit, observed_at
            )
        for register, raw in changed_live_samples:
            self.last_live[(inverter, slave_id, register.key)] = (raw, register.address, register.unit)
        for register, raw in samples:
            if register.record_history:
                self.last_observed[(inverter, slave_id, register.key)] = (raw, observed_at)
        if store_history_cycle:
            self.last_cycle_history[cycle_key] = now_monotonic
        self._record_storage_growth_sample(observed_at)

    def close(self) -> None:
        try:
            self.connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        except sqlite3.Error:
            pass
        self.connection.close()

    def store_thermal_event(self, observed_at: str, state: str, temperature_celsius: float, interval_factor: int, detail: str) -> None:
        """Persist every thermal-protection transition for audit and export."""
        with self.connection:
            self.connection.execute(
                "INSERT INTO thermal_events(observed_at,state,temperature_celsius,interval_factor,detail) VALUES (?,?,?,?,?)",
                (observed_at, state, temperature_celsius, interval_factor, detail),
            )
            self.connection.execute(
                """INSERT INTO thermal_protection(singleton,observed_at,state,temperature_celsius,interval_factor)
                   VALUES (1,?,?,?,?) ON CONFLICT(singleton) DO UPDATE SET
                   observed_at=excluded.observed_at,state=excluded.state,temperature_celsius=excluded.temperature_celsius,
                   interval_factor=excluded.interval_factor""",
                (observed_at, state, temperature_celsius, interval_factor),
            )

    def reinitialize(self, reference: str, archive_path: Path | None = None) -> None:
        """Optionally back up, then clear the live database without replacing its file."""
        if archive_path is not None:
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            with sqlite3.connect(archive_path) as archive:
                self.connection.backup(archive)
        with self.connection:
            existing_tables = {
                str(row[0]) for row in self.connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
            for table in (
                "samples", "poll_cycles", "latest_values", "latest_poll_cycles",
                "logged_values", "diagnostic_minutes", "thermal_events", "thermal_protection",
                "milestones", "condition_states", "storage_growth_samples",
                "modbus_proxy_transactions",
            ):
                if table in existing_tables:
                    self.connection.execute(f"DELETE FROM {table}")
            self.connection.execute(
                "UPDATE storage_stats SET sample_count=0, cycle_count=0, oldest_sample=NULL, newest_sample=NULL WHERE singleton=1"
            )
            self.connection.execute(
                "UPDATE recording_info SET reference=?, created_at=? WHERE singleton=1",
                (reference, utc_now()),
            )
        self.reset_runtime_state()
        self.connection.execute("PRAGMA wal_checkpoint(PASSIVE)")
        self.last_storage_growth_sample = float("-inf")
        self._record_storage_growth_sample(utc_now(), force=True)

    def invalidate_metrics(self, inverter: str, slave_id: int, metrics: set[str]) -> None:
        placeholders = ",".join("?" for _ in metrics)
        parameters = (inverter, slave_id, *sorted(metrics))
        with self.connection:
            self.connection.execute(
                f"DELETE FROM latest_values WHERE inverter=? AND slave_id=? AND metric IN ({placeholders})",
                parameters,
            )
            self.connection.execute(
                f"DELETE FROM logged_values WHERE inverter=? AND slave_id=? AND metric IN ({placeholders})",
                parameters,
            )
        for metric in metrics:
            self.last_live.pop((inverter, slave_id, metric), None)
            self.last_logged.pop((inverter, slave_id, metric), None)

    def reset_source_state(self, inverter: str, slave_id: int) -> None:
        """Forget cached values after another collector cleared the database."""
        source = (inverter, slave_id)
        for cache in (self.last_logged, self.last_live, self.last_observed):
            for key in [key for key in cache if key[:2] == source]:
                cache.pop(key, None)
        self.last_cycle_history.pop(source, None)
        self.last_communication_state.pop(source, None)
        self.communication_failures.pop(source, None)

    def prune_before(self, cutoff: str) -> tuple[int, int]:
        """Delete old samples/cycles and return their respective row counts."""
        with self.connection:
            samples = self.connection.execute(
                "DELETE FROM samples WHERE observed_at < ?", (cutoff,)
            ).rowcount
            cycles = self.connection.execute(
                "DELETE FROM poll_cycles WHERE observed_at < ?", (cutoff,)
            ).rowcount
            self.connection.execute("DELETE FROM diagnostic_minutes WHERE minute < ?", (cutoff[:19],))
            bounds = self.connection.execute("SELECT MIN(observed_at), MAX(observed_at) FROM samples").fetchone()
            self.connection.execute(
                """UPDATE storage_stats SET sample_count=sample_count-?, cycle_count=cycle_count-?,
                   oldest_sample=?, newest_sample=? WHERE singleton=1""",
                (samples, cycles, bounds[0], bounds[1]),
            )
            expired = [key for key, value in self.last_logged.items() if value[3] < cutoff]
            self.connection.executemany(
                "DELETE FROM logged_values WHERE inverter=? AND slave_id=? AND metric=?", expired
            )
            for key in expired:
                self.last_logged.pop(key, None)
        self.connection.execute("PRAGMA wal_checkpoint(PASSIVE)")
        return samples, cycles


class Collector:
    def __init__(self, config: dict[str, Any], serial_factory: Callable[..., Any] | None = None):
        self.config = config
        if serial_factory is None:
            if serial is None:
                raise RuntimeError("pyserial is not installed")
            serial_factory = serial.Serial
        self.serial_factory = serial_factory
        self.port: Any | None = None
        self.access_denied_failures = 0

    def connect(self) -> None:
        settings = self.config["serial"]
        self.close()
        try:
            self.port = self.serial_factory(
                port=settings["device"],
                baudrate=int(settings["baudrate"]),
                bytesize=int(settings.get("bytesize", 8)),
                parity=str(settings.get("parity", "E")),
                stopbits=float(settings.get("stopbits", 1)),
                timeout=float(settings.get("timeout_seconds", 0.75)),
                write_timeout=float(settings.get("timeout_seconds", 0.75)),
            )
        except Exception as error:
            denied = os.name == "nt" and (
                getattr(error, "winerror", None) == 5 or "Access is denied" in str(error)
            )
            self.access_denied_failures = self.access_denied_failures + 1 if denied else 0
            limit = int(self.config.get("polling", {}).get("windows_access_denied_restart_after", 10))
            if denied and self.access_denied_failures >= max(1, limit):
                raise PortRecoveryRequired(
                    f"{settings['device']} remained inaccessible after {self.access_denied_failures} attempts; requesting service restart"
                ) from error
            raise
        self.access_denied_failures = 0
        LOG.info("serial connection open: %s", settings["device"])

    def close(self) -> None:
        if self.port is not None:
            try:
                self.port.close()
            finally:
                self.port = None

    def read_register(self, register: Register, slave_id: int) -> int:
        return self.read_range(register.address, 1, slave_id)[0]

    def read_range(self, address: int, count: int, slave_id: int) -> list[int]:
        if self.port is None or not self.port.is_open:
            self.connect()
        request = read_request(slave_id, address, count)
        self.port.reset_input_buffer()
        self.port.write(request)
        self.port.flush()
        response = self.port.read(5 + count * 2)
        return parse_read_responses(response, slave_id, count)

    def write_register(self, address: int, value: int, slave_id: int) -> None:
        if self.port is None or not self.port.is_open:
            self.connect()
        request = write_request(slave_id, address, value)
        self.port.reset_input_buffer(); self.port.write(request); self.port.flush()
        response = self.port.read(8)
        parse_write_response(response, slave_id, address, value)

    def poll(self, device: Device, registers: list[Register] | None = None) -> tuple[list[tuple[Register, int]], list[str], PollStats]:
        started = time.monotonic()
        stats = PollStats()
        polling = self.config["polling"]
        retries = int(polling.get("retries", 2))
        retry_delay = float(polling.get("retry_delay_seconds", 0.15))
        samples: list[tuple[Register, int]] = []
        errors: list[str] = []
        selected = registers if registers is not None else device.registers
        ranges: list[list[Register]] = []
        for register in sorted(selected, key=lambda item: item.address):
            if not ranges or register.address - ranges[-1][0].address >= device.max_read_words:
                ranges.append([register])
            else:
                ranges[-1].append(register)
        for group in ranges:
            start = group[0].address
            count = group[-1].address - start + 1
            last_error: Exception | None = None
            for attempt in range(retries + 1):
                stats.transactions += 1
                if attempt:
                    stats.retries += 1
                serial_settings = self.config["serial"]
                parity_bits = 0 if str(serial_settings.get("parity", "E")).upper() == "N" else 1
                bits_per_character = 1 + int(serial_settings.get("bytesize", 8)) + parity_bits + float(serial_settings.get("stopbits", 1))
                stats.estimated_bus_ms += (8 + 5 + count * 2) * bits_per_character * 1000 / int(serial_settings["baudrate"])
                try:
                    values = self.read_range(start, count, device.slave_id)
                    samples.extend((register, values[register.address - start]) for register in group)
                    last_error = None
                    break
                except ModbusException as error:
                    # The inverter returned a complete, valid frame. The serial
                    # connection is healthy and must remain open, especially on
                    # Windows where an immediate FTDI close/reopen can fail with
                    # ERROR_ACCESS_DENIED while the driver releases its handle.
                    last_error = error
                    break
                except (OSError, ProtocolError) as error:
                    last_error = error
                    self.close()
                    if attempt < retries:
                        time.sleep(retry_delay)
                except Exception as error:
                    # pyserial's SerialException is not an OSError on every version.
                    if serial is None or not isinstance(error, serial.SerialException):
                        raise
                    last_error = error
                    self.close()
                    if attempt < retries:
                        time.sleep(retry_delay)
            if last_error is not None:
                names = ", ".join(register.key for register in group)
                message = f"{names} (0x{start:04X}-0x{start + count - 1:04X}): {last_error}"
                errors.append(message)
                LOG.warning("read failed: %s", message)
        stats.duration_ms = (time.monotonic() - started) * 1000
        return samples, errors, stats


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def host_temperature_celsius() -> float | None:
    """Read the Pi thermal zones without adding a psutil dependency."""
    readings: list[float] = []
    for sensor in Path("/sys/class/thermal").glob("thermal_zone*/temp"):
        try:
            readings.append(int(sensor.read_text(encoding="utf-8").strip()) / 1000.0)
        except (OSError, ValueError):
            continue
    return max(readings) if readings else None


def add_derived_samples(device: Device, samples: list[tuple[Register, int]]) -> list[tuple[Register, int]]:
    result = list(samples)
    by_key = {register.key: (register, raw) for register, raw in samples}
    for register, raw in samples:
        if register.key == "input_terminal_status":
            for signal, bit in terminal_signal_bits(device.model).items():
                result.append((Register(
                    f"terminal_{signal.lower()}", register.address, 1, "on/off", register.sampling,
                    derived=True, record_history=register.record_history,
                ), 1 if raw & (1 << bit) else 0))
        if register.key == "calculated_motor_speed" and device.machine_speed_factor is not None:
            result.append((Register(
                "machine_speed", register.address,
                register.scale * device.machine_speed_factor,
                device.machine_speed_unit, register.sampling, derived=True,
                record_history=register.record_history,
            ), raw))
        elif register.key == "output_current" and device.rated_output_current_a is not None:
            result.append((Register(
                "actual_output_current", register.address,
                register.scale * device.rated_output_current_a / 100.0,
                "A", register.sampling, derived=True, record_history=register.record_history,
            ), raw))
        elif register.key == "output_voltage" and device.rated_output_voltage_v is not None:
            result.append((Register(
                "actual_output_voltage", register.address,
                register.scale * device.rated_output_voltage_v / 100.0,
                "V", register.sampling, derived=True, record_history=register.record_history,
            ), raw))
    if device.motor_rated_power_kw is not None and device.motor_rated_speed_rpm is not None:
        rated_torque_nm = 9550.0 * device.motor_rated_power_kw / device.motor_rated_speed_rpm
        torque_sample = by_key.get("torque")
        speed_sample = by_key.get("calculated_motor_speed")
        if torque_sample is not None:
            register, raw = torque_sample
            result.append((Register(
                "actual_motor_torque", register.address,
                register.scale * rated_torque_nm / 100.0,
                "Nm", register.sampling, derived=True, record_history=register.record_history,
            ), raw))
        if torque_sample is not None and speed_sample is not None:
            torque_register, torque_raw = torque_sample
            speed_register, speed_raw = speed_sample
            torque_nm = torque_raw * torque_register.scale * rated_torque_nm / 100.0
            speed_rpm = speed_raw * speed_register.scale
            power_kw = torque_nm * speed_rpm / 9550.0
            result.append((Register(
                "mechanical_power", torque_register.address,
                0.001, "kW", torque_register.sampling, derived=True,
                record_history=torque_register.record_history and speed_register.record_history,
            ), int(round(power_kw * 1000.0))))
    return result


def process_recording_request(
    database: Database, database_path: Path, change_logging: dict[str, Any], request_path: Path
) -> Database:
    if not request_path.is_file():
        return database
    result_path = request_path.with_name("recording-result.json")
    try:
        request = json.loads(request_path.read_text(encoding="utf-8"))
        operation_id = str(request.get("operation_id", "")).strip() or None
        action = str(request.get("action", "archive"))
        reference = str(request.get("reference", "")).strip()
        if not reference or len(reference) > 240:
            raise ValueError("recording reference must contain 1 to 240 characters")
        if action not in {"archive", "delete"}:
            raise ValueError("recording action must be archive or delete")
        if action == "delete" and str(request.get("confirmation", "")).split() != ["DELETE"] * 3:
            raise ValueError("permanent deletion requires DELETE repeated three times")

        row = database.connection.execute(
            "SELECT reference FROM recording_info WHERE singleton = 1"
        ).fetchone()
        previous_reference = str(row[0]).strip() if row else ""
        archived_to = None
        archive_path = None
        if action == "archive":
            archive_dir = database_path.parent / "archive"
            archive_dir.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            safe_reference = re.sub(r"[^A-Za-z0-9_.-]+", "-", previous_reference).strip("-.")[:60] or "recording"
            archive_path = archive_dir / f"{database_path.stem}-{stamp}-{safe_reference}{database_path.suffix}"
            counter = 1
            while archive_path.exists():
                archive_path = archive_dir / f"{database_path.stem}-{stamp}-{safe_reference}-{counter}{database_path.suffix}"
                counter += 1
            archived_to = str(archive_path)
        database.reinitialize(reference, archive_path)
        result = {"status": "complete", "operation_id": operation_id, "action": action, "reference": reference, "archived_to": archived_to}
        LOG.warning("recording database reinitialized: action=%s reference=%r archive=%s", action, reference, archived_to)
        result_path.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
        return database
    except Exception as error:
        result_path.write_text(json.dumps({"status": "error", "operation_id": locals().get("operation_id"), "detail": str(error)}), encoding="utf-8")
        LOG.error("recording database reinitialization failed: %s", error)
        return database
    finally:
        request_path.unlink(missing_ok=True)


def run_proxy_administration(config: dict[str, Any], stop: threading.Event) -> None:
    """Process recording administration without entering the serial forwarding path."""
    database_path = Path(config["storage"]["database"])
    request_path = database_path.parent / "recording-request.json"
    database: Database | None = None
    LOG.info("proxy administration worker started")
    try:
        while not stop.is_set():
            try:
                if database is None:
                    database = Database(
                        database_path,
                        config["storage"].get("change_logging"),
                        str(config.get("recording", {}).get("reference", "")).strip(),
                        condition_rules(config),
                    )
                database = process_recording_request(
                    database, database_path, config["storage"].get("change_logging", {}), request_path
                )
                stop.wait(0.25)
            except Exception as error:
                LOG.error("proxy administration worker recovering after error: %s", error)
                if database is not None:
                    try: database.close()
                    except Exception: pass
                database = None
                stop.wait(1.0)
    finally:
        if database is not None:
            database.close()
        LOG.info("proxy administration worker stopped")


def process_engineering_request(
    database: Database, devices: list[Device], request_path: Path
) -> list[Device]:
    if not request_path.is_file():
        return devices
    result_path = request_path.with_name("engineering-result.json")
    try:
        request = json.loads(request_path.read_text(encoding="utf-8"))
        name = str(request["inverter"])
        engineering = request["engineering"]
        factor = float(engineering["machine_speed_factor"])
        unit = str(engineering["machine_speed_unit"]).strip()
        current = float(engineering["rated_output_current_a"])
        voltage = float(engineering["rated_output_voltage_v"])
        power_value = engineering.get("motor_rated_power_kw")
        speed_value = engineering.get("motor_rated_speed_rpm")
        power = None if power_value in (None, "") else float(power_value)
        speed = None if speed_value in (None, "") else float(speed_value)
        if factor <= 0 or current <= 0 or voltage <= 0 or not unit or len(unit) > 20:
            raise ValueError("engineering values must be positive and the unit must contain 1 to 20 characters")
        if (power is None) != (speed is None) or (power is not None and (power <= 0 or speed <= 0)):
            raise ValueError("motor rated power and speed must be positive and configured together")
        updated = []
        found = False
        for device in devices:
            if device.name == name:
                device = replace(
                    device, machine_speed_factor=factor, machine_speed_unit=unit,
                    rated_output_current_a=current, rated_output_voltage_v=voltage,
                    motor_rated_power_kw=power, motor_rated_speed_rpm=speed,
                )
                database.invalidate_metrics(device.name, device.slave_id, {
                    "machine_speed", "actual_output_current", "actual_output_voltage",
                    "actual_motor_torque", "mechanical_power",
                })
                found = True
            updated.append(device)
        if not found:
            raise ValueError(f"unknown inverter: {name}")
        result_path.write_text(json.dumps({"status": "complete", "inverter": name}, ensure_ascii=False), encoding="utf-8")
        LOG.info("engineering settings updated for %s", name)
        return updated
    except Exception as error:
        result_path.write_text(json.dumps({"status": "error", "detail": str(error)}), encoding="utf-8")
        LOG.error("engineering settings update failed: %s", error)
        return devices
    finally:
        request_path.unlink(missing_ok=True)


def process_channels_request(devices: list[Device], request_path: Path) -> list[Device]:
    """Hot-reload channel modes after the web process atomically updated config.json."""
    if not request_path.is_file():
        return devices
    result_path = request_path.with_name("channels-result.json")
    try:
        request = json.loads(request_path.read_text(encoding="utf-8"))
        updated = configured_devices(request["config"])
        result_path.write_text(json.dumps({"status": "complete"}), encoding="utf-8")
        LOG.info("measurement channel configuration reloaded")
        return updated
    except Exception as error:
        result_path.write_text(json.dumps({"status": "error", "detail": str(error)}), encoding="utf-8")
        LOG.error("measurement channel reload failed: %s", error)
        return devices
    finally:
        request_path.unlink(missing_ok=True)


def process_conditions_request(database: Database, request_path: Path) -> None:
    if not request_path.is_file():
        return
    result_path = request_path.with_name("conditions-result.json")
    try:
        request = json.loads(request_path.read_text(encoding="utf-8"))
        rules = condition_rules(request["config"])
        database.configure_condition_rules(rules)
        result_path.write_text(json.dumps({"status": "complete", "rules": len(rules)}), encoding="utf-8")
    except Exception as error:
        result_path.write_text(json.dumps({"status": "error", "detail": str(error)}), encoding="utf-8")
        LOG.exception("condition configuration reload failed")
    finally:
        request_path.unlink(missing_ok=True)


def parse_pcm_template(content: str) -> tuple[list[str], list[tuple[int, int, int, int]]]:
    """Parse PCM002Z ASCII data while preserving its eight-line header."""
    lines = content.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    if len(lines) < 9 or lines[0] != "###":
        raise ValueError("not a PCM002Z PCM file")
    records = []
    for line_number, line in enumerate(lines[8:], start=9):
        parts = line.split(",")
        if len(parts) != 4 or not re.fullmatch(r"[0-9A-Fa-f]{4}", parts[0]):
            raise ValueError(f"invalid PCM record at line {line_number}")
        address = int(parts[0], 16)
        try:
            original_value, marker_a, marker_b = int(parts[1]), int(parts[2]), int(parts[3])
        except ValueError as error:
            raise ValueError(f"invalid PCM value or flags at line {line_number}") from error
        records.append((address, original_value, marker_a, marker_b))
    if not records or len(records) > 2000:
        raise ValueError("PCM template must contain 1 to 2000 records")
    return lines[:8], records


def pcm_template_matches_model(header: list[str], model: str) -> bool:
    """Match a PCM002Z header to TMM's model family without trusting its filename."""
    if len(header) < 3:
        return False
    template_model = f"{header[1]}{header[2]}".replace("-", "").upper()
    configured_model = model.replace("-", "").upper()
    return configured_model in template_model or template_model in configured_model


def parameter_backup_files(directory: Path, inverter_name: str) -> list[Path]:
    """Return only PCM backups created for the requested configured inverter."""
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "-", inverter_name).strip("-.") or "inverter"
    name_pattern = re.compile(rf"{re.escape(safe_name)}-\d{{8}}-\d{{6}}(?:-partial)?\.pcm\Z")
    return sorted(
        (path for path in directory.glob("*.pcm") if name_pattern.fullmatch(path.name)),
        key=lambda path: path.stat().st_mtime, reverse=True,
    )


def collector_for_device(collector_or_buses: Collector | dict[str, Collector], device: Device) -> Collector:
    return collector_or_buses[device.bus_id] if isinstance(collector_or_buses, dict) else collector_or_buses


def pcm_display_value(original_value: int, raw_value: int) -> int:
    """Preserve PCM002Z's signed decimal convention when the template proves it."""
    if original_value < 0 and raw_value >= 0x8000:
        return raw_value - 0x10000
    return raw_value


def process_parameter_backup_request(
    collector: Collector | dict[str, Collector], devices: list[Device], request_path: Path, output_dir: Path
) -> None:
    if not request_path.is_file():
        return
    result_path = request_path.with_name("parameter-backup-result.json")
    try:
        request = json.loads(request_path.read_text(encoding="utf-8"))
        name = str(request["inverter"])
        device = next((item for item in devices if item.name == name), None)
        if device is None:
            raise ValueError(f"unknown inverter: {name}")
        selected_collector = collector_for_device(collector, device)
        header, records = parse_pcm_template(str(request["content"]))
        if not pcm_template_matches_model(header, device.model):
            raise ValueError(f"PCM template model {header[1]}{header[2]} does not match {device.model}")
        registers = [Register(f"parameter_{address:04X}", address, 1, "raw", "information") for address, _, _, _ in records]
        samples, errors, _stats = selected_collector.poll(device, registers)
        values = {register.address: raw for register, raw in samples}
        missing = [(address, original) for address, original, _, _ in records if address not in values]
        output_dir.mkdir(parents=True, exist_ok=True)
        safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "-", name).strip("-.") or "inverter"
        suffix = "-partial" if missing else ""
        filename = f"{safe_name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}{suffix}.pcm"
        output_path = output_dir / filename
        output_lines = header + [
            f"{address:04X},{pcm_display_value(original, values.get(address, original))},{marker_a},{marker_b}"
            for address, original, marker_a, marker_b in records
        ]
        output_path.write_bytes(("\r\n".join(output_lines) + "\r\n").encode("ascii"))
        report_name = None
        if missing:
            report_path = output_path.with_suffix(".txt")
            report_name = report_path.name
            report_lines = [
                "* Communication Error Parameters",
                "* Values below were retained from the selected PCM template.",
                *(f"{address:04X}: retained template raw value {original}" for address, original in missing),
                "",
                "* Modbus errors",
                *errors,
            ]
            report_path.write_text("\r\n".join(report_lines) + "\r\n", encoding="ascii", errors="replace")
        result_path.write_text(json.dumps({
            "status": "complete_with_warnings" if missing else "complete",
            "file": filename, "report": report_name, "records": len(records),
            "refreshed_records": len(values), "retained_records": len(missing), "inverter": name,
        }), encoding="utf-8")
        LOG.info("PCM002Z parameter backup complete: %s (%d refreshed, %d retained)", output_path, len(values), len(missing))
    except Exception as error:
        result_path.write_text(json.dumps({"status": "error", "detail": str(error)}), encoding="utf-8")
        LOG.error("PCM002Z parameter backup failed: %s", error)
    finally:
        request_path.unlink(missing_ok=True)


def confirm_safe_parameter_write_state(collector: Collector, device: Device) -> None:
    """Confirm the same stop criteria used immediately before every FC06 write."""
    stationary = [
        Register("safe_output_frequency", 0xFD00, 0.01, "Hz", "fast"),
        Register("safe_operating_status", 0xFD01, 1, "raw", "fast"),
        Register("safe_input_terminal_status", 0xFD06, 1, "raw", "fast"),
    ]
    for _ in range(3):
        samples, errors, _ = collector.poll(device, stationary)
        values = {register.key: raw for register, raw in samples}
        if errors or len(values) != 3:
            raise RuntimeError("safe standstill cannot be confirmed: communication incomplete")
        status = values["safe_operating_status"]
        if values["safe_output_frequency"] != 0 or status & (1 << 10) or values["safe_input_terminal_status"] & 0x0003:
            raise RuntimeError("safe standstill cannot be confirmed: output or F/R command active")
        if status & ((1 << 1) | (1 << 2) | (1 << 12)):
            raise RuntimeError("safe standstill cannot be confirmed: trip, alarm, or emergency stop active")
        time.sleep(0.15)


def process_parameter_preflight_request(collector: Collector | dict[str, Collector], devices: list[Device], request_path: Path) -> None:
    if not request_path.is_file():
        return
    result_path = request_path.with_name("parameter-preflight-result.json")
    try:
        request = json.loads(request_path.read_text(encoding="utf-8"))
        name = str(request["inverter"])
        device = next((item for item in devices if item.name == name), None)
        if device is None or device.model != "VF-AS1":
            raise ValueError("parameter preflight is currently limited to VF-AS1")
        confirm_safe_parameter_write_state(collector_for_device(collector, device), device)
        result_path.write_text(json.dumps({"status": "ready", "checked_at": utc_now(), "inverter": name}), encoding="utf-8")
    except Exception as error:
        result_path.write_text(json.dumps({"status": "blocked", "detail": str(error)}), encoding="utf-8")
        LOG.warning("parameter write preflight blocked: %s", error)
    finally:
        request_path.unlink(missing_ok=True)


def process_parameter_write_request(
    database: Database, collector: Collector | dict[str, Collector], devices: list[Device], request_path: Path
) -> None:
    if not request_path.is_file():
        return
    result_path = request_path.with_name("parameter-write-result.json")
    completed: list[dict[str, int | str]] = []
    try:
        request = json.loads(request_path.read_text(encoding="utf-8"))
        name = str(request["inverter"])
        changes = [(int(item["address"]), int(item["target"])) for item in request["changes"]]
        source_backup = str(request.get("source_backup", ""))[:255]
        target_sha256 = str(request.get("target_sha256", ""))[:64]
        device = next((item for item in devices if item.name == name), None)
        if device is None or device.model != "VF-AS1":
            raise ValueError("single parameter writing is currently limited to VF-AS1")
        selected_collector = collector_for_device(collector, device)
        if not 1 <= len(changes) <= 32 or len({address for address, _target in changes}) != len(changes):
            raise ValueError("write request must contain 1 to 32 distinct parameters")
        if any(parameter_safety_class(address, 1, device.model) != "candidate" or not 0 <= target <= 0xFFFF for address, target in changes):
            raise ValueError("write request contains an invalid configuration candidate")
        for address, target in changes:
            confirm_safe_parameter_write_state(selected_collector, device)
            old = selected_collector.read_register(Register("parameter", address, 1, "raw"), device.slave_id)
            selected_collector.write_register(address, target, device.slave_id)
            verified = selected_collector.read_register(Register("parameter", address, 1, "raw"), device.slave_id)
            if verified != target:
                raise RuntimeError(f"write verification failed for {address:04X}: expected {target}, read {verified}")
            with database.connection:
                database.connection.execute(
                    "INSERT INTO parameter_changes(changed_at,inverter,slave_id,register_address,old_raw_value,new_raw_value,verified_raw_value,result,source_backup,target_sha256) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (utc_now(), name, device.slave_id, address, old, target, verified, "verified", source_backup, target_sha256),
                )
            completed.append({"address": f"{address:04X}", "old": old, "new": target})
            LOG.warning("parameter write verified: %s 0x%04X %d -> %d", name, address, old, target)
        result_path.write_text(json.dumps({"status": "complete", "changes": completed}), encoding="utf-8")
    except Exception as error:
        # A deliberately sequential batch cannot be rolled back safely.  Keep
        # the verified prefix visible to the operator and in the audit table.
        result_path.write_text(json.dumps({
            "status": "partial" if completed else "error", "detail": str(error), "changes": completed,
        }), encoding="utf-8")
        LOG.error("parameter write rejected/failed: %s", error)
    finally:
        request_path.unlink(missing_ok=True)


def run_addon_collector(
    definition: Any, database_path: Path, change_logging: dict[str, Any],
    recording_reference: str, stop: threading.Event, config_path: Path | None = None,
) -> None:
    """Poll one I²C card independently of Modbus and serial Modbus.

    Each thread owns its SQLite connection. I²C transfers themselves are
    serialized through ``ADDON_I2C_LOCK``; this keeps physical HAT reads
    atomic while still isolating their timing from RS-485 reconnects.
    """
    # SequentAddon.changes() already applies each channel's engineering
    # threshold and its system-card heartbeat.  Applying the global Modbus
    # change logger a second time can suppress even the initial Fan/UPS point.
    initial_config = load_config(config_path) if config_path and config_path.exists() else {}
    database = Database(database_path, {**change_logging, "enabled": False}, recording_reference,
                        condition_rules(initial_config))
    runtime = SequentAddon(definition, fan_policy_path=database_path.parent / "smart-fan-policy.json")
    next_due = 0.0
    next_error_log = 0.0
    unavailable = False
    # A card can be healthy while every user-facing channel is disabled.
    # Persist exactly one empty successful cycle on start/reload and after an
    # outage so a historical failure cannot remain the card's current health.
    # Normal empty polls stay write-free to avoid database churn.
    health_confirmed = False
    config_mtime = config_path.stat().st_mtime_ns if config_path and config_path.exists() else None
    recording_identity = database.recording_identity()
    next_recording_check = 0.0
    LOG.info("add-on collector started: %s (stack %d)", definition.label, definition.stack)

    def store_addon_cycle(observed_at: str, registers: list[tuple[Register, int]], errors: list[str]) -> bool:
        """Wait out recording maintenance without misreporting an I²C card failure."""
        nonlocal recording_identity, health_confirmed
        delay = 0.02
        retries = 0
        while not stop.is_set():
            try:
                current_identity = database.recording_identity()
                if current_identity != recording_identity:
                    recording_identity = current_identity
                    runtime.reset_recording_baseline()
                    database.reset_source_state(runtime.definition.source_name, -(runtime.definition.stack + 1))
                    health_confirmed = False
                    LOG.info("add-on discarded pre-reset sample and reset baseline: %s", runtime.definition.label)
                    return False
                database.store_cycle(observed_at, runtime.definition.source_name,
                                     -(runtime.definition.stack + 1), registers, errors)
                return True
            except sqlite3.OperationalError as error:
                if "locked" not in str(error).lower() and "busy" not in str(error).lower():
                    raise
                retries += 1
                if retries == 1 or retries % 100 == 0:
                    LOG.warning("add-on persistence waiting for recording maintenance: %s", runtime.definition.label)
                stop.wait(delay)
                delay = min(0.5, delay * 1.5)
        raise RuntimeError("collector stopping")
    try:
        while not stop.is_set():
            # Recording reinitialization is performed by the Modbus collector
            # on its own SQLite connection.  An add-on keeps separate runtime
            # and database caches, so it must explicitly create a fresh
            # baseline afterwards.  Digital 0 and 1 are both valid states.
            check_now = time.monotonic()
            if check_now >= next_recording_check:
                next_recording_check = check_now + 0.5
                current_identity = database.recording_identity()
                if current_identity != recording_identity:
                    recording_identity = current_identity
                    runtime.reset_recording_baseline()
                    database.reset_source_state(runtime.definition.source_name, -(runtime.definition.stack + 1))
                    health_confirmed = False
                    LOG.info("add-on recording generation reset: %s", runtime.definition.label)
            if config_path and config_path.exists():
                current_mtime = config_path.stat().st_mtime_ns
                if current_mtime != config_mtime:
                    config_mtime = current_mtime
                    try:
                        updated = next(item for item in configured_addons(load_config(config_path)) if item.identifier == definition.identifier)
                        runtime.close()
                        runtime = SequentAddon(updated, fan_policy_path=database_path.parent / "smart-fan-policy.json")
                        database.configure_condition_rules(condition_rules(load_config(config_path)))
                        definition = updated
                        health_confirmed = False
                        LOG.info("add-on channel configuration reloaded: %s", definition.label)
                    except StopIteration:
                        LOG.warning("configured add-on was removed: %s", definition.identifier)
                        break
                    except Exception as error:
                        LOG.warning("add-on configuration reload failed: %s", error)
            # A disabled card stays owned by this lightweight worker so it can
            # be re-enabled from the UI without a service restart.  Crucially,
            # it performs no I²C transaction while switched off.
            if not definition.enabled:
                stop.wait(0.5)
                continue
            now = time.monotonic()
            if now < next_due:
                stop.wait(max(0.001, next_due - now))
                continue
            observed_at = utc_now()
            try:
                with ADDON_I2C_LOCK:
                    samples = runtime.changes(now)
                if unavailable:
                    LOG.info("add-on communication restored: %s", runtime.definition.label)
                    unavailable = False
                registers = [
                    (Register(sample.metric, 0xE000 + index, sample.value / sample.raw_value if sample.raw_value else 1.0,
                              sample.unit, "fast", record_history=sample.record_history, label=sample.label), sample.raw_value)
                    for index, sample in enumerate(samples)
                ]
                if registers or not health_confirmed:
                    stored = store_addon_cycle(observed_at, registers, [])
                    if not stored:
                        continue
                    if not health_confirmed:
                        LOG.info("add-on communication verified: %s", runtime.definition.label)
                    health_confirmed = True
            except Exception as error:
                detail = f"{runtime.definition.label}: {error}"
                if now >= next_error_log:
                    store_addon_cycle(observed_at, [], [detail])
                    LOG.warning("add-on unavailable: %s", detail)
                    next_error_log = now + 1.0
                unavailable = True
                health_confirmed = False
                # A disconnected card needs no high-frequency reprobe.  Apart
                # from avoiding needless I²C traffic, this protects against
                # third-party drivers that allocate resources during a failed
                # detection attempt.
                next_due = max(next_due, now + 2.0)
            while next_due <= now:
                next_due += runtime.definition.interval_seconds
    finally:
        runtime.close()
        database.close()
        LOG.info("add-on collector stopped")


def start_addon_collectors(
    config: dict[str, Any], database_path: Path, stop: threading.Event,
) -> list[threading.Thread]:
    """Start independent Sequent workers for normal and proxy operation."""
    change_logging = config["storage"].get("change_logging", {
        "enabled": True,
        "default_analog_delta": 0.1,
        "thresholds": DEFAULT_CHANGE_THRESHOLDS,
    })
    recording_reference = str(config.get("recording", {}).get("reference", "")).strip()
    config_path = Path(config["_config_path"]) if config.get("_config_path") else None
    threads: list[threading.Thread] = []
    for definition in configured_addons(config):
        thread = threading.Thread(
            target=run_addon_collector,
            args=(definition, database_path, change_logging, recording_reference, stop),
            kwargs={"config_path": config_path} if config_path else {},
            name=f"tmm-addon-{definition.identifier}", daemon=True,
        )
        thread.start()
        threads.append(thread)
    return threads


def run(config: dict[str, Any], once: bool = False) -> int:
    stop = threading.Event()
    if not once:
        signal.signal(signal.SIGTERM, lambda *_: stop.set())
        signal.signal(signal.SIGINT, lambda *_: stop.set())

    change_logging = config["storage"].get("change_logging", {
        "enabled": True,
        "default_analog_delta": 0.1,
        "thresholds": DEFAULT_CHANGE_THRESHOLDS,
    })
    database_path = Path(config["storage"]["database"])
    recording_reference = str(config.get("recording", {}).get("reference", "")).strip()
    database = Database(database_path, change_logging, recording_reference, condition_rules(config))
    recording_request = database_path.parent / "recording-request.json"
    engineering_request = database_path.parent / "engineering-request.json"
    channels_request = database_path.parent / "channels-request.json"
    conditions_request = database_path.parent / "conditions-request.json"
    parameter_backup_request = database_path.parent / "parameter-backup-request.json"
    parameter_backup_dir = database_path.parent / "parameter-backups"
    parameter_preflight_request = database_path.parent / "parameter-preflight-request.json"
    parameter_write_request = database_path.parent / "parameter-write-request.json"
    collectors = {
        identifier: Collector({**config, "serial": settings})
        for identifier, settings in configured_serial_buses(config).items()
    }
    devices = configured_devices(config)
    addon_runtimes = [SequentAddon(definition) for definition in configured_addons(config)]
    addon_threads: list[threading.Thread] = []
    if addon_runtimes and not once:
        for runtime in addon_runtimes:
            thread = threading.Thread(
                target=run_addon_collector,
                args=(runtime.definition, database_path, change_logging, recording_reference, stop),
                kwargs={"config_path": Path(config.get("_config_path", ""))} if config.get("_config_path") else {},
                name=f"tmm-addon-{runtime.definition.identifier}", daemon=True,
            )
            thread.start()
            addon_threads.append(thread)
    polling_config = config["polling"]
    legacy_interval = float(polling_config.get("interval_seconds", 1.0))
    configured_intervals = polling_config.get("intervals", {})
    intervals = {
        "fast": float(configured_intervals.get("fast", legacy_interval)),
        "normal": float(configured_intervals.get("normal", legacy_interval)),
        "diagnostic": float(configured_intervals.get("diagnostic", legacy_interval)),
        "information": float(configured_intervals.get("information", 3600.0)),
    }
    if any(value <= 0 for value in intervals.values()):
        raise ValueError("all polling intervals must be greater than zero")
    reconnect_delay = float(config["polling"].get("reconnect_delay_seconds", 2.0))
    retention_days = float(config["storage"].get("retention_days", 0))
    cleanup_interval = max(60.0, float(config["storage"].get("cleanup_interval_seconds", 3600)))
    next_cleanup = 0.0
    next_due = {sampling: 0.0 for sampling in intervals}
    next_status_log = 0.0
    thermal_state = "normal"
    thermal_factor = 1
    thermal_cooled_below_limit = False
    LOG.info(
        "collector started for %d inverter(s): %s",
        len(devices),
        ", ".join(f"{device.name}/{device.model} (slave {device.slave_id})" for device in devices),
    )

    try:
        while not stop.is_set():
            database = process_recording_request(database, database_path, change_logging, recording_request)
            devices = process_engineering_request(database, devices, engineering_request)
            devices = process_channels_request(devices, channels_request)
            process_conditions_request(database, conditions_request)
            process_parameter_backup_request(collectors, devices, parameter_backup_request, parameter_backup_dir)
            process_parameter_preflight_request(collectors, devices, parameter_preflight_request)
            process_parameter_write_request(database, collectors, devices, parameter_write_request)
            temperature = host_temperature_celsius()
            if temperature is not None:
                if thermal_state == "normal" and temperature >= 75.0:
                    thermal_state, thermal_factor, thermal_cooled_below_limit = "throttled", 2, False
                    database.store_thermal_event(utc_now(), thermal_state, temperature, thermal_factor, "Pi temperature reached 75 °C; polling interval doubled")
                    LOG.warning("thermal protection throttled polling at %.1f °C", temperature)
                elif thermal_state == "throttled":
                    if temperature < 70.0:
                        thermal_state, thermal_factor, thermal_cooled_below_limit = "normal", 1, False
                        database.store_thermal_event(utc_now(), thermal_state, temperature, thermal_factor, "Pi cooled below 70 °C; normal polling restored")
                        LOG.info("thermal protection restored normal polling at %.1f °C", temperature)
                    elif temperature < 75.0:
                        thermal_cooled_below_limit = True
                    elif thermal_cooled_below_limit:
                        thermal_state, thermal_factor = "paused", 2
                        database.store_thermal_event(utc_now(), thermal_state, temperature, thermal_factor, "Pi temperature crossed 75 °C again while throttled; polling paused")
                        LOG.error("thermal protection paused polling at %.1f °C", temperature)
                elif thermal_state == "paused" and temperature < 70.0:
                    thermal_state, thermal_factor, thermal_cooled_below_limit = "normal", 1, False
                    database.store_thermal_event(utc_now(), thermal_state, temperature, thermal_factor, "Pi cooled below 70 °C; polling resumed")
                    LOG.info("thermal protection resumed polling at %.1f °C", temperature)
            if thermal_state == "paused":
                stop.wait(1.0)
                continue
            cycle_start = time.monotonic()
            due = list(intervals) if once else [name for name in intervals if cycle_start >= next_due[name]]
            due_addons = addon_runtimes if once else []
            if not due and not due_addons:
                wake_at = min([*next_due.values()] or [cycle_start + 1.0])
                stop.wait(max(0.001, wake_at - cycle_start))
                continue
            all_errors = []
            displayed_samples = []
            any_samples = False
            for device in devices:
                for sampling in due:
                    registers = [register for register in device.registers if register.sampling == sampling]
                    if not registers:
                        continue
                    observed_at = utc_now()
                    samples, errors, stats = collectors[device.bus_id].poll(device, registers)
                    samples = add_derived_samples(device, samples)
                    database.store_cycle(observed_at, device.name, device.slave_id, samples, errors, stats)
                    any_samples = any_samples or bool(samples)
                    all_errors.extend(f"{device.name}: {error}" for error in errors)
                    displayed_samples.extend((device, register, raw) for register, raw in samples)
            for runtime in due_addons:
                observed_at = utc_now()
                try:
                    addon_samples = runtime.changes(cycle_start)
                    addon_registers = [
                        (Register(sample.metric, 0xE000 + index, sample.value / sample.raw_value if sample.raw_value else 1.0, sample.unit, "fast", record_history=sample.record_history, label=sample.label), sample.raw_value)
                        for index, sample in enumerate(addon_samples)
                    ]
                    if addon_registers:
                        database.store_cycle(observed_at, runtime.definition.source_name, -(runtime.definition.stack + 1), addon_registers, [])
                        any_samples = True
                except Exception as error:
                    detail = f"{runtime.definition.label}: {error}"
                    database.store_cycle(observed_at, runtime.definition.source_name, -(runtime.definition.stack + 1), [], [detail])
                    LOG.warning("add-on unavailable: %s", detail)
                    all_errors.append(detail)
            # Schedule from the end of the work, not its start.  A complete
            # Modbus round can legitimately take longer than a fast sampling
            # interval.  Advancing only to ``cycle_start`` in that case leaves
            # every due time in the past and turns the collector into a busy
            # loop which continuously tries to catch up.
            completed_at = time.monotonic()
            for sampling in due:
                while next_due[sampling] <= completed_at:
                    next_due[sampling] += intervals[sampling] * thermal_factor
            if retention_days > 0 and time.monotonic() >= next_cleanup:
                cutoff = (datetime.now(timezone.utc) - timedelta(days=retention_days)).isoformat(timespec="milliseconds")
                deleted_samples, deleted_cycles = database.prune_before(cutoff)
                if deleted_samples or deleted_cycles:
                    LOG.info(
                        "retention cleanup: deleted %d samples and %d cycles older than %s",
                        deleted_samples,
                        deleted_cycles,
                        cutoff,
                    )
                next_cleanup = time.monotonic() + cleanup_interval
            if any_samples and time.monotonic() >= next_status_log:
                LOG.info("poll complete: %d values, %d errors", len(displayed_samples), len(all_errors))
                next_status_log = time.monotonic() + 60.0
            if once:
                for device, register, raw in displayed_samples:
                    print(f"{device.name}.{register.key}=0x{raw:04X} ({raw * register.scale:g} {register.unit})")
                return 1 if all_errors else 0
            wake_at = min([*next_due.values()] or [time.monotonic() + reconnect_delay])
            delay = reconnect_delay if not any_samples else max(0.0, wake_at - time.monotonic())
            stop.wait(delay)
    finally:
        stop.set()
        for thread in addon_threads:
            thread.join(timeout=5.0)
        for collector in collectors.values():
            collector.close()
        database.close()
        LOG.info("collector stopped")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--once", action="store_true", help="poll once and exit")
    parser.add_argument("--log-level", default="INFO", choices=("DEBUG", "INFO", "WARNING", "ERROR"))
    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level), format="%(asctime)s %(levelname)s %(message)s")
    try:
        settings = load_config(args.config)
        settings["_config_path"] = str(args.config)
        bridge = settings.get("communication_bridge", {})
        if isinstance(bridge, dict) and bridge.get("enabled", False):
            if args.once:
                LOG.info("proxy one-shot mode waits for one upstream transaction")
            from tmm_proxy import run_proxy
            # A proxy-only first start must still create the common schema used
            # by the web application before the dedicated frame table is added.
            database = Database(
                Path(settings["storage"]["database"]),
                settings["storage"].get("change_logging"),
                str(settings.get("recording", {}).get("reference", "")).strip(),
                condition_rules(settings),
            )
            database.close()
            stop = threading.Event()
            addon_threads: list[threading.Thread] = []
            administration_thread: threading.Thread | None = None
            if not args.once:
                signal.signal(signal.SIGTERM, lambda *_: stop.set())
                signal.signal(signal.SIGINT, lambda *_: stop.set())
                addon_threads = start_addon_collectors(
                    settings, Path(settings["storage"]["database"]), stop
                )
                administration_thread = threading.Thread(
                    target=run_proxy_administration,
                    args=(settings, stop),
                    name="tmm-proxy-administration", daemon=True,
                )
                administration_thread.start()
            try:
                return run_proxy(settings, stop, once=args.once)
            finally:
                stop.set()
                for thread in addon_threads:
                    thread.join(timeout=5.0)
                if administration_thread is not None:
                    administration_thread.join(timeout=10.0)
        return run(settings, once=args.once)
    except PortRecoveryRequired as error:
        LOG.error("serial recovery required: %s", error)
        return 75
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        LOG.error("startup failed: %s", error)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
