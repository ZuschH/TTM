#!/usr/bin/env python3
"""Read-only web API and dashboard for Toshiba Modbus Monitor (TMM)."""

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
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, Any

import uvicorn
try:
    import psutil
except ImportError:  # pragma: no cover - useful for a minimal development host
    psutil = None  # type: ignore[assignment]
from fastapi import Body, FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from tmm_decode import enrich_sample
from tmm_monitor import configured_devices, parameter_backup_files, parameter_safety_class, parse_pcm_template, pcm_template_matches_model
from tmm_profiles import profile
from tmm_web_data import MonitorRepository

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
README_PATH = APP_DIR / "README.md"

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
}

DASHBOARD_SECTION_IDS = (
    "device-info-title", "alerts-title", "live-title", "io-title", "history-title",
    "fault-title", "storage-title", "recording-title", "channels-title", "comm-title",
    "engineering-title", "parameter-backup-title", "parameter-preview-title",
)

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
            result[section][key] = {"warning": warning, "critical": critical}
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
    alert_thresholds = configured_alert_thresholds(config)
    app = FastAPI(
        title="Toshiba Modbus Monitor API",
        version="1.0.0",
        description="Read-only access to current and historical inverter measurements.",
    )

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

    def require_local_administration(request: Request) -> None:
        client = request.client.host if request.client else ""
        allow_remote = bool(config.get("web", {}).get("allow_remote_administration", False))
        if not allow_remote and client not in {"127.0.0.1", "::1"}:
            raise HTTPException(403, "administration is restricted to localhost")

    @app.get("/api/v1/health")
    def health() -> dict[str, Any]:
        try:
            cycles = repository.last_cycles()
        except (FileNotFoundError, sqlite3.Error) as error:
            return {"status": "unavailable", "database": False, "detail": str(error)}
        if not cycles:
            return {"status": "starting", "database": True, "devices": []}
        device_states = []
        for cycle in cycles:
            observed = datetime.fromisoformat(cycle["observed_at"].replace("Z", "+00:00"))
            age = max(0.0, (datetime.now(timezone.utc) - observed).total_seconds())
            if age > stale_after:
                device_status = "stale"
            elif cycle["failed_reads"]:
                device_status = "degraded"
            else:
                device_status = "healthy"
            device_states.append({"status": device_status, "age_seconds": round(age, 3), **cycle})
        statuses = {item["status"] for item in device_states}
        status = "stale" if "stale" in statuses else "degraded" if "degraded" in statuses else "healthy"
        return {
            "status": status,
            "database": True,
            "age_seconds": max(item["age_seconds"] for item in device_states),
            "stale_after_seconds": stale_after,
            "last_cycle": max(cycles, key=lambda item: item["id"]),
            "devices": device_states,
        }

    @app.get("/api/v1/metadata")
    def metadata() -> dict[str, Any]:
        enabled = active_metrics()
        return {
            "product": "Toshiba Modbus Monitor",
            "short_name": "TMM",
            "version": "1.0.0",
            "contact": config.get("product", {}),
            "inverters": [
                {"name": device.name, "model": device.model, "slave_id": device.slave_id}
                for device in devices
            ],
            "poll_interval_seconds": config["polling"]["interval_seconds"],
            "metrics": sorted({
                item["metric"]
                for item in repository.latest_samples()
                if item["metric"] in enabled.get(item["inverter"], set())
            }),
            "retention_days": float(config["storage"].get("retention_days", 0)),
            "alert_thresholds": alert_thresholds,
        }

    @app.get("/api/v1/storage")
    def storage() -> dict[str, Any]:
        data = repository.storage_info()
        retention_days = float(config["storage"].get("retention_days", 0))
        data["retention_days"] = retention_days
        rate = data["growth_bytes_per_second"]
        data["retention_expected_to_limit_growth"] = False
        data["retention_exceeds_remaining_space"] = False
        data["estimated_seconds_to_full"] = None
        if rate and rate > 0:
            available_for_database = data["filesystem_free_bytes"] + data["files"]["database"] + data["files"]["wal"]
            projected_retained_bytes = rate * retention_days * 86400 if retention_days > 0 else None
            if projected_retained_bytes is not None and projected_retained_bytes <= available_for_database:
                data["retention_expected_to_limit_growth"] = True
            else:
                data["estimated_seconds_to_full"] = data["filesystem_free_bytes"] / rate
                data["retention_exceeds_remaining_space"] = (
                    retention_days > 0
                    and data["estimated_seconds_to_full"] < retention_days * 86400
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
        if result_path.is_file():
            try:
                info["last_operation"] = json.loads(result_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                pass
        return info

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
        temporary = request_path.with_suffix(".tmp")
        temporary.write_text(json.dumps({"action": action, "reference": reference, "confirmation": confirmation}, ensure_ascii=False), encoding="utf-8")
        os.replace(temporary, request_path)
        return {"status": "accepted", "action": action, "reference": reference}

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
                        "mode": "record" if item["key"] == "operating_status" else "hide" if item["key"] in hidden_live_cards else configured.get(item["key"], "record"),
                        "protected": item["key"] == "operating_status",
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
        requested["operating_status"] = "record"
        target["channels"] = {key: value for key, value in requested.items() if value in {"off", "live"}}
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

    @app.get("/api/v1/live-card-order")
    def live_card_order() -> dict[str, Any]:
        """Return the operator-defined order of the live measurement cards.

        This is a dashboard preference only: it deliberately does not create a
        collector request or affect Modbus polling and recording.
        """
        current = load_settings(config_path)
        order = current.get("web", {}).get("live_card_order", [])
        return {"order": order if isinstance(order, list) else []}

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
        return {
            "items": [
                enrich_sample(item, device_by_name[item["inverter"]].model) if device_by_name.get(item["inverter"], None) and device_by_name[item["inverter"]].decoder else item
                for item in repository.latest_samples()
                if item["metric"] in enabled.get(item["inverter"], set())
            ]
        }

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
        items = repository.history(metric, inverter, start_value, end_value, limit)
        decode = inverter in device_by_name and device_by_name[inverter].decoder
        model = device_by_name[inverter].model if inverter in device_by_name else "VF-AS1"
        return {"metric": metric, "inverter": inverter, "items": [enrich_sample(item, model) for item in items] if decode else items}

    @app.get("/api/v1/poll-cycles")
    def cycles(limit: Annotated[int, Query(ge=1, le=1000)] = 100) -> dict[str, Any]:
        return {"items": repository.poll_cycles(limit)}

    @app.get("/api/v1/diagnostics")
    def diagnostics() -> dict[str, Any]:
        return {
            "communication": repository.communication_diagnostics(60),
            "system": system_metrics(Path(config["storage"]["database"]), previous_cpu),
            "inverter_cpu_percent": None,
        }

    @app.get("/api/v1/export.csv")
    def export_csv(
        metric: Annotated[str | None, Query(max_length=80, pattern=r"^[A-Za-z0-9_.-]+$")] = None,
        inverter: Annotated[str | None, Query(max_length=120)] = None,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> StreamingResponse:
        start_value = parse_timestamp(start)
        end_value = parse_timestamp(end)
        if start_value and end_value and start_value > end_value:
            raise HTTPException(422, "start must not be later than end")

        def generate():
            buffer = io.StringIO()
            writer = csv.writer(buffer, lineterminator="\n")
            reference = repository.recording_info()["reference"]
            writer.writerow(("observed_at", "inverter", "slave_id", "metric", "register_address", "raw_value", "value", "unit", "investigation_reference"))
            yield buffer.getvalue()
            for row in repository.export_rows(metric, inverter, start_value, end_value, export_max_rows):
                buffer.seek(0)
                buffer.truncate(0)
                writer.writerow((*row, reference))
                yield buffer.getvalue()

        filename_part = re.sub(r"[^A-Za-z0-9_.-]+", "_", inverter or "all")
        filename = f"tmm-{filename_part}-{metric or 'all'}-{datetime.now(timezone.utc).date().isoformat()}.csv"
        return StreamingResponse(
            generate(),
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    @app.get("/", include_in_schema=False)
    def dashboard() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

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
