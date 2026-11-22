#!/usr/bin/env python3
"""Web API and dashboard for Toshiba Modbus Monitor (TMM)."""

from __future__ import annotations

import argparse
import base64
import binascii
import csv
import io
import hashlib
import json
import re
import shutil
import sqlite3
import os
import tempfile
import statistics
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Annotated, Any

import uvicorn
try:
    import psutil
except ImportError:  # pragma: no cover - useful for a minimal development host
    psutil = None  # type: ignore[assignment]
from fastapi import Body, FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from tmm_decode import enrich_sample, terminal_history_items
from tmm_conditions import OPERATORS, condition_rules
from tmm_addons import AddonConfigurationError, MULTIIO_INPUTS, SYSTEM_ADDON_METRICS, addon_metadata, configured_addons, normalize_fan_control
from tmm_monitor import configured_devices, parameter_backup_files, parameter_safety_class, parse_pcm_template, pcm_template_matches_model
from tmm_profiles import profile
from tmm_proxy import configured_endpoint_status, crc16
from tmm_web_data import MonitorRepository

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
README_PATH = APP_DIR / "README.md"
APP_VERSION = ((APP_DIR / "VERSION").read_text(encoding="utf-8").strip() or "1.3.0")

SUPPORTED_ADDON_VISUALS = (
    ("raspberry_pi_gpio", "pi_gpio", "Raspberry Pi GPIO terminal HAT", "field", "Digital GPIO inputs"),
    ("sequent_16inpind", "field_di", "16 LV Digital Inputs", "field", "16 isolated digital inputs"),
    ("sequent_24b8vin", "field_ai", "8 x 24-Bit Analog Inputs DAQ", "field", "8 high-resolution analog inputs"),
    ("sequent_multiio", "field_multiio", "Multi-IO", "field", "Digital, voltage, current and temperature inputs"),
    ("sequent_smart_fan", "system_fan", "Smart Fan", "system", "System cooling and processor temperature"),
    ("sequent_super_watchdog", "system_ups", "Super Watchdog & UPS", "system", "Power, battery and watchdog monitoring"),
)

DEFAULT_ALERT_THRESHOLDS = {
    "system": {
        "cpu_percent": {"warning": 80, "critical": 95},
        "temperature_celsius": {"warning": 70, "critical": 80},
        "memory_percent": {"warning": 85, "critical": 95},
        "disk_percent": {"warning": 85, "critical": 95},
    },
    "metrics": {
        "output_current": {"warning": 90, "critical": 110},
        "dc_input_voltage": {"warning": 110, "critical": 120},
        "braking_resistor_load": {"warning": 70, "critical": 90},
        "inverter_internal_temperature": {"warning": 70, "critical": 85},
        "power_board_temperature": {"warning": 80, "critical": 95},
    },
}

# Derived channels are only meaningful while their source monitor is enabled.
DERIVED_CHANNEL_SOURCES = {
    "machine_speed": "calculated_motor_speed",
    "actual_output_current": "output_current",
    "actual_output_voltage": "output_voltage",
    "actual_motor_torque": "torque",
    "mechanical_power": "torque",
    "terminal_f": "input_terminal_status",
    "terminal_r": "input_terminal_status",
    "terminal_s1": "input_terminal_status",
    "terminal_s2": "input_terminal_status",
    "terminal_s3": "input_terminal_status",
}


COMMUNICATION_METRICS = {
    "communication.samples_per_second": ("Samples per second", "samples/s"),
    "communication.average_cycle_ms": ("Average cycle time", "ms"),
    "communication.maximum_cycle_ms": ("Maximum cycle time", "ms"),
    "communication.bus_utilization_percent": ("Bus utilization", "%"),
    "communication.retries": ("Retries per minute", "count"),
    "communication.success_percent": ("Successful reads", "%"),
}

DASHBOARD_SECTION_IDS = (
    "device-info-title", "alerts-title", "live-title", "addons-title", "ups-title",
    "history-title", "conditions-title", "fault-title", "storage-title", "recording-title", "comm-title", "bridge-title",
    "engineering-title", "parameter-backup-title", "parameter-preview-title",
)

def communication_bridge_status(config: dict[str, Any]) -> dict[str, Any]:
    """Describe configured bridge readiness without touching serial ports."""
    bridge = config.get("communication_bridge", {})
    if not isinstance(bridge, dict):
        bridge = {}
    scheduled_settings = bridge.get("scheduled_polling", {})
    if not isinstance(scheduled_settings, dict):
        scheduled_settings = {}
    scheduled_requested = bool(bridge.get("enabled", False) and scheduled_settings.get("enabled", False))
    # Production-safe proxy mode currently suppresses injected TMM requests.
    scheduled_enabled = False
    endpoints, missing_adapters, checks = configured_endpoint_status(bridge)
    enabled = bool(bridge.get("enabled", False))
    heartbeat = Path("/run/tmm/proxy-active")
    runtime_state = "offline" if enabled else "disabled"
    runtime_error = ""
    wiring_diagnostic: dict[str, Any] | None = None
    runtime_diagnostics: dict[str, Any] = {}
    try:
        status = json.loads(Path("/run/tmm/proxy-status.json").read_text(encoding="utf-8"))
        if isinstance(status, dict):
            runtime_state = str(status.get("state", runtime_state))
            runtime_error = str(status.get("error", ""))
            wiring = status.get("wiring")
            if isinstance(wiring, dict):
                wiring_diagnostic = wiring
            diagnostics = status.get("diagnostics")
            if isinstance(diagnostics, dict):
                runtime_diagnostics = diagnostics
    except (OSError, json.JSONDecodeError):
        pass
    try:
        runtime_active = enabled and heartbeat.is_file() and time.time() - heartbeat.stat().st_mtime < 5.0
    except OSError:
        runtime_active = False
    if runtime_active:
        runtime_state = "active"
    return {
        "implementation_stage": "transparent_proxy" if enabled else "design",
        "active_phase": "scheduled_polling" if scheduled_enabled else "transparent_proxy" if enabled else "passive_observer",
        "enabled": enabled,
        "runtime_active": runtime_active,
        "runtime_state": runtime_state,
        "runtime_error": runtime_error,
        "wiring_diagnostic": wiring_diagnostic,
        "runtime_diagnostics": runtime_diagnostics,
        "scheduled_polling": {
            "enabled": scheduled_enabled,
            "requested": scheduled_requested,
            "suppressed_for_hmi_priority": scheduled_requested,
            "passive_decode": bool(scheduled_settings.get("passive_decode", True)),
            "idle_guard_seconds": float(scheduled_settings.get("idle_guard_seconds", 0.02)),
            "response_timeout_seconds": float(scheduled_settings.get("response_timeout_seconds", 0.1)),
            "minimum_gap_seconds": float(scheduled_settings.get("minimum_gap_seconds", 0.02)),
        },
        "missing_adapters": missing_adapters,
        "requested_mode": str(bridge.get("mode", "transparent_proxy")),
        "endpoints": endpoints,
        "checks": checks,
        "phases": ["passive_observer", "transparent_proxy", "scheduled_polling"],
        "capabilities": ["frames", "latency", "exceptions", "crc_errors", "register_activity", "write_audit"],
    }

def configured_alert_thresholds(config: dict[str, Any]) -> dict[str, Any]:
    result = {section: {key: dict(value) for key, value in values.items()} for section, values in DEFAULT_ALERT_THRESHOLDS.items()}
    for section in ("system", "metrics"):
        for key, values in config.get("alerts", {}).get(section, {}).items():
            if values is None:
                result[section].pop(key, None)
                continue
            merged = dict(result[section].get(key, {})); merged.update(values)
            warning = float(merged["warning"]); critical = float(merged["critical"])
            if warning >= critical:
                raise ValueError(f"alert threshold {section}.{key}: warning must be below critical")
            normalized = {"warning": warning, "critical": critical}
            if "warning_low" in merged or "critical_low" in merged:
                if "warning_low" not in merged or "critical_low" not in merged:
                    raise ValueError(f"alert threshold {section}.{key}: warning_low and critical_low must be configured together")
                warning_low = float(merged["warning_low"]); critical_low = float(merged["critical_low"])
                if critical_low >= warning_low:
                    raise ValueError(f"alert threshold {section}.{key}: critical_low must be below warning_low")
                normalized.update({"warning_low": warning_low, "critical_low": critical_low})
            result[section][key] = normalized
    return result


def load_settings(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_timestamp(value: datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        raise HTTPException(422, "timestamps must include a timezone, for example Z or +01:00")
    return value.astimezone(timezone.utc).isoformat(timespec="milliseconds")


def parse_pcm_csv_limits(content: str) -> dict[int, tuple[int, int]]:
    rows = csv.DictReader(io.StringIO(content))
    result = {}
    for row in rows:
        try:
            address = int(str(row["Comm. No."]).strip(), 16)
            unit = str(row["Unit"]).strip()
            scale_match = re.match(r"([0-9]+(?:\.[0-9]+)?)", unit)
            scale = float(scale_match.group(1)) if scale_match else 1.0
            minimum = round(float(str(row["Low limit."]).strip()) / scale)
            maximum = round(float(str(row["Up limit."]).strip()) / scale)
        except (KeyError, TypeError, ValueError):
            continue
        if 0 <= minimum <= maximum <= 0xFFFF:
            result[address] = (minimum, maximum)
    if not result:
        raise ValueError("no usable PCM002Z CSV limits found")
    return result


def parameter_backup_age_seconds(path: Path) -> int:
    return max(0, int(datetime.now(timezone.utc).timestamp() - path.stat().st_mtime))


def system_metrics(database: Path, previous_cpu: list[Any]) -> dict[str, Any]:
    """Return portable host metrics; unavailable sensors remain null."""
    if psutil is None:
        disk = shutil.disk_usage(database.parent)
        memory_total = memory_available = 0
        try:
            fields = dict(
                line.split(":", 1) for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines()
                if ":" in line
            )
            memory_total = int(fields.get("MemTotal", "0").split()[0]) * 1024
            memory_available = int(fields.get("MemAvailable", fields.get("MemFree", "0")).split()[0]) * 1024
        except (OSError, ValueError):
            pass
        temperature = None
        for sensor in Path("/sys/class/thermal").glob("thermal_zone*/temp"):
            try:
                temperature = max(temperature or float("-inf"), int(sensor.read_text().strip()) / 1000)
            except (OSError, ValueError):
                continue
        try:
            load_average = list(os.getloadavg())
        except OSError:
            load_average = []
        return {
            "cpu_percent": None,
            "memory_percent": round(100.0 * (memory_total - memory_available) / memory_total, 2) if memory_total else None,
            "memory_used_bytes": memory_total - memory_available if memory_total else None,
            "memory_total_bytes": memory_total or None,
            "disk_percent": round(100.0 * disk.used / disk.total, 2),
            "disk_free_bytes": disk.free,
            "disk_total_bytes": disk.total,
            "temperature_celsius": temperature,
            "load_average": load_average,
        }
    cpu_percent = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory()
    disk = shutil.disk_usage(database.parent)
    temperature = None
    try:
        groups = psutil.sensors_temperatures()
        readings = [item.current for group in groups.values() for item in group if item.current is not None]
        temperature = max(readings) if readings else None
    except (AttributeError, OSError):
        pass
    try:
        load_average = list(psutil.getloadavg())
    except (AttributeError, OSError):
        load_average = []
    return {
        "cpu_percent": round(max(0.0, min(100.0, cpu_percent)), 2),
        "memory_percent": round(memory.percent, 2),
        "memory_used_bytes": memory.used,
        "memory_total_bytes": memory.total,
        "disk_percent": round(100.0 * disk.used / disk.total, 2),
        "disk_free_bytes": disk.free,
        "disk_total_bytes": disk.total,
        "temperature_celsius": temperature,
        "load_average": load_average,
    }


def create_app(config_path: Path) -> FastAPI:
    config = load_settings(config_path)
    repository = MonitorRepository(Path(config["storage"]["database"]))
    devices = configured_devices(config)
    device_by_name = {device.name: device for device in devices}
    stale_after = float(config.get("web", {}).get("stale_after_seconds", 10))
    export_max_rows = int(config["storage"].get("export_max_rows", 250000))
    previous_cpu: list[Any] = []
    live_snapshot_lock = Lock()
    live_snapshot: dict[str, Any] = {"created_at": 0.0, "latest": [], "cycles": []}
    diagnostics_lock = Lock()
    diagnostics_snapshot: dict[str, Any] = {"created_at": 0.0, "value": {}}
    ups_estimate_lock = Lock()
    ups_estimate_cache: dict[str, tuple[float, tuple[bool, int | None], dict[str, Any] | None]] = {}
    alert_thresholds = configured_alert_thresholds(config)
    app = FastAPI(
        title="Toshiba Modbus Monitor API",
        version=APP_VERSION,
        description="Monitoring and guarded service access for Toshiba inverter installations.",
    )

    @app.middleware("http")
    async def prevent_stale_dashboard_assets(request: Request, call_next: Any) -> Any:
        """Force browsers and intervening proxies to revalidate the dashboard shell."""
        response = await call_next(request)
        if request.url.path in {"/", "/static/index.html", "/static/app.js", "/static/style.css"}:
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        return response

    def current_live_snapshot() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Share the current SQLite snapshot across one dashboard refresh.

        The browser asks health, current measurements and add-on data in
        parallel.  Those endpoints used to independently read the same two
        tables every three seconds.  A one-second cache is shorter than the
        dashboard cadence, but collapses those concurrent reads to one.
        """
        with live_snapshot_lock:
            now = time.monotonic()
            if now - float(live_snapshot["created_at"]) >= 1.0:
                live_snapshot["latest"] = repository.latest_samples()
                live_snapshot["cycles"] = repository.last_cycles()
                live_snapshot["created_at"] = now
            return list(live_snapshot["latest"]), list(live_snapshot["cycles"])

    def current_diagnostics() -> dict[str, Any]:
        """Host sensors need not be sampled more often than once per 5 s."""
        with diagnostics_lock:
            now = time.monotonic()
            if now - float(diagnostics_snapshot["created_at"]) >= 5.0:
                proxy_mode = bool(load_settings(config_path).get("communication_bridge", {}).get("enabled", False))
                diagnostics_snapshot["value"] = {
                    "mode": "transparent_proxy" if proxy_mode else "polling",
                    "communication": repository.communication_diagnostics(60) if not proxy_mode else None,
                    "proxy": repository.proxy_diagnostics(60) if proxy_mode else None,
                    "system": system_metrics(Path(config["storage"]["database"]), previous_cpu),
                    "thermal_protection": repository.thermal_protection(),
                    "inverter_cpu_percent": None,
                }
                diagnostics_snapshot["created_at"] = now
            return dict(diagnostics_snapshot["value"])

    def active_metrics() -> dict[str, set[str]]:
        """Return metrics which belong to the currently enabled channels.

        `latest_values` intentionally retains the last sample for each metric.
        Filtering it here makes a channel switched Off disappear immediately,
        without deleting its useful historical data.
        """
        result = {
            device.name: {register.key for register in device.registers}
            for device in configured_devices(load_settings(config_path))
        }
        for name, metrics in result.items():
            for derived, source in DERIVED_CHANNEL_SOURCES.items():
                if source in metrics:
                    metrics.add(derived)
            # This synthetic state is needed to explain an unavailable drive;
            # it is not a user-selectable Modbus channel.
            metrics.add("communication_status")
        return result

    def active_addon_sources() -> dict[str, int]:
        """Map each configured add-on source to its current pseudo slave ID.

        An add-on's stack address is part of its identity.  Keeping it in the
        filter prevents values or errors left over from a previous stack
        assignment from reappearing in the history selector.
        """
        return {
            definition.source_name: -(definition.stack + 1)
            for definition in configured_addons(load_settings(config_path))
            if definition.enabled
        }

    def is_active_sample(item: dict[str, Any], enabled: dict[str, set[str]], addon_sources: dict[str, int]) -> bool:
        source = item["inverter"]
        if source in addon_sources:
            return item["slave_id"] == addon_sources[source]
        return item["metric"] in enabled.get(source, set())

    def is_known_historical_sample(item: dict[str, Any], addon_sources: dict[str, int]) -> bool:
        """Allow retained trends for configured drives, including disabled channels."""
        source = item["inverter"]
        if source in addon_sources:
            return item["slave_id"] == addon_sources[source]
        return source in device_by_name

    def effective_addon_channels(definition: Any) -> list[dict[str, Any]]:
        """Expose every physical DI/AI point, including points with defaults."""
        # System cards describe named measurements (for example
        # ``battery_voltage``), not numbered field channels.  They must not
        # enter the field-I/O normalisation below.
        if definition.kind in SYSTEM_ADDON_METRICS:
            configured = {str(item.get("metric", "")): dict(item) for item in definition.channels}
            default = {"enabled": False, "record": False, "live": False}
            return [
                {
                    **default,
                    **configured.get(metric, {}),
                    "metric": metric,
                    "metric_label": label,
                    "unit": unit,
                }
                for metric, (label, unit) in SYSTEM_ADDON_METRICS[definition.kind].items()
            ]
        if definition.kind not in {"raspberry_pi_gpio", "sequent_16inpind", "sequent_24b8vin", "sequent_multiio"}:
            return [dict(channel) for channel in definition.channels]
        configured = {(str(item.get("signal", "input")), int(item["channel"])): dict(item) for item in definition.channels}
        if definition.kind == "raspberry_pi_gpio":
            keys = list(configured)
        elif definition.kind == "sequent_16inpind":
            keys = [("input", number) for number in range(1, 17)]
        elif definition.kind == "sequent_24b8vin":
            keys = [("input", number) for number in range(1, 9)]
        else:
            keys = list(configured)
        default = {"enabled": False, "record": False, "live": False}
        return [{**default, **configured.get(key, {}), "signal": key[0], "channel": key[1]} for key in keys]

    def addon_sample_is_live(definition: Any, item: dict[str, Any]) -> bool:
        """Apply an add-on channel's live-card choice to retained samples."""
        if definition.kind not in {"raspberry_pi_gpio", "sequent_16inpind", "sequent_24b8vin", "sequent_multiio"}:
            return True
        leaf = str(item.get("metric", "")).rsplit(".", 1)[-1]
        match = re.fullmatch(r"(.+)_(\d+)", leaf)
        if match is None:
            return False
        signal, number = match.group(1), int(match.group(2))
        channels = {(str(channel.get("signal", "input")), int(channel["channel"])): channel
                    for channel in effective_addon_channels(definition)}
        channel = channels.get((signal, number)) or channels.get(("input", number))
        return channel is not None and channel.get("enabled", True) and channel.get("live", True)

    def ups_shutdown_policy() -> dict[str, Any]:
        policy = dict(load_settings(config_path).get("ups_shutdown", {}))
        override_path = Path(config["storage"]["database"]).parent / "ups-shutdown-policy.json"
        try:
            override = json.loads(override_path.read_text(encoding="utf-8"))
            if isinstance(override, dict): policy.update(override)
        except (OSError, json.JSONDecodeError):
            pass
        return {"input_loss_delay_seconds": float(policy.get("input_loss_delay_seconds", 30))}

    def fan_control_policy(definition: Any) -> dict[str, Any]:
        policy = dict(definition.options.get("control", {}))
        path = Path(config["storage"]["database"]).parent / "smart-fan-policy.json"
        try:
            overrides = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(overrides, dict) and isinstance(overrides.get(definition.identifier), dict):
                policy.update(overrides[definition.identifier])
        except (OSError, json.JSONDecodeError):
            pass
        return normalize_fan_control(policy)

    def ups_estimate(definition: Any, values: list[dict[str, Any]]) -> dict[str, Any] | None:
        """Estimate remaining UPS runtime from the measured discharge slope.

        The board exposes voltage, not battery current/capacity.  This estimate
        therefore remains intentionally conservative and is omitted until a
        real battery-discharge segment has supplied enough samples.
        """
        source = definition.source_name
        leaf = lambda name: next((item for item in values if item["metric"].endswith(f".{name}")), None)
        input_value, battery_value, charge_value = leaf("input_voltage"), leaf("battery_voltage"), leaf("charge_status")
        if not input_value or not battery_value:
            return None
        addon_config = next((item for item in load_settings(config_path).get("addons", []) if item.get("id") == definition.identifier), {})
        threshold = float(addon_config.get("input_loss_threshold_v", 4.5))
        cutoff = float(addon_config.get("battery_shutdown_voltage_v", 3.05))
        full = float(addon_config.get("battery_full_voltage_v", 4.15))
        on_mains = float(input_value["value"]) >= threshold
        input_history = repository.recent_history(f"addon.{definition.identifier}.input_voltage", source)
        boundary = next((row["observed_at"] for row in reversed(input_history) if (float(row["value"]) < threshold) == on_mains), None)
        battery_history = repository.recent_history(f"addon.{definition.identifier}.battery_voltage", source)
        if boundary:
            battery_history = [row for row in battery_history if row["observed_at"] > boundary]
        mode = "charge" if on_mains and charge_value and round(float(charge_value["value"])) == 2 else "discharge"
        if on_mains and mode != "charge":
            return {"state": "mains", "battery_voltage": battery_value["value"], "cutoff_voltage": cutoff}
        if len(battery_history) < 30:
            return {"state": "charge_learning" if mode == "charge" else "learning", "battery_voltage": battery_value["value"], "cutoff_voltage": cutoff, "samples": len(battery_history)}
        origin = datetime.fromisoformat(battery_history[0]["observed_at"].replace("Z", "+00:00"))
        x = [(datetime.fromisoformat(row["observed_at"].replace("Z", "+00:00")) - origin).total_seconds() for row in battery_history]
        y = [float(row["value"]) for row in battery_history]
        mean_x, mean_y = statistics.fmean(x), statistics.fmean(y)
        denominator = sum((item - mean_x) ** 2 for item in x)
        slope = sum((left - mean_x) * (right - mean_y) for left, right in zip(x, y)) / denominator if denominator else 0.0
        voltage = float(battery_value["value"])
        if mode == "charge":
            if slope <= 0.000001 or voltage >= full:
                return {"state": "charge_learning", "battery_voltage": voltage, "full_voltage": full, "samples": len(y)}
            remaining = max(0, int((full - voltage) / slope))
            return {"state": "charge_estimated", "battery_voltage": voltage, "full_voltage": full, "samples": len(y), "remaining_seconds": remaining, "charge_volts_per_hour": round(slope * 3600, 3)}
        if slope >= -0.000001 or voltage <= cutoff:
            return {"state": "learning", "battery_voltage": voltage, "cutoff_voltage": cutoff, "samples": len(y)}
        remaining = max(0, int((voltage - cutoff) / -slope))
        return {"state": "estimated", "battery_voltage": voltage, "cutoff_voltage": cutoff, "samples": len(y), "remaining_seconds": remaining, "discharge_volts_per_hour": round(-slope * 3600, 3)}

    def cached_ups_estimate(definition: Any, values: list[dict[str, Any]]) -> dict[str, Any] | None:
        """Keep the expensive historical slope calculation off the live path.

        The estimator loads two windows of up to 3,600 samples and performs a
        regression.  Battery runtime evolves far more slowly than the three
        second dashboard cadence; a short cache preserves useful feedback
        while avoiding repeated historical scans and datetime parsing.
        """
        with ups_estimate_lock:
            now = time.monotonic()
            current = {str(item.get("metric", "")).rsplit(".", 1)[-1]: item for item in values}
            addon_config = next((item for item in load_settings(config_path).get("addons", []) if item.get("id") == definition.identifier), {})
            threshold = float(addon_config.get("input_loss_threshold_v", 4.5))
            input_value = current.get("input_voltage")
            charge_value = current.get("charge_status")
            # Do not delay a change between mains and battery operation, or a
            # charge-state transition; both are safety-relevant UI states.
            signature = (
                bool(input_value and float(input_value.get("value", 0)) >= threshold),
                round(float(charge_value.get("value", 0))) if charge_value else None,
            )
            cached = ups_estimate_cache.get(definition.identifier)
            if cached and cached[1] == signature and now - cached[0] < 30.0:
                return cached[2]
            estimate = ups_estimate(definition, values)
            ups_estimate_cache[definition.identifier] = (now, signature, estimate)
            return estimate

    def require_local_administration(request: Request) -> None:
        client = request.client.host if request.client else ""
        allow_remote = bool(config.get("web", {}).get("allow_remote_administration", False))
        if not allow_remote and client not in {"127.0.0.1", "::1"}:
            raise HTTPException(403, "administration is restricted to localhost")

    @app.get("/api/v1/health")
    def health() -> dict[str, Any]:
        current_settings = load_settings(config_path)
        if bool(current_settings.get("communication_bridge", {}).get("enabled", False)):
            proxy = repository.proxy_diagnostics(60)
            bridge_status = communication_bridge_status(current_settings)
            return {"status": "healthy" if bridge_status["runtime_active"] else "unavailable",
                    "database": True, "mode": "transparent_proxy", "proxy": proxy,
                    "runtime_active": bridge_status["runtime_active"], "devices": []}
        try:
            _, cycles = current_live_snapshot()
        except (FileNotFoundError, sqlite3.Error) as error:
            return {"status": "unavailable", "database": False, "detail": str(error)}
        if not cycles:
            return {"status": "starting", "database": True, "devices": []}
        device_states = []
        for cycle in cycles:
            # Add-on health has its own dashboard area.  It must not make the
            # Toshiba connection badge appear offline.
            if cycle["inverter"] not in device_by_name:
                continue
            observed = datetime.fromisoformat(cycle["observed_at"].replace("Z", "+00:00"))
            age = max(0.0, (datetime.now(timezone.utc) - observed).total_seconds())
            if age > stale_after:
                device_status = "stale"
            elif cycle["failed_reads"]:
                device_status = "degraded"
            else:
                device_status = "healthy"
            device_states.append({"status": device_status, "age_seconds": round(age, 3), **cycle})
        if not device_states:
            return {"status": "starting", "database": True, "devices": []}
        statuses = {item["status"] for item in device_states}
        status = "stale" if "stale" in statuses else "degraded" if "degraded" in statuses else "healthy"
        return {
            "status": status,
            "database": True,
            "age_seconds": max(item["age_seconds"] for item in device_states),
            "stale_after_seconds": stale_after,
            "last_cycle": max(device_states, key=lambda item: item["id"]),
            "devices": device_states,
        }

    @app.get("/api/v1/metadata")
    def metadata() -> dict[str, Any]:
        current_settings = load_settings(config_path)
        enabled = active_metrics()
        addon_sources = active_addon_sources()
        return {
            "product": "Toshiba Modbus Monitor",
            "short_name": "TMM",
            "version": APP_VERSION,
            "contact": config.get("product", {}),
            "inverters": [
                {"name": device.name, "model": device.model, "slave_id": device.slave_id}
                for device in devices
            ],
            "poll_interval_seconds": config["polling"]["interval_seconds"],
            "metrics": sorted({
                item["metric"]
                for item in repository.latest_samples()
                if is_active_sample(item, enabled, addon_sources)
            }),
            "retention_days": float(config["storage"].get("retention_days", 0)),
            "alert_thresholds": alert_thresholds,
            "addons": addon_metadata(configured_addons(config)),
            "communication_bridge": communication_bridge_status(current_settings),
        }

    @app.get("/api/v1/addons")
    def addons() -> dict[str, Any]:
        definitions = configured_addons(load_settings(config_path))
        order_path = Path(config["storage"]["database"]).parent / "addon-live-order.json"
        try:
            saved_orders = json.loads(order_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            saved_orders = {}
        known = {item.source_name: item for item in definitions}
        current_values, current_cycles = current_live_snapshot()
        values = [item for item in current_values if item["inverter"] in known]
        cycles = {(item["inverter"], item["slave_id"]): item
                  for item in current_cycles if item["inverter"] in known}
        items = [
            {
                "id": definition.identifier, "type": definition.kind,
                "label": definition.label, "stack": definition.stack,
                "configured": True,
                "enabled": definition.enabled,
                "interval_seconds": definition.interval_seconds,
                "live_order": saved_orders.get(definition.identifier, []),
                "channels": effective_addon_channels(definition),
                # Stack changes intentionally preserve history.  The live card
                # must nevertheless use only the currently configured pseudo
                # slave ID; otherwise an old card error could override a newer
                # successful cycle from the same add-on name.
                "values": [item for item in values if definition.enabled and item["inverter"] == source and item["slave_id"] == -(definition.stack + 1) and addon_sample_is_live(definition, item)],
                "health": cycles.get((source, -(definition.stack + 1))) if definition.enabled else None,
                "battery_estimate": cached_ups_estimate(definition, [item for item in values if item["inverter"] == source and item["slave_id"] == -(definition.stack + 1)]) if definition.kind == "sequent_super_watchdog" else None,
                "fan_control": fan_control_policy(definition) if definition.kind == "sequent_smart_fan" else None,
            }
            for source, definition in known.items()
        ]
        configured_types = {definition.kind for definition in definitions}
        items.extend({
            "id": identifier, "type": kind, "label": label, "stack": None,
            "configured": False, "enabled": False, "interval_seconds": None,
            "live_order": [], "channels": [], "values": [], "health": None,
            "battery_estimate": None, "fan_control": None,
            "catalog_group": group, "capability_summary": capability,
        } for kind, identifier, label, group, capability in SUPPORTED_ADDON_VISUALS if kind not in configured_types)
        return {"items": items, "ups_shutdown": ups_shutdown_policy()}

    @app.post("/api/v1/addons/enabled", status_code=202)
    def update_addon_enabled(request: Request, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
        """Enable or suspend polling of one external I/O card."""
        require_local_administration(request)
        identifier = str(payload.get("id", ""))
        enabled = payload.get("enabled")
        if not isinstance(enabled, bool):
            raise HTTPException(422, "enabled must be a boolean")
        settings = load_settings(config_path)
        target = next((item for item in settings.get("addons", []) if str(item.get("id")) == identifier), None)
        if target is None:
            raise HTTPException(404, "unknown add-on")
        if str(target.get("type", "")) in SYSTEM_ADDON_METRICS:
            raise HTTPException(422, "system add-ons cannot be disabled here")
        target["enabled"] = enabled
        configured_addons(settings)
        temporary = config_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.chmod(temporary, 0o660)
        os.replace(temporary, config_path)
        return {"status": "accepted", "id": identifier, "enabled": enabled}

    @app.post("/api/v1/fans/control-policy", status_code=202)
    def update_fan_control_policy(request: Request, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
        require_local_administration(request)
        identifier = str(payload.get("id", ""))
        definition = next((item for item in configured_addons(load_settings(config_path))
                           if item.identifier == identifier and item.kind == "sequent_smart_fan"), None)
        if definition is None:
            raise HTTPException(404, "unknown Smart Fan")
        control = payload.get("control")
        if not isinstance(control, dict):
            raise HTTPException(422, "control must be an object")
        try:
            normalized = normalize_fan_control(control)
        except (AddonConfigurationError, ValueError) as error:
            raise HTTPException(422, str(error)) from error
        path = Path(config["storage"]["database"]).parent / "smart-fan-policy.json"
        try:
            policies = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            policies = {}
        policies[identifier] = normalized
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(policies, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temporary, path)
        return {"status": "accepted", "id": identifier, "control": normalized}

    @app.post("/api/v1/ups/shutdown-policy", status_code=202)
    def update_ups_shutdown_policy(request: Request, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
        require_local_administration(request)
        try:
            delay = float(payload["input_loss_delay_seconds"])
        except (KeyError, TypeError, ValueError):
            raise HTTPException(422, "input_loss_delay_seconds must be a number")
        if not 1 <= delay <= 86400:
            raise HTTPException(422, "input_loss_delay_seconds must be between 1 and 86400")
        path = Path(config["storage"]["database"]).parent / "ups-shutdown-policy.json"
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps({"input_loss_delay_seconds": delay}) + "\n", encoding="utf-8")
        os.replace(temporary, path)
        return {"status": "accepted", "input_loss_delay_seconds": delay}

    @app.post("/api/v1/addons/order", status_code=202)
    def update_addon_order(request: Request, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
        require_local_administration(request)
        identifier = str(payload.get("id", ""))
        order = payload.get("order")
        if not isinstance(order, list) or any(not isinstance(item, str) or len(item) > 120 for item in order):
            raise HTTPException(422, "order must be a list of metric names")
        if len(set(order)) != len(order):
            raise HTTPException(422, "order contains duplicates")
        if identifier not in {item.identifier for item in configured_addons(load_settings(config_path))}:
            raise HTTPException(404, "unknown add-on")
        order_path = Path(config["storage"]["database"]).parent / "addon-live-order.json"
        try:
            saved_orders = json.loads(order_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            saved_orders = {}
        saved_orders[identifier] = order
        temporary = order_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(saved_orders, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temporary, order_path)
        return {"status": "accepted", "id": identifier}

    @app.post("/api/v1/addons/channels", status_code=202)
    def update_addon_channels(request: Request, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
        """Apply operator-facing names, scaling and history selection to one card."""
        require_local_administration(request)
        identifier = str(payload.get("id", ""))
        requested = payload.get("channels")
        if not isinstance(requested, list):
            raise HTTPException(422, "channels must be a list")
        settings = load_settings(config_path)
        target = next((item for item in settings.get("addons", []) if str(item.get("id")) == identifier), None)
        if target is None:
            raise HTTPException(404, "unknown add-on")
        existing = {(str(item.get("signal", "input")), int(item.get("channel", 0))): item for item in target.get("channels", [])}
        kind = str(target.get("type", ""))
        if kind in SYSTEM_ADDON_METRICS:
            configured = {str(item.get("metric", "")): item for item in target.get("channels", [])}
            for item in requested:
                if not isinstance(item, dict):
                    raise HTTPException(422, "invalid channel")
                metric = str(item.get("metric", ""))
                if metric not in SYSTEM_ADDON_METRICS[kind]:
                    raise HTTPException(422, "unknown system metric")
                update = configured.setdefault(metric, {"metric": metric})
                mode = item.get("mode")
                if mode not in {"off", "live", "record", "hide"}:
                    raise HTTPException(422, "system metric mode must be off, live, record, or hide")
                update.update({"enabled": mode != "off", "record": mode in {"record", "hide"}, "live": mode != "hide"})
            target["channels"] = list(configured.values())
            configured_addons(settings)
            temporary = config_path.with_suffix(".tmp")
            temporary.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            os.chmod(temporary, 0o660)
            os.replace(temporary, config_path)
            return {"status": "accepted", "id": identifier}
        for item in requested:
            if not isinstance(item, dict):
                raise HTTPException(422, "invalid channel")
            key = (str(item.get("signal", "input")), int(item.get("channel", 0)))
            maximum = 27 if kind == "raspberry_pi_gpio" else 16 if kind == "sequent_16inpind" else 8 if kind == "sequent_24b8vin" else MULTIIO_INPUTS.get(key[0], (0,))[0]
            minimum = 2 if kind == "raspberry_pi_gpio" else 1
            if not minimum <= key[1] <= maximum or (kind == "sequent_multiio" and key[0] not in MULTIIO_INPUTS):
                raise HTTPException(422, "unknown add-on channel")
            update = existing.setdefault(key, {"channel": key[1], **({"signal": key[0]} if kind == "sequent_multiio" else {})})
            for field in ("label", "unit"):
                if field in item:
                    update[field] = str(item[field]).strip()
            mode = item.get("mode")
            if mode is not None:
                if mode not in {"off", "live", "record", "hide"}:
                    raise HTTPException(422, "add-on channel mode must be off, live, record, or hide")
                update.update({
                    "enabled": mode != "off",
                    "record": mode in {"record", "hide"},
                    "live": mode != "hide",
                })
            for field in ("enabled", "record", "live"):
                if field in item:
                    update[field] = bool(item[field])
            if kind == "raspberry_pi_gpio":
                if "pull" in item:
                    update["pull"] = str(item["pull"]).strip().lower()
                if "active_low" in item:
                    update["active_low"] = bool(item["active_low"])
            for field in ("scale", "offset"):
                if field in item:
                    update[field] = float(item[field])
            if "decimals" in item:
                update["decimals"] = int(item["decimals"])
            if "change_threshold" in item:
                update["change_threshold"] = float(item["change_threshold"])
        target["channels"] = list(existing.values())
        # Reuse the collector's strict validation before replacing config.json.
        configured_addons(settings)
        temporary = config_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        # The web worker owns this configuration so it can atomically replace
        # it.  Do not let the process umask turn the replacement world-readable.
        os.chmod(temporary, 0o660)
        os.replace(temporary, config_path)
        return {"status": "accepted", "id": identifier}

    @app.get("/api/v1/storage")
    def storage() -> dict[str, Any]:
        data = repository.storage_info()
        retention_days = float(config["storage"].get("retention_days", 0))
        data["retention_days"] = retention_days
        rate = data["growth_bytes_per_second"]
        data["retention_expected_to_limit_growth"] = False
        data["retention_exceeds_remaining_space"] = False
        data["estimated_seconds_to_full"] = None
        data["growth_measurement_ready"] = data.get("growth_observed_seconds", 0) >= 300
        data["storage_capacity_stable"] = bool(data["growth_measurement_ready"] and rate == 0)
        if rate and rate > 0:
            available_for_database = data["filesystem_free_bytes"] + data.get("sqlite_reusable_bytes", 0)
            projected_retained_bytes = rate * retention_days * 86400 if retention_days > 0 else None
            data["estimated_seconds_to_full"] = available_for_database / rate
            data["retention_expected_to_limit_growth"] = bool(
                projected_retained_bytes is not None and projected_retained_bytes <= available_for_database
            )
            data["retention_exceeds_remaining_space"] = bool(
                retention_days > 0 and data["estimated_seconds_to_full"] < retention_days * 86400
            )
        return data

    @app.get("/api/v1/recording")
    def recording() -> dict[str, Any]:
        info = repository.recording_info()
        archive_dir = Path(config["storage"]["database"]).parent / "archive"
        info["archives"] = [
            {"name": item.name, "bytes": item.stat().st_size, "modified_at": datetime.fromtimestamp(item.stat().st_mtime, timezone.utc).isoformat()}
            for item in sorted(archive_dir.glob("*.sqlite3"), reverse=True)
        ] if archive_dir.is_dir() else []
        result_path = Path(config["storage"]["database"]).parent / "recording-result.json"
        request_path = result_path.with_name("recording-request.json")
        if request_path.is_file():
            try:
                pending = json.loads(request_path.read_text(encoding="utf-8"))
                info["pending_operation"] = {
                    "operation_id": pending.get("operation_id"),
                    "action": pending.get("action"),
                    "reference": pending.get("reference"),
                }
            except (OSError, json.JSONDecodeError):
                pass
        if result_path.is_file():
            try:
                info["last_operation"] = json.loads(result_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                pass
        return info

    @app.get("/api/v1/communication-bridge")
    def communication_bridge() -> dict[str, Any]:
        return communication_bridge_status(load_settings(config_path))

    @app.post("/api/v1/recording/reinitialize", status_code=202)
    def reinitialize_recording(request: Request, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
        require_local_administration(request)
        action = str(payload.get("action", "archive"))
        reference = str(payload.get("reference", "")).strip()
        confirmation = str(payload.get("confirmation", ""))
        if not reference or len(reference) > 240:
            raise HTTPException(422, "reference must contain 1 to 240 characters")
        if action not in {"archive", "delete"}:
            raise HTTPException(422, "action must be archive or delete")
        if action == "delete" and confirmation.split() != ["DELETE"] * 3:
            raise HTTPException(422, "permanent deletion requires DELETE repeated three times")
        request_path = Path(config["storage"]["database"]).parent / "recording-request.json"
        result_path = request_path.with_name("recording-result.json")
        result_path.unlink(missing_ok=True)
        operation_id = uuid.uuid4().hex
        temporary = request_path.with_suffix(".tmp")
        temporary.write_text(json.dumps({"operation_id": operation_id, "action": action, "reference": reference, "confirmation": confirmation}, ensure_ascii=False), encoding="utf-8")
        os.replace(temporary, request_path)
        return {"status": "accepted", "operation_id": operation_id, "action": action, "reference": reference}

    @app.get("/api/v1/engineering")
    def engineering() -> dict[str, Any]:
        current = load_settings(config_path)
        return {"inverters": [
            {
                "name": entry["name"],
                "model": entry.get("model", "VF-AS1"),
                "engineering": entry.get("engineering", {}),
            }
            for entry in current.get("inverters", []) if entry.get("enabled", True)
        ]}

    @app.post("/api/v1/engineering", status_code=202)
    def update_engineering(request: Request, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
        require_local_administration(request)
        name = str(payload.get("inverter", ""))
        values = payload.get("engineering", {})
        try:
            factor = float(values["machine_speed_factor"])
            unit = str(values["machine_speed_unit"]).strip()
            current_a = float(values["rated_output_current_a"])
            voltage_v = float(values["rated_output_voltage_v"])
        except (KeyError, TypeError, ValueError):
            raise HTTPException(422, "all engineering values are required")
        if factor <= 0 or current_a <= 0 or voltage_v <= 0 or not unit or len(unit) > 20:
            raise HTTPException(422, "engineering values must be positive and the unit must contain 1 to 20 characters")
        power_value = values.get("motor_rated_power_kw")
        speed_value = values.get("motor_rated_speed_rpm")
        try:
            power_kw = None if power_value in (None, "") else float(power_value)
            speed_rpm = None if speed_value in (None, "") else float(speed_value)
        except (TypeError, ValueError):
            raise HTTPException(422, "motor rated power and speed must be numeric")
        if (power_kw is None) != (speed_rpm is None) or (power_kw is not None and (power_kw <= 0 or speed_rpm <= 0)):
            raise HTTPException(422, "motor rated power and speed must be positive and configured together")
        settings = load_settings(config_path)
        target = next((item for item in settings.get("inverters", []) if str(item.get("name")) == name), None)
        if target is None:
            raise HTTPException(404, "unknown inverter")
        engineering_values = {
            "machine_speed_factor": factor,
            "machine_speed_unit": unit,
            "rated_output_current_a": current_a,
            "rated_output_voltage_v": voltage_v,
        }
        if power_kw is not None:
            engineering_values["motor_rated_power_kw"] = power_kw
            engineering_values["motor_rated_speed_rpm"] = speed_rpm
        target["engineering"] = engineering_values
        temporary_config = config_path.with_suffix(".tmp")
        temporary_config.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        json.loads(temporary_config.read_text(encoding="utf-8"))
        os.replace(temporary_config, config_path)
        control_dir = Path(config["storage"]["database"]).parent
        result_path = control_dir / "engineering-result.json"
        result_path.unlink(missing_ok=True)
        request_path = control_dir / "engineering-request.json"
        temporary_request = request_path.with_suffix(".tmp")
        temporary_request.write_text(json.dumps({"inverter": name, "engineering": engineering_values}, ensure_ascii=False), encoding="utf-8")
        os.replace(temporary_request, request_path)
        return {"status": "accepted", "inverter": name, "engineering": engineering_values}

    @app.get("/api/v1/channels")
    def channels() -> dict[str, Any]:
        current = load_settings(config_path)
        result = []
        for entry in current.get("inverters", []):
            if not entry.get("enabled", True):
                continue
            configured = entry.get("channels", {})
            default_mode = "off" if "channels" in entry else "record"
            hidden_live_cards = set(entry.get("hidden_live_cards", []))
            available = profile(str(entry.get("model", "VF-AS1")))["registers"]
            result.append({
                "name": str(entry["name"]),
                "model": str(entry.get("model", "VF-AS1")),
                "channels": [
                    {
                        "key": item["key"],
                        "address": item["address"],
                        "scale": item.get("scale", 1),
                        "unit": item.get("unit", "raw"),
                        "sampling": item.get("sampling", "normal"),
                        "mode": "hide" if item["key"] in hidden_live_cards else configured.get(item["key"], default_mode),
                        "protected": False,
                        "internally_required": item["key"] == "operating_status",
                    }
                    for item in available
                ],
            })
        return {"inverters": result, "modes": ["off", "live", "record", "hide"]}

    @app.post("/api/v1/channels", status_code=202)
    def update_channels(request: Request, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
        require_local_administration(request)
        name = str(payload.get("inverter", ""))
        requested = payload.get("channels")
        if not isinstance(requested, dict):
            raise HTTPException(422, "channels must be an object")
        if any(value not in {"off", "live", "record", "hide"} for value in requested.values()):
            raise HTTPException(422, "channel mode must be off, live, record, or hide")
        settings = load_settings(config_path)
        target = next((item for item in settings.get("inverters", []) if str(item.get("name")) == name), None)
        if target is None:
            raise HTTPException(404, "unknown inverter")
        known = {item["key"] for item in profile(str(target.get("model", "VF-AS1")))["registers"]}
        unknown = set(requested) - known
        if unknown:
            raise HTTPException(422, f"unknown channels: {', '.join(sorted(unknown))}")
        target["channels"] = {key: value for key, value in requested.items() if value in {"live", "record"}}
        target["hidden_live_cards"] = sorted(key for key, value in requested.items() if value == "hide")
        temporary_config = config_path.with_suffix(".tmp")
        temporary_config.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        json.loads(temporary_config.read_text(encoding="utf-8"))
        os.replace(temporary_config, config_path)
        control_dir = Path(config["storage"]["database"]).parent
        result_path = control_dir / "channels-result.json"
        result_path.unlink(missing_ok=True)
        request_path = control_dir / "channels-request.json"
        temporary_request = request_path.with_suffix(".tmp")
        temporary_request.write_text(json.dumps({"config": settings}, ensure_ascii=False), encoding="utf-8")
        os.replace(temporary_request, request_path)
        return {"status": "accepted", "inverter": name}

    @app.get("/api/v1/communication/channels")
    def communication_channels() -> dict[str, Any]:
        current = load_settings(config_path)
        configured = current.get("communication_channels", {})
        return {"channels": [{"key": metric, "mode": configured.get(metric, "off")}
                             for metric in COMMUNICATION_METRICS], "modes": ["off", "live", "record", "hide"]}

    @app.post("/api/v1/communication/channels", status_code=202)
    def update_communication_channels(request: Request, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
        require_local_administration(request)
        requested = payload.get("channels")
        if not isinstance(requested, dict) or set(requested) - set(COMMUNICATION_METRICS):
            raise HTTPException(422, "unknown communication channels")
        if any(mode not in {"off", "live", "record", "hide"} for mode in requested.values()):
            raise HTTPException(422, "communication channel mode must be off, live, record, or hide")
        settings = load_settings(config_path)
        previous = settings.get("communication_channels", {})
        merged = {metric: requested.get(metric, previous.get(metric, "off")) for metric in COMMUNICATION_METRICS}
        settings["communication_channels"] = {metric: mode for metric, mode in merged.items() if mode != "off"}
        temporary = config_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.chmod(temporary, 0o660); os.replace(temporary, config_path)
        return {"status": "accepted", "channels": merged}

    @app.get("/api/v1/live-card-order")
    def live_card_order() -> dict[str, Any]:
        """Return the operator-defined order of the live measurement cards.

        This is a dashboard preference only: it deliberately does not create a
        collector request or affect Modbus polling and recording.
        """
        current = load_settings(config_path)
        order = current.get("web", {}).get("live_card_order", [])
        return {"order": order if isinstance(order, list) else []}

    @app.get("/api/v1/live-group-order")
    def live_group_order() -> dict[str, Any]:
        current = load_settings(config_path)
        order = current.get("web", {}).get("live_group_order", [])
        return {"order": order if isinstance(order, list) else []}

    @app.post("/api/v1/live-group-order", status_code=202)
    def update_live_group_order(request: Request, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
        require_local_administration(request)
        order = payload.get("order")
        if not isinstance(order, list) or len(order) > 100 or any(not isinstance(item, str) or len(item) > 120 for item in order):
            raise HTTPException(422, "order must contain at most 100 group identifiers")
        if len(order) != len(set(order)):
            raise HTTPException(422, "order contains duplicate group identifiers")
        settings = load_settings(config_path)
        allowed = {str(entry.get("name", "")) for entry in settings.get("inverters", []) if entry.get("enabled", True)}
        allowed.update(definition.source_name for definition in configured_addons(settings) if definition.enabled)
        if any(mode in {"live", "record"} for mode in settings.get("communication_channels", {}).values()):
            allowed.add("communication")
        if set(order) - allowed:
            raise HTTPException(422, "order contains unavailable live groups")
        settings.setdefault("web", {})["live_group_order"] = order
        temporary = config_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.chmod(temporary, 0o660)
        os.replace(temporary, config_path)
        return {"status": "accepted", "order": order}

    @app.post("/api/v1/live-card-order", status_code=202)
    def update_live_card_order(request: Request, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
        require_local_administration(request)
        order = payload.get("order")
        if not isinstance(order, list) or len(order) > 500 or any(not isinstance(item, str) or len(item) > 250 for item in order):
            raise HTTPException(422, "order must contain at most 500 card identifiers")
        if len(order) != len(set(order)):
            raise HTTPException(422, "order contains duplicate card identifiers")

        settings = load_settings(config_path)
        allowed: set[str] = set()
        for entry in settings.get("inverters", []):
            if not entry.get("enabled", True):
                continue
            name = str(entry.get("name", ""))
            configured = entry.get("channels", {})
            registers = profile(str(entry.get("model", "VF-AS1")))["registers"]
            enabled = {item["key"] for item in registers if configured.get(item["key"], "record") != "off"}
            enabled.add("operating_status")
            for derived, source in DERIVED_CHANNEL_SOURCES.items():
                if source in enabled:
                    enabled.add(derived)
            allowed.update(f"{name}\x1f{metric}" for metric in enabled)
        # Sequent field and system cards share the dashboard order with drive
        # measurements.  Their dedicated configuration/control panels remain
        # available independently.
        for definition in configured_addons(settings):
            if not definition.enabled:
                continue
            if definition.kind in SYSTEM_ADDON_METRICS:
                overrides = {str(channel.get("metric")): channel for channel in definition.channels}
                for metric in SYSTEM_ADDON_METRICS[definition.kind]:
                    channel = overrides.get(metric, {})
                    if channel.get("enabled", True) and channel.get("live", True):
                        allowed.add(f"{definition.source_name}\x1faddon.{definition.identifier}.{metric}")
                if definition.kind == "sequent_super_watchdog":
                    allowed.add(f"{definition.source_name}\x1faddon.{definition.identifier}.estimated_battery_runtime")
                continue
            for channel in effective_addon_channels(definition):
                if not channel.get("enabled", True) or not channel.get("live", True):
                    continue
                signal = str(channel.get("signal", "input"))
                metric = f"addon.{definition.identifier}.{signal}_{int(channel['channel']):02d}"
                allowed.add(f"{definition.source_name}\x1f{metric}")
        communication_modes = settings.get("communication_channels", {})
        allowed.update(f"communication\x1f{metric}" for metric in COMMUNICATION_METRICS
                       if communication_modes.get(metric) in {"live", "record"})
        if set(order) - allowed:
            raise HTTPException(422, "order contains unavailable measurement cards")

        web_settings = settings.setdefault("web", {})
        web_settings["live_card_order"] = order
        temporary_config = config_path.with_suffix(".tmp")
        temporary_config.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        json.loads(temporary_config.read_text(encoding="utf-8"))
        os.replace(temporary_config, config_path)
        return {"status": "accepted", "order": order}

    @app.get("/api/v1/dashboard-section-order")
    def dashboard_section_order() -> dict[str, Any]:
        current = load_settings(config_path)
        order = current.get("web", {}).get("dashboard_section_order", [])
        return {"order": order if isinstance(order, list) else []}

    @app.post("/api/v1/dashboard-section-order", status_code=202)
    def update_dashboard_section_order(request: Request, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
        require_local_administration(request)
        order = payload.get("order")
        if not isinstance(order, list) or any(not isinstance(item, str) for item in order) or set(order) != set(DASHBOARD_SECTION_IDS) or len(order) != len(DASHBOARD_SECTION_IDS):
            raise HTTPException(422, "order must contain every dashboard category exactly once")
        settings = load_settings(config_path)
        settings.setdefault("web", {})["dashboard_section_order"] = order
        temporary_config = config_path.with_suffix(".tmp")
        temporary_config.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        json.loads(temporary_config.read_text(encoding="utf-8"))
        os.replace(temporary_config, config_path)
        return {"status": "accepted", "order": order}

    @app.get("/api/v1/parameter-backups")
    def parameter_backups(inverter: str | None = Query(default=None, max_length=120)) -> dict[str, Any]:
        directory = Path(config["storage"]["database"]).parent / "parameter-backups"
        result_path = directory.parent / "parameter-backup-result.json"
        result: dict[str, Any] = {"status": "idle", "files": []}
        if result_path.is_file():
            try:
                result.update(json.loads(result_path.read_text(encoding="utf-8")))
            except (OSError, json.JSONDecodeError):
                pass
        if inverter is not None and inverter not in device_by_name:
            raise HTTPException(404, "unknown inverter")
        if directory.is_dir():
            current_pcm = None
            if inverter is not None:
                pcm_files = parameter_backup_files(directory, inverter)
                current_pcm = pcm_files[0].name if pcm_files else None
                files = []
                for pcm in pcm_files:
                    files.append(pcm)
                    report = pcm.with_suffix(".txt")
                    if report.is_file():
                        files.append(report)
            else:
                files = [*directory.glob("*.pcm"), *directory.glob("*.txt")]
            result["files"] = [
                {
                    "name": item.name,
                    "bytes": item.stat().st_size,
                    "modified_at": datetime.fromtimestamp(item.stat().st_mtime, timezone.utc).isoformat(timespec="seconds"),
                    "partial": item.name.endswith("-partial.pcm") or item.name.endswith("-partial.txt"),
                    "current": item.name == current_pcm,
                }
                for item in sorted(files, key=lambda path: path.stat().st_mtime, reverse=True)
            ]
        return result

    @app.post("/api/v1/parameter-backups", status_code=202)
    def create_parameter_backup(request: Request, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
        require_local_administration(request)
        name = str(payload.get("inverter", ""))
        if name not in device_by_name:
            raise HTTPException(404, "unknown inverter")
        try:
            raw_content = base64.b64decode(str(payload.get("content_base64", "")), validate=True)
            content = raw_content.decode("ascii")
        except (ValueError, binascii.Error, UnicodeDecodeError) as error:
            raise HTTPException(422, "PCM template must be an ASCII PCM002Z file") from error
        if not 1 <= len(raw_content) <= 300000:
            raise HTTPException(422, "PCM template must contain 1 to 300000 bytes")
        if not content.startswith("###"):
            raise HTTPException(422, "not a PCM002Z PCM file")
        control_dir = Path(config["storage"]["database"]).parent
        result_path = control_dir / "parameter-backup-result.json"
        result_path.unlink(missing_ok=True)
        request_path = control_dir / "parameter-backup-request.json"
        temporary = request_path.with_suffix(".tmp")
        temporary.write_text(json.dumps({"inverter": name, "content": content}), encoding="utf-8")
        os.replace(temporary, request_path)
        return {"status": "accepted", "inverter": name}

    @app.get("/api/v1/parameter-backups/{filename}")
    def download_parameter_backup(filename: str) -> FileResponse:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+\.(?:pcm|txt)", filename):
            raise HTTPException(404, "backup not found")
        path = Path(config["storage"]["database"]).parent / "parameter-backups" / filename
        if not path.is_file():
            raise HTTPException(404, "backup not found")
        return FileResponse(path, media_type="application/octet-stream", filename=filename)

    @app.delete("/api/v1/parameter-backups/{filename}")
    def delete_parameter_backup(filename: str, request: Request) -> dict[str, Any]:
        require_local_administration(request)
        if not re.fullmatch(r"[A-Za-z0-9_.-]+\.(?:pcm|txt)", filename):
            raise HTTPException(404, "backup not found")
        directory = Path(config["storage"]["database"]).parent / "parameter-backups"
        path = directory / filename
        if not path.is_file():
            raise HTTPException(404, "backup not found")
        deleted = [path.name]
        # A partial PCM and its diagnostic report are one backup artifact.
        path.unlink()
        if path.suffix.lower() == ".pcm":
            report = path.with_suffix(".txt")
            if report.is_file():
                report.unlink()
                deleted.append(report.name)
        return {"status": "deleted", "files": deleted}

    @app.post("/api/v1/parameter-import-preview")
    def parameter_import_preview(request: Request, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
        require_local_administration(request)
        name = str(payload.get("inverter", ""))
        device = device_by_name.get(name)
        if device is None:
            raise HTTPException(404, "unknown inverter")
        try:
            target_bytes = base64.b64decode(str(payload.get("content_base64", "")), validate=True)
            target_content = target_bytes.decode("ascii")
        except (ValueError, binascii.Error, UnicodeDecodeError) as error:
            raise HTTPException(422, "target must be an ASCII PCM002Z file") from error
        target_header, target_records = parse_pcm_template(target_content)
        if not pcm_template_matches_model(target_header, device.model):
            raise HTTPException(422, "target PCM model does not match the configured inverter")
        backup_dir = Path(config["storage"]["database"]).parent / "parameter-backups"
        current_files = parameter_backup_files(backup_dir, name)
        if not current_files:
            raise HTTPException(409, "create a parameter backup before comparing an import")
        current_file = current_files[0]
        backup_age_seconds = parameter_backup_age_seconds(current_file)
        try:
            max_backup_age_minutes = float(config["storage"].get("parameter_write_max_backup_age_minutes", 60))
        except (TypeError, ValueError):
            max_backup_age_minutes = 60
        current_header, current_records = parse_pcm_template(current_file.read_text(encoding="ascii"))
        if not pcm_template_matches_model(current_header, device.model):
            raise HTTPException(409, "newest parameter backup does not match the configured inverter")
        current = {address: value for address, value, _a, _b in current_records}
        rows = []
        counts = {key: 0 for key in ("candidate", "communication", "special", "monitor", "unsupported")}
        for address, target_value, _marker_a, marker_b in target_records:
            if address not in current or current[address] == target_value:
                continue
            classification = parameter_safety_class(address, marker_b, device.model)
            counts[classification] += 1
            rows.append({
                "address": f"{address:04X}", "current": current[address], "target": target_value,
                "classification": classification, "selectable": classification == "candidate",
            })
        return {"inverter": name, "target_sha256": hashlib.sha256(target_bytes).hexdigest(), "current_file": current_file.name, "current_backup_age_seconds": backup_age_seconds,
                "backup_stale": max_backup_age_minutes > 0 and backup_age_seconds > max_backup_age_minutes * 60,
                "changes": rows, "counts": counts}

    @app.post("/api/v1/parameter-write", status_code=202)
    def parameter_write(request: Request, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
        require_local_administration(request)
        name = str(payload.get("inverter", ""))
        address_texts = [str(value).upper() for value in payload.get("addresses", [])]
        confirmation = str(payload.get("confirmation", ""))
        device = device_by_name.get(name)
        if device is None or device.model != "VF-AS1":
            raise HTTPException(422, "parameter writing is currently limited to VF-AS1")
        addresses = sorted(address_texts)
        if not 1 <= len(addresses) <= 32 or len(set(addresses)) != len(addresses) or any(not re.fullmatch(r"[0-9A-F]{4}", value) for value in addresses):
            raise HTTPException(422, "select between 1 and 32 distinct four-digit hexadecimal addresses")
        if confirmation != f"WRITE {' '.join(addresses)}":
            raise HTTPException(422, "confirmation must be exactly WRITE followed by all selected addresses in ascending order")
        try:
            content_bytes = base64.b64decode(str(payload.get("content_base64", "")), validate=True)
            content = content_bytes.decode("ascii")
            header, records = parse_pcm_template(content)
            if not pcm_template_matches_model(header, device.model):
                raise HTTPException(422, "target PCM model does not match the configured inverter")
            limits = parse_pcm_csv_limits(base64.b64decode(str(payload.get("csv_base64", "")), validate=True).decode("ascii"))
        except (ValueError, binascii.Error, UnicodeDecodeError) as error:
            raise HTTPException(422, "target PCM and matching PCM002Z CSV limits are required") from error
        target_sha256 = hashlib.sha256(content_bytes).hexdigest()
        if str(payload.get("preview_sha256", "")) != target_sha256:
            raise HTTPException(409, "target PCM differs from the file used for the import preview; compare it again")
        changes = []
        for address_text in addresses:
            address = int(address_text, 16)
            record = next((item for item in records if item[0] == address), None)
            if record is None or parameter_safety_class(address, record[3], device.model) != "candidate":
                raise HTTPException(422, f"{address_text} is not an approved configuration candidate")
            target_raw = record[1] & 0xFFFF
            if address not in limits or not limits[address][0] <= target_raw <= limits[address][1]:
                raise HTTPException(422, f"{address_text} is outside the verified PCM002Z CSV range")
            changes.append({"address": address, "target": target_raw})
        backup_dir = Path(config["storage"]["database"]).parent / "parameter-backups"
        current_files = parameter_backup_files(backup_dir, name)
        if not current_files:
            raise HTTPException(409, "create a parameter backup before writing")
        current_header, current_records = parse_pcm_template(current_files[0].read_text(encoding="ascii"))
        if not pcm_template_matches_model(current_header, device.model):
            raise HTTPException(409, "newest parameter backup does not match the configured inverter")
        try:
            max_backup_age_minutes = float(config["storage"].get("parameter_write_max_backup_age_minutes", 60))
        except (TypeError, ValueError):
            max_backup_age_minutes = 60
        backup_age_seconds = parameter_backup_age_seconds(current_files[0])
        if max_backup_age_minutes > 0 and backup_age_seconds > max_backup_age_minutes * 60:
            raise HTTPException(409, f"newest parameter backup is {backup_age_seconds // 60} minutes old; create a current backup before writing")
        current = {item[0]: item[1] for item in current_records}
        unchanged = [f"{item['address']:04X}" for item in changes if current.get(item["address"]) == item["target"]]
        if unchanged:
            raise HTTPException(422, f"value already matches the newest backup: {', '.join(unchanged)}")
        control_dir = Path(config["storage"]["database"]).parent
        request_path = control_dir / "parameter-write-request.json"
        if request_path.exists():
            raise HTTPException(409, "a parameter write request is already pending")
        result_path = control_dir / "parameter-write-result.json"; result_path.unlink(missing_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(prefix="parameter-write-", suffix=".tmp", dir=control_dir)
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                handle.write(json.dumps({"inverter": name, "changes": changes, "source_backup": current_files[0].name, "target_sha256": target_sha256}))
            try:
                # link() reserves the request name atomically. A pending request
                # therefore cannot be overwritten by another browser click.
                os.link(temporary, request_path)
            except FileExistsError as error:
                raise HTTPException(409, "a parameter write request is already pending") from error
        finally:
            temporary.unlink(missing_ok=True)
        return {"status": "accepted", "addresses": addresses, "count": len(changes)}

    @app.post("/api/v1/parameter-preflight", status_code=202)
    def parameter_preflight(request: Request, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
        require_local_administration(request)
        name = str(payload.get("inverter", ""))
        device = device_by_name.get(name)
        if device is None or device.model != "VF-AS1":
            raise HTTPException(422, "parameter preflight is currently limited to VF-AS1")
        control_dir = Path(config["storage"]["database"]).parent
        request_path = control_dir / "parameter-preflight-request.json"
        if request_path.exists():
            raise HTTPException(409, "a parameter preflight is already pending")
        result_path = control_dir / "parameter-preflight-result.json"; result_path.unlink(missing_ok=True)
        temporary = request_path.with_suffix(".tmp")
        temporary.write_text(json.dumps({"inverter": name}), encoding="utf-8")
        os.replace(temporary, request_path)
        return {"status": "accepted", "inverter": name}

    @app.get("/api/v1/parameter-preflight")
    def parameter_preflight_status() -> dict[str, Any]:
        path = Path(config["storage"]["database"]).parent / "parameter-preflight-result.json"
        if not path.is_file():
            return {"status": "idle"}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"status": "error", "detail": "invalid result file"}

    @app.get("/api/v1/parameter-write")
    def parameter_write_status() -> dict[str, Any]:
        path = Path(config["storage"]["database"]).parent / "parameter-write-result.json"
        if not path.is_file():
            return {"status": "idle"}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"status": "error", "detail": "invalid result file"}

    @app.get("/api/v1/parameter-changes")
    def parameter_changes(limit: int = Query(20, ge=1, le=100)) -> dict[str, Any]:
        """Return the verified parameter-write audit trail without exposing writes."""
        database_path = Path(config["storage"]["database"])
        if not database_path.is_file():
            return {"items": []}
        try:
            connection = sqlite3.connect(f"file:{database_path}?mode=ro", uri=True)
            connection.row_factory = sqlite3.Row
            try:
                rows = connection.execute(
                    "SELECT changed_at,inverter,slave_id,register_address,old_raw_value,new_raw_value,verified_raw_value,result,source_backup,target_sha256 "
                    "FROM parameter_changes ORDER BY id DESC LIMIT ?", (limit,)
                ).fetchall()
            finally:
                connection.close()
        except sqlite3.Error:
            return {"items": []}
        return {"items": [{
            "changed_at": row["changed_at"], "inverter": row["inverter"], "slave_id": row["slave_id"],
            "address": f"{row['register_address']:04X}", "old": row["old_raw_value"],
            "new": row["new_raw_value"], "verified": row["verified_raw_value"], "result": row["result"],
            "source_backup": row["source_backup"], "target_sha256": row["target_sha256"],
        } for row in rows]}

    @app.get("/api/v1/parameter-changes.csv")
    def export_parameter_changes() -> StreamingResponse:
        database_path = Path(config["storage"]["database"])
        recording_reference = repository.recording_info()["reference"]
        rows: list[sqlite3.Row] = []
        if database_path.is_file():
            try:
                connection = sqlite3.connect(f"file:{database_path}?mode=ro", uri=True)
                connection.row_factory = sqlite3.Row
                try:
                    rows = connection.execute(
                    "SELECT changed_at,inverter,slave_id,register_address,old_raw_value,new_raw_value,verified_raw_value,result,source_backup,target_sha256 "
                        "FROM parameter_changes ORDER BY id ASC LIMIT ?", (export_max_rows,)
                    ).fetchall()
                finally:
                    connection.close()
            except sqlite3.Error:
                rows = []

        def generate():
            buffer = io.StringIO(); writer = csv.writer(buffer, lineterminator="\n")
            writer.writerow(("changed_at", "inverter", "slave_id", "register_address", "old_raw_value", "new_raw_value", "verified_raw_value", "result", "source_backup", "target_sha256", "investigation_reference"))
            yield buffer.getvalue()
            for row in rows:
                buffer.seek(0); buffer.truncate(0)
                writer.writerow((row["changed_at"], row["inverter"], row["slave_id"], f"0x{row['register_address']:04X}", row["old_raw_value"], row["new_raw_value"], row["verified_raw_value"], row["result"], row["source_backup"], row["target_sha256"], recording_reference))
                yield buffer.getvalue()

        filename = f"tmm-parameter-changes-{datetime.now(timezone.utc).date().isoformat()}.csv"
        return StreamingResponse(generate(), media_type="text/csv; charset=utf-8", headers={"Content-Disposition": f'attachment; filename="{filename}"'})

    @app.get("/api/v1/metrics/latest")
    def latest() -> dict[str, Any]:
        enabled = active_metrics()
        addon_sources = active_addon_sources()
        current_values, _ = current_live_snapshot()
        return {
            "items": [
                enrich_sample(item, device_by_name[item["inverter"]].model) if device_by_name.get(item["inverter"], None) and device_by_name[item["inverter"]].decoder else item
                for item in current_values
                if is_active_sample(item, enabled, addon_sources)
            ]
        }

    @app.get("/api/v1/conditions")
    def conditions() -> dict[str, Any]:
        rules = condition_rules(load_settings(config_path))
        states = {item["rule_id"]: item for item in repository.condition_states()}
        return {"operators": sorted(OPERATORS), "rules": [rule.as_dict() | {"state": states.get(rule.identifier)} for rule in rules]}

    @app.post("/api/v1/conditions", status_code=202)
    def update_condition(request: Request, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
        require_local_administration(request)
        settings = load_settings(config_path)
        raw_rules = settings.setdefault("condition_monitoring", {}).setdefault("rules", [])
        if not isinstance(raw_rules, list):
            raise HTTPException(422, "condition_monitoring.rules must be a list")
        identifier = str(payload.get("id", "")).strip() or f"condition-{int(time.time() * 1000)}"
        existing = next((item for item in raw_rules if str(item.get("id")) == identifier), None)
        revision = int(existing.get("revision", 1)) + 1 if existing else 1
        candidate = {key: payload[key] for key in (
            "name", "source", "metric", "operator", "value", "duration_seconds",
            "hysteresis", "tolerance", "severity", "enabled", "expression"
        ) if key in payload}
        candidate.update({"id": identifier, "revision": revision})
        if existing is None:
            raw_rules.append(candidate)
        else:
            existing.clear(); existing.update(candidate)
        try:
            normalized = condition_rules(settings)
        except (TypeError, ValueError, KeyError) as error:
            raise HTTPException(422, str(error)) from error
        temporary = config_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.chmod(temporary, 0o660); os.replace(temporary, config_path)
        control_dir = Path(settings["storage"]["database"]).parent
        request_path = control_dir / "conditions-request.json"; request_tmp = request_path.with_suffix(".tmp")
        request_tmp.write_text(json.dumps({"config": settings}, ensure_ascii=False), encoding="utf-8"); os.replace(request_tmp, request_path)
        rule = next(item for item in normalized if item.identifier == identifier)
        return {"status": "accepted", "rule": rule.as_dict()}

    @app.delete("/api/v1/conditions/{identifier}", status_code=202)
    def delete_condition(request: Request, identifier: str) -> dict[str, Any]:
        require_local_administration(request)
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", identifier): raise HTTPException(422, "invalid condition rule id")
        settings = load_settings(config_path); monitoring = settings.setdefault("condition_monitoring", {})
        raw_rules = monitoring.setdefault("rules", []); retained = [item for item in raw_rules if str(item.get("id")) != identifier]
        if len(retained) == len(raw_rules): raise HTTPException(404, "unknown condition rule")
        monitoring["rules"] = retained; condition_rules(settings)
        temporary = config_path.with_suffix(".tmp"); temporary.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.chmod(temporary, 0o660); os.replace(temporary, config_path)
        request_path = Path(settings["storage"]["database"]).parent / "conditions-request.json"; request_tmp = request_path.with_suffix(".tmp")
        request_tmp.write_text(json.dumps({"config": settings}, ensure_ascii=False), encoding="utf-8"); os.replace(request_tmp, request_path)
        return {"status": "accepted", "id": identifier}

    @app.get("/api/v1/milestones")
    def milestones(start: datetime | None = None, end: datetime | None = None,
                   limit: Annotated[int, Query(ge=1, le=10000)] = 1000) -> dict[str, Any]:
        return {"items": repository.milestones(parse_timestamp(start), parse_timestamp(end), limit)}

    @app.get("/api/v1/metrics/catalog")
    def metric_catalog() -> dict[str, Any]:
        """All retained selectable metrics, also available while Modbus is offline."""
        addon_sources = active_addon_sources()
        items = {
            (item["inverter"], item["metric"]): item
            for item in repository.recorded_metrics()
            if is_known_historical_sample(item, addon_sources)
        }
        for device in devices:
            for register in profile(device.model)["registers"]:
                items.setdefault((device.name, register["key"]), {
                    "inverter": device.name, "slave_id": device.slave_id, "metric": register["key"],
                    "metric_label": register["key"].replace("_", " ").title(),
                    "unit": str(register.get("unit", "raw")), "minimum_value": None,
                    "maximum_value": None, "observed_at": None,
                })
        # Field I/O defaults to Off, so it has no latest value and no history
        # yet.  It must nevertheless be offered here; otherwise an operator
        # cannot enable a newly named channel from the unified history cards.
        for definition in configured_addons(load_settings(config_path)):
            if not definition.enabled:
                continue
            source = definition.source_name
            configured = {(str(channel.get("signal", "input")), int(channel.get("channel", 0))): channel for channel in definition.channels}
            if definition.kind in {"raspberry_pi_gpio", "sequent_16inpind", "sequent_24b8vin"}:
                numbers = sorted(number for signal, number in configured if signal == "input") if definition.kind == "raspberry_pi_gpio" else range(1, 17 if definition.kind == "sequent_16inpind" else 9)
                default_unit = "on/off" if definition.kind in {"raspberry_pi_gpio", "sequent_16inpind"} else "V"
                for number in numbers:
                    channel = configured.get(("input", number), {})
                    prefix = "gpio" if definition.kind == "raspberry_pi_gpio" else "input"
                    metric = f"addon.{definition.identifier}.{prefix}_{number:02d}"
                    default_label = f"GPIO {number}" if definition.kind == "raspberry_pi_gpio" else f"{'DI' if definition.kind == 'sequent_16inpind' else 'AI'} {number}"
                    catalog_item = items.setdefault((source, metric), {
                        "inverter": source, "slave_id": -(definition.stack + 1), "metric": metric,
                        "metric_label": str(channel.get("label") or default_label),
                        "unit": str(channel.get("unit", default_unit)), "minimum_value": None, "maximum_value": None,
                        "observed_at": None,
                    })
                    # A technician's current name and engineering unit are
                    # authoritative, even if old samples were recorded before
                    # the channel was named.
                    catalog_item["metric_label"] = str(channel.get("label") or default_label)
                    catalog_item["unit"] = str(channel.get("unit", default_unit))
            elif definition.kind == "sequent_multiio":
                for (signal, number), channel in configured.items():
                    if signal not in MULTIIO_INPUTS:
                        continue
                    _, default_unit, _ = MULTIIO_INPUTS[signal]
                    metric = f"addon.{definition.identifier}.{signal}_{number:02d}"
                    catalog_item = items.setdefault((source, metric), {
                        "inverter": source, "slave_id": -(definition.stack + 1), "metric": metric,
                        "metric_label": str(channel.get("label") or f"Multi-IO {signal} {number}"),
                        "unit": str(channel.get("unit", default_unit)), "minimum_value": None, "maximum_value": None,
                        "observed_at": None,
                    })
                    catalog_item["metric_label"] = str(channel.get("label") or f"Multi-IO {signal} {number}")
                    catalog_item["unit"] = str(channel.get("unit", default_unit))
        for metric, (label, unit) in COMMUNICATION_METRICS.items():
            items.setdefault(("communication", metric), {"inverter": "communication", "slave_id": 0, "metric": metric,
                "metric_label": label, "unit": unit, "minimum_value": None, "maximum_value": None, "observed_at": None})
        return {"items": sorted(items.values(), key=lambda item: (item["inverter"], item["metric"]))}

    @app.get("/api/v1/metrics/history")
    def history(
        metric: Annotated[str, Query(min_length=1, max_length=80, pattern=r"^[A-Za-z0-9_.-]+$")],
        inverter: Annotated[str | None, Query(max_length=120)] = None,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: Annotated[int, Query(ge=1, le=10000)] = 1000,
    ) -> dict[str, Any]:
        start_value = parse_timestamp(start)
        end_value = parse_timestamp(end)
        if start_value and end_value and start_value > end_value:
            raise HTTPException(422, "start must not be later than end")
        if inverter == "communication" and metric.startswith("communication."):
            mode = load_settings(config_path).get("communication_channels", {}).get(metric, "off")
            items = repository.communication_history(metric, limit) if mode in {"record", "hide"} else []
        elif metric in {"terminal_f", "terminal_r", "terminal_s1", "terminal_s2", "terminal_s3"} and inverter in device_by_name:
            model = device_by_name[inverter].model
            source_items = repository.history("input_terminal_status", inverter, start_value, end_value, limit)
            items = terminal_history_items(source_items, metric, model)
        else:
            items = repository.history(metric, inverter, start_value, end_value, limit)
        decode = inverter in device_by_name and device_by_name[inverter].decoder
        model = device_by_name[inverter].model if inverter in device_by_name else "VF-AS1"
        return {"metric": metric, "inverter": inverter, "items": [enrich_sample(item, model) for item in items] if decode else items}

    @app.get("/api/v1/poll-cycles")
    def cycles(limit: Annotated[int, Query(ge=1, le=1000)] = 100) -> dict[str, Any]:
        return {"items": repository.poll_cycles(limit)}

    @app.get("/api/v1/diagnostics")
    def diagnostics() -> dict[str, Any]:
        return current_diagnostics()

    @app.get("/api/v1/proxy-transactions")
    def proxy_transactions(limit: Annotated[int, Query(ge=1, le=500)] = 50) -> dict[str, Any]:
        def crc_evidence(hexadecimal: str | None) -> dict[str, Any] | None:
            if not hexadecimal:
                return None
            try:
                frame = bytes.fromhex(hexadecimal)
            except ValueError:
                return {"received": None, "calculated": None, "valid": False}
            if len(frame) < 2:
                return {"received": None, "calculated": None, "valid": False}
            received = int.from_bytes(frame[-2:], "little")
            calculated = crc16(frame[:-2])
            return {
                "received": frame[-2:].hex(" ").upper(),
                "calculated": calculated.to_bytes(2, "little").hex(" ").upper(),
                "valid": received == calculated,
            }

        items = repository.proxy_transactions(limit)
        for item in items:
            item["request_crc"] = crc_evidence(item.get("request_hex"))
            item["response_crc"] = crc_evidence(item.get("response_hex"))
            request = bytes.fromhex(item["request_hex"]) if item.get("request_hex") else b""
            item["slave"] = request[0] if request else None
            item["function"] = request[1] if len(request) > 1 else None
        return {"items": items}

    @app.get("/api/v1/export.csv")
    def export_csv(
        metric: Annotated[str | None, Query(max_length=80, pattern=r"^[A-Za-z0-9_.-]+$")] = None,
        metrics: Annotated[str | None, Query(max_length=5000)] = None,
        inverter: Annotated[str | None, Query(max_length=120)] = None,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> StreamingResponse:
        start_value = parse_timestamp(start)
        end_value = parse_timestamp(end)
        if start_value and end_value and start_value > end_value:
            raise HTTPException(422, "start must not be later than end")

        selected_metrics = [item for item in (metrics or "").split(",") if item]
        if any(not re.fullmatch(r"[A-Za-z0-9_.-]+", item) for item in selected_metrics):
            raise HTTPException(422, "metrics contains an invalid name")
        if len(selected_metrics) > 128:
            raise HTTPException(422, "at most 128 metrics may be exported")

        def generate():
            buffer = io.StringIO()
            writer = csv.writer(buffer, lineterminator="\n")
            reference = repository.recording_info()["reference"]
            writer.writerow(("observed_at", "inverter", "slave_id", "metric", "register_address", "raw_value", "value", "unit", "metric_label", "investigation_reference"))
            yield buffer.getvalue()
            if inverter == "communication":
                modes = load_settings(config_path).get("communication_channels", {})
                requested = selected_metrics or ([metric] if metric else list(COMMUNICATION_METRICS))
                for communication_metric in requested:
                    if communication_metric not in COMMUNICATION_METRICS or modes.get(communication_metric) not in {"record", "hide"}:
                        continue
                    label, _ = COMMUNICATION_METRICS[communication_metric]
                    for item in repository.communication_history(communication_metric, export_max_rows):
                        buffer.seek(0)
                        buffer.truncate(0)
                        writer.writerow((item["observed_at"], "communication", 0, communication_metric, "", item["raw_value"], item["value"], item["unit"], label, reference))
                        yield buffer.getvalue()
                return
            for row in repository.export_rows(metric, selected_metrics or None, inverter, start_value, end_value, export_max_rows):
                buffer.seek(0)
                buffer.truncate(0)
                writer.writerow((*row, reference))
                yield buffer.getvalue()
            # Thermal protection is an operational event stream, not an
            # ordinary measurement. Include it in a full CSV export so a
            # recording remains auditable outside the dashboard.
            if not metric and not selected_metrics and not inverter:
                for event in repository.thermal_events(export_max_rows):
                    buffer.seek(0)
                    buffer.truncate(0)
                    writer.writerow((event["observed_at"], "system", 0, "system.thermal_protection", "",
                                     "", event["temperature_celsius"], "°C",
                                     f"{event['state']} · factor {event['interval_factor']} · {event['detail']}", reference))
                    yield buffer.getvalue()

        filename_part = re.sub(r"[^A-Za-z0-9_.-]+", "_", inverter or "all")
        filename = f"tmm-{filename_part}-{metric or ('selected' if selected_metrics else 'all')}-{datetime.now(timezone.utc).date().isoformat()}.csv"
        return StreamingResponse(
            generate(),
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    @app.get("/", include_in_schema=False)
    def dashboard() -> FileResponse:
        return FileResponse(
            STATIC_DIR / "index.html",
            headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"},
        )

    @app.get("/README.md", include_in_schema=False)
    def readme() -> FileResponse:
        return FileResponse(README_PATH, media_type="text/markdown; charset=utf-8")

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    return app


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    config = load_settings(args.config)
    web = config.get("web", {})
    uvicorn.run(
        create_app(args.config),
        host=str(web.get("host", "0.0.0.0")),
        port=int(web.get("port", 8080)),
        access_log=False,
    )


if __name__ == "__main__":
    main()
