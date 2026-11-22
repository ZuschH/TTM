"""Linux-only field-I/O acquisition add-ons for TMM.

The module deliberately has no hard dependency on the Sequent packages.  A
configured card reports an actionable health error when its vendor driver is
missing; a TMM installation without add-ons behaves exactly as before.
"""

from __future__ import annotations

from dataclasses import dataclass
import importlib
import json
import math
from pathlib import Path
import time
from typing import Any, Callable


MULTIIO_INPUTS: dict[str, tuple[int, str, str]] = {
    # signal: (channel count, default engineering unit, vendor read method)
    "digital": (4, "on/off", "get_opto"),
    "voltage": (2, "V", "get_u_in"),
    "current": (2, "mA", "get_i_in"),
    "temperature": (2, "°C", "get_rtd_temp"),
    "frequency": (4, "Hz", "get_opto_frequency"),
    "duty_cycle": (4, "%", "get_opto_pwm_fill"),
    "counter": (4, "count", "get_opto_counter"),
}

SYSTEM_ADDON_METRICS: dict[str, dict[str, tuple[str, str]]] = {
    "sequent_super_watchdog": {
        "input_voltage": ("Input voltage", "V"), "raspberry_voltage": ("Raspberry Pi voltage", "V"),
        "battery_voltage": ("Battery voltage", "V"), "board_temperature": ("Board temperature", "°C"),
        "charge_status": ("Charge status", "raw"), "reset_count": ("Watchdog reset count", "count"),
    },
    "sequent_smart_fan": {
        "fan_power": ("Fan power", "%"), "stop_interval": ("Fan stop interval", "s"),
        "processor_temperature": ("Processor temperature", "°C"), "target_power": ("Requested fan power", "%"),
    },
}

# Header pins commonly left available when I²C, SPI and the primary UART are
# reserved for TMM or other HATs.  Configuration may deliberately use another
# BCM GPIO from 2..27, but setup offers this conflict-free set by default.
SAFE_GPIO_INPUTS = (4, 5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27)


class AddonConfigurationError(ValueError):
    """Raised when an add-on declaration is unsafe or ambiguous."""


@dataclass(frozen=True)
class AddonSample:
    metric: str
    raw_value: int
    value: float
    unit: str
    label: str
    record_history: bool = True
    history_threshold: float = 0.0


@dataclass(frozen=True)
class AddonDefinition:
    identifier: str
    kind: str
    stack: int
    interval_seconds: float
    label: str
    channels: tuple[dict[str, Any], ...]
    options: dict[str, Any]
    enabled: bool = True

    @property
    def source_name(self) -> str:
        return f"addon:{self.identifier}"


def configured_addons(config: dict[str, Any]) -> list[AddonDefinition]:
    """Validate optional Sequent card declarations.

    `stack` corresponds to the physical card address (0..7).  Names remain
    stable in the database, so changing a display label never breaks history.
    """
    entries = config.get("addons", [])
    if entries is None:
        return []
    if not isinstance(entries, list):
        raise AddonConfigurationError("addons must be a list")
    result: list[AddonDefinition] = []
    identifiers: set[str] = set()
    occupied: set[tuple[str, int]] = set()
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            continue
        enabled = bool(entry.get("enabled", True))
        kind = str(entry.get("type", "")).strip()
        if kind not in {"raspberry_pi_gpio", "sequent_16inpind", "sequent_24b8vin", "sequent_multiio", "sequent_super_watchdog", "sequent_smart_fan"}:
            raise AddonConfigurationError(f"addon {index}: unsupported type {kind!r}")
        identifier = str(entry.get("id", f"{kind}_{entry.get('stack', 0)}")).strip()
        if not identifier or any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for char in identifier):
            raise AddonConfigurationError(f"addon {index}: id must contain only letters, numbers, _ or -")
        if identifier in identifiers:
            raise AddonConfigurationError(f"duplicate addon id: {identifier}")
        stack = int(entry.get("stack", 0))
        if not 0 <= stack <= 7:
            raise AddonConfigurationError(f"addon {identifier}: stack must be between 0 and 7")
        if kind == "sequent_smart_fan" and stack not in {0, 1}:
            raise AddonConfigurationError(f"addon {identifier}: Smart Fan stack must be 0 or 1")
        if (kind, stack) in occupied:
            raise AddonConfigurationError(f"duplicate {kind} card at stack {stack}")
        interval = float(entry.get("interval_seconds", 0.02 if kind == "sequent_16inpind" else 0.05))
        if not 0.01 <= interval <= 60:
            raise AddonConfigurationError(f"addon {identifier}: interval_seconds must be between 0.01 and 60")
        channels = entry.get("channels", [])
        if not isinstance(channels, list):
            raise AddonConfigurationError(f"addon {identifier}: channels must be a list")
        channel_numbers: set[tuple[str, int]] = set()
        normalized: list[dict[str, Any]] = []
        for channel in channels:
            if not isinstance(channel, dict):
                raise AddonConfigurationError(f"addon {identifier}: invalid channel declaration")
            if kind in SYSTEM_ADDON_METRICS:
                metric = str(channel.get("metric", "")).strip()
                if metric not in SYSTEM_ADDON_METRICS[kind]:
                    raise AddonConfigurationError(f"addon {identifier}: unknown system metric {metric!r}")
                label = str(channel.get("label", "")).strip()
                if len(label) > 120:
                    raise AddonConfigurationError(f"addon {identifier}: channel label must be at most 120 characters")
                normalized_channel = dict(channel, metric=metric, enabled=bool(channel.get("enabled", True)), record=bool(channel.get("record", True)), live=bool(channel.get("live", True)))
                if label:
                    normalized_channel["label"] = label
                unit = str(channel.get("unit", "")).strip()
                if unit:
                    normalized_channel["unit"] = unit
                threshold = float(channel.get("change_threshold", 0.0))
                if not math.isfinite(threshold) or threshold < 0:
                    raise AddonConfigurationError(f"addon {identifier}: change_threshold must be finite and non-negative")
                normalized_channel["change_threshold"] = threshold
                normalized.append(normalized_channel)
                continue
            number = int(channel.get("channel", 0))
            signal = str(channel.get("signal", "")).strip().lower()
            if kind == "sequent_multiio":
                if signal not in MULTIIO_INPUTS:
                    raise AddonConfigurationError(f"addon {identifier}: Multi-IO channel requires a supported signal type")
                maximum = MULTIIO_INPUTS[signal][0]
            elif kind == "raspberry_pi_gpio":
                maximum = 27
                if not 2 <= number <= maximum:
                    raise AddonConfigurationError(f"addon {identifier}: BCM GPIO must be between 2 and 27")
            else:
                maximum = 16 if kind == "sequent_16inpind" else 8
            if not 1 <= number <= maximum:
                raise AddonConfigurationError(f"addon {identifier}: invalid channel {number}")
            channel_key = (signal, number) if kind == "sequent_multiio" else ("input", number)
            if channel_key in channel_numbers:
                raise AddonConfigurationError(f"addon {identifier}: duplicate channel {number}")
            channel_numbers.add(channel_key)
            label = str(channel.get("label", "")).strip()
            if len(label) > 120:
                raise AddonConfigurationError(f"addon {identifier}: channel label must be at most 120 characters")
            # ``live`` is deliberately independent from history recording:
            # an input may be stored for diagnostics without occupying a live
            # dashboard card.
            # Field inputs are opt-in.  A newly declared I/O card must not
            # silently increase bus/I²C traffic, fill the database, or crowd
            # the live view before the technician selects its purpose.
            default_enabled = kind not in {"raspberry_pi_gpio", "sequent_16inpind", "sequent_24b8vin", "sequent_multiio"}
            normalized_channel = dict(channel, channel=number, enabled=bool(channel.get("enabled", default_enabled)), record=bool(channel.get("record", default_enabled)), live=bool(channel.get("live", default_enabled)))
            if label:
                normalized_channel["label"] = label
            if kind == "sequent_24b8vin":
                # Retained as expected hardware documentation; TMM does not
                # write the gain to a field card.
                gain = int(channel.get("gain", 1))
                if not 0 <= gain <= 7:
                    raise AddonConfigurationError(f"addon {identifier}: gain for channel {number} must be between 0 and 7")
                normalized_channel["gain"] = gain
            if kind == "sequent_multiio":
                normalized_channel["signal"] = signal
            if kind == "raspberry_pi_gpio":
                pull = str(channel.get("pull", "down")).strip().lower()
                if pull not in {"up", "down", "none"}:
                    raise AddonConfigurationError(f"addon {identifier}: GPIO {number} pull must be up, down or none")
                normalized_channel["pull"] = pull
                normalized_channel["active_low"] = bool(channel.get("active_low", False))
            if kind in {"sequent_24b8vin", "sequent_multiio"}:
                for field, default in (("scale", 1.0), ("offset", 0.0)):
                    value = float(channel.get(field, default))
                    if not math.isfinite(value):
                        raise AddonConfigurationError(f"addon {identifier}: {field} must be finite")
                    normalized_channel[field] = value
                unit = str(channel.get("unit", "")).strip()
                if len(unit) > 24:
                    raise AddonConfigurationError(f"addon {identifier}: unit must be at most 24 characters")
                if unit:
                    normalized_channel["unit"] = unit
                decimals = int(channel.get("decimals", 3))
                if not 0 <= decimals <= 6:
                    raise AddonConfigurationError(f"addon {identifier}: decimals must be between 0 and 6")
                normalized_channel["decimals"] = decimals
                threshold = float(channel.get("change_threshold", 0.0))
                if not math.isfinite(threshold) or threshold < 0:
                    raise AddonConfigurationError(f"addon {identifier}: change_threshold must be finite and non-negative")
                normalized_channel["change_threshold"] = threshold
            normalized.append(normalized_channel)
        options: dict[str, Any] = {}
        if kind == "sequent_smart_fan":
            control = entry.get("control", {})
            if not isinstance(control, dict):
                raise AddonConfigurationError(f"addon {identifier}: Smart Fan control must be an object")
            options["control"] = normalize_fan_control(control)
        identifiers.add(identifier); occupied.add((kind, stack))
        result.append(AddonDefinition(identifier, kind, stack, interval, str(entry.get("label", identifier)), tuple(normalized), options, enabled))
    return result


def normalize_fan_control(control: dict[str, Any]) -> dict[str, Any]:
    """Validate the deliberate, small Smart-Fan control surface."""
    mode = str(control.get("mode", "monitor")).lower()
    if mode not in {"monitor", "automatic", "manual"}:
        raise AddonConfigurationError("Smart Fan mode must be monitor, automatic or manual")
    result = {"mode": mode}
    for key, default, low, high in (
        ("minimum_power_percent", 25.0, 0.0, 100.0),
        ("start_temperature_c", 45.0, 20.0, 100.0),
        ("full_temperature_c", 70.0, 25.0, 110.0),
        ("manual_power_percent", 25.0, 0.0, 100.0),
        ("failsafe_power_percent", 100.0, 0.0, 100.0),
    ):
        value = float(control.get(key, default))
        if not math.isfinite(value) or not low <= value <= high:
            raise AddonConfigurationError(f"Smart Fan {key} must be between {low:g} and {high:g}")
        result[key] = value
    if result["full_temperature_c"] <= result["start_temperature_c"]:
        raise AddonConfigurationError("Smart Fan full temperature must exceed start temperature")
    return result


class SequentAddon:
    """One physical board with lazy driver loading and stable metric names."""

    def __init__(self, definition: AddonDefinition, importer: Callable[[str], Any] = importlib.import_module, fan_policy_path: Path | None = None):
        self.definition = definition
        self.importer = importer
        self.driver: Any | None = None
        self.last_values: dict[str, float] = {}
        self.last_recorded: dict[str, float] = {}
        self.last_recorded_at: dict[str, float] = {}
        self.last_emit = 0.0
        self.fan_policy_path = fan_policy_path
        self.last_fan_power: float | None = None

    def _fan_control(self) -> dict[str, Any]:
        control = dict(self.definition.options.get("control", {}))
        if self.fan_policy_path:
            try:
                policies = json.loads(self.fan_policy_path.read_text(encoding="utf-8"))
                if isinstance(policies, dict) and isinstance(policies.get(self.definition.identifier), dict):
                    control.update(policies[self.definition.identifier])
            except (OSError, json.JSONDecodeError):
                pass
        return normalize_fan_control(control)

    @staticmethod
    def _cpu_temperature() -> float | None:
        for path in Path("/sys/class/thermal").glob("thermal_zone*/temp"):
            try:
                value = float(path.read_text(encoding="ascii").strip()) / 1000.0
                if -20.0 <= value <= 150.0:
                    return value
            except (OSError, ValueError):
                pass
        return None

    @staticmethod
    def _construct_board(factory: Any, **kwargs: Any) -> Any:
        """Instantiate a vendor board without leaking its bus on a failed probe.

        The 24-bit DAQ and Multi-IO vendor constructors open ``/dev/i2c-1``
        before probing their revision register.  On a missing/offline card the
        constructor raises without closing that newly opened descriptor.  TMM
        retains the partly initialized instance long enough to close it here.
        """
        # Keep lightweight test doubles and alternative factory-style vendor
        # APIs compatible; only normal Python classes can expose a partially
        # initialized instance after ``__init__`` raises.
        if not isinstance(factory, type):
            return factory(**kwargs)
        instance = factory.__new__(factory)
        try:
            factory.__init__(instance, **kwargs)
        except Exception:
            bus = getattr(instance, "bus", None)
            close = getattr(bus, "close", None)
            if callable(close):
                try:
                    close()
                except Exception:
                    pass
            raise
        return instance

    def close(self) -> None:
        """Release an open vendor I²C bus when a collector exits or reloads."""
        if isinstance(self.driver, dict):
            for device in self.driver.values():
                close = getattr(device, "close", None)
                if callable(close):
                    try:
                        close()
                    except Exception:
                        pass
            self.driver = None
            return
        bus = getattr(self.driver, "bus", None)
        close = getattr(bus, "close", None)
        if callable(close):
            try:
                close()
            except Exception:
                pass
        self.driver = None

    def _load(self) -> Any:
        if self.driver is not None:
            return self.driver
        if self.definition.kind == "raspberry_pi_gpio":
            module = self.importer("gpiozero")
            devices = {}
            for settings in self.definition.channels:
                if not settings.get("enabled", False):
                    continue
                pull = settings.get("pull", "down")
                devices[int(settings["channel"])] = module.DigitalInputDevice(
                    int(settings["channel"]),
                    pull_up={"up": True, "down": False, "none": None}[pull],
                    active_state=True if pull == "none" else None,
                )
            self.driver = devices
        elif self.definition.kind == "sequent_16inpind":
            self.driver = self.importer("lib16inpind")
        elif self.definition.kind == "sequent_24b8vin":
            module = self.importer("SM24b8vin")
            self.driver = self._construct_board(module.SM24b8vin, stack=self.definition.stack)
        elif self.definition.kind == "sequent_multiio":
            module = self.importer("multiio")
            self.driver = self._construct_board(module.SMmultiio, stack=self.definition.stack)
        elif self.definition.kind == "sequent_super_watchdog":
            self.driver = self.importer("wdt")
        else:
            self.driver = self.importer("sfan")
        return self.driver

    def poll(self) -> list[AddonSample]:
        driver = self._load()
        result: list[AddonSample] = []
        if self.definition.kind == "raspberry_pi_gpio":
            configured = {item["channel"]: item for item in self.definition.channels}
            for channel, device in driver.items():
                settings = configured[channel]
                pin = getattr(device, "pin", None)
                physical = bool(pin.state if pin is not None and hasattr(pin, "state") else device.value)
                active = int(not physical if settings.get("active_low", False) else physical)
                label = str(settings.get("label", f"GPIO {channel}"))
                result.append(AddonSample(f"addon.{self.definition.identifier}.gpio_{channel:02d}", active, float(active), "on/off", label, bool(settings.get("record", True))))
        elif self.definition.kind == "sequent_16inpind":
            bitmap = int(driver.readAll(self.definition.stack))
            configured = {item["channel"]: item for item in self.definition.channels}
            for channel in range(1, 17):
                settings = configured.get(channel, {"enabled": False})
                if not settings.get("enabled", True):
                    continue
                active = 1 if bitmap & (1 << (channel - 1)) else 0
                label = str(settings.get("label", f"DI {channel}"))
                result.append(AddonSample(f"addon.{self.definition.identifier}.input_{channel:02d}", active, float(active), "on/off", label, bool(settings.get("record", True))))
        elif self.definition.kind == "sequent_24b8vin":
            configured = {item["channel"]: item for item in self.definition.channels}
            for channel in range(1, 9):
                settings = configured.get(channel, {"enabled": False})
                if not settings.get("enabled", True):
                    continue
                voltage = float(driver.get_u_in(channel))
                multiplier = float(settings.get("scale", 1.0))
                offset = float(settings.get("offset", 0.0))
                value = voltage * multiplier + offset
                unit = str(settings.get("unit", "V"))
                label = str(settings.get("label", f"AI {channel}"))
                # 1 µunit preserves both the raw 24-bit voltage reading and the
                # configured engineering value in TMM's integer sample schema.
                result.append(AddonSample(f"addon.{self.definition.identifier}.input_{channel:02d}", round(value * 1_000_000), value, unit, label, bool(settings.get("record", True)), float(settings.get("change_threshold", 0.0))))
        elif self.definition.kind == "sequent_multiio":
            for settings in self.definition.channels:
                if not settings.get("enabled", True):
                    continue
                signal = settings["signal"]
                channel = settings["channel"]
                _, default_unit, method = MULTIIO_INPUTS[signal]
                value = float(getattr(driver, method)(channel))
                unit = str(settings.get("unit", default_unit))
                multiplier = float(settings.get("scale", 1.0))
                offset = float(settings.get("offset", 0.0))
                value = value * multiplier + offset
                active = 1 if signal == "digital" and value else 0
                raw = active if signal == "digital" else round(value * 1_000_000)
                label = str(settings.get("label", f"Multi-IO {signal} {channel}"))
                result.append(AddonSample(f"addon.{self.definition.identifier}.{signal}_{channel:02d}", raw, float(active) if signal == "digital" else value, unit, label, bool(settings.get("record", True)), float(settings.get("change_threshold", 0.0))))
        elif self.definition.kind == "sequent_super_watchdog":
            readings = (
                ("input_voltage", "Input voltage", "V", "getVin"),
                ("raspberry_voltage", "Raspberry Pi voltage", "V", "getVrasp"),
                ("battery_voltage", "Battery voltage", "V", "getVbat"),
                ("board_temperature", "Board temperature", "°C", "getTemp"),
                ("charge_status", "Charge status", "raw", "getChargeStat"),
                ("reset_count", "Watchdog reset count", "count", "getResetCount"),
            )
            configured = {str(item.get("metric")): item for item in self.definition.channels}
            for metric, default_label, unit, method in readings:
                settings = configured.get(metric, {"enabled": False, "record": False, "live": False})
                if not settings.get("enabled", True):
                    continue
                value = float(getattr(driver, method)())
                result.append(AddonSample(f"addon.{self.definition.identifier}.{metric}", round(value * 1_000_000), value, str(settings.get("unit", unit)), str(settings.get("label", default_label)), bool(settings.get("record", True)), float(settings.get("change_threshold", 0.0))))
        else:
            # Read-only integration: the Smart Fan's autonomous thermal
            # protection remains active and TMM never changes its power or
            # safety threshold without a separate, explicit control feature.
            # Older/reduced Smart-Fan revisions expose only power and Pi
            # temperature.  Unsupported optional registers must not make an
            # otherwise healthy card appear unavailable.
            readings = (
                ("fan_power", "Fan power", "%", "getPower"),
                ("stop_interval", "Fan stop interval", "s", "getStopInt"),
            )
            configured = {str(item.get("metric")): item for item in self.definition.channels}
            failures: list[Exception] = []
            for metric, label, unit, method in readings:
                settings = configured.get(metric, {"enabled": False, "record": False, "live": False})
                if not settings.get("enabled", True):
                    continue
                try:
                    value = float(getattr(driver, method)(self.definition.stack))
                except (AttributeError, OSError, RuntimeError, ValueError) as error:
                    failures.append(error)
                    continue
                result.append(AddonSample(f"addon.{self.definition.identifier}.{metric}", round(value * 1_000_000), value, str(settings.get("unit", unit)), str(settings.get("label", label)), bool(settings.get("record", True)), float(settings.get("change_threshold", 0.0))))
            temperature = self._cpu_temperature()
            temperature_settings = configured.get("processor_temperature", {"enabled": False, "record": False, "live": False})
            if temperature is not None and temperature_settings.get("enabled", True):
                result.append(AddonSample(f"addon.{self.definition.identifier}.processor_temperature", round(temperature * 1_000_000), temperature, str(temperature_settings.get("unit", "°C")), str(temperature_settings.get("label", "Processor temperature")), bool(temperature_settings.get("record", True)), float(temperature_settings.get("change_threshold", 0.0))))
            control = self._fan_control()
            target: float | None = None
            if control["mode"] == "manual":
                target = control["manual_power_percent"]
            elif control["mode"] == "automatic":
                if temperature is None:
                    target = control["failsafe_power_percent"]
                elif temperature <= control["start_temperature_c"]:
                    target = control["minimum_power_percent"]
                elif temperature >= control["full_temperature_c"]:
                    target = 100.0
                else:
                    span = control["full_temperature_c"] - control["start_temperature_c"]
                    target = control["minimum_power_percent"] + (100.0 - control["minimum_power_percent"]) * (temperature - control["start_temperature_c"]) / span
                target = round(target)
            if target is not None:
                if self.last_fan_power is None or abs(target - self.last_fan_power) >= 1:
                    written = getattr(driver, "setPower")(self.definition.stack, int(target))
                    if written != 1:
                        raise OSError("Smart Fan rejected the requested power")
                    self.last_fan_power = target
                settings = configured.get("target_power", {"enabled": False, "record": False, "live": False})
                if settings.get("enabled", True):
                    result.append(AddonSample(f"addon.{self.definition.identifier}.target_power", round(target * 1_000_000), target, str(settings.get("unit", "%")), str(settings.get("label", "Requested fan power")), bool(settings.get("record", True)), float(settings.get("change_threshold", 0.0))))
            if not result:
                if not any(bool(settings.get("enabled", False)) for settings in configured.values()):
                    return []
                detail = str(failures[-1]) if failures else "no supported measurements"
                raise OSError(f"Smart Fan did not return a supported measurement: {detail}")
        return result

    def changes(self, now: float | None = None) -> list[AddonSample]:
        """Return changed values, plus a one-second heartbeat for freshness."""
        now = time.monotonic() if now is None else now
        samples = self.poll()
        heartbeat = now - self.last_emit >= 1.0
        changed = [sample for sample in samples if heartbeat or self.last_values.get(sample.metric) != sample.value]
        result = []
        for sample in changed:
            previous = self.last_values.get(sample.metric)
            # Latest values retain a one-second heartbeat for a responsive UI;
            # history is only written after the configured engineering change.
            recorded = self.last_recorded.get(sample.metric)
            # Field inputs use their configured change threshold.  System
            # health values additionally receive a sparse heartbeat so a
            # steady fan or UPS still has a usable trend line.
            system_heartbeat = (
                self.definition.kind in {"sequent_super_watchdog", "sequent_smart_fan"}
                and now - self.last_recorded_at.get(sample.metric, float("-inf")) >= 60.0
            )
            record = sample.record_history and (
                recorded is None or abs(sample.value - recorded) >= sample.history_threshold or system_heartbeat
            )
            if record:
                self.last_recorded[sample.metric] = sample.value
                self.last_recorded_at[sample.metric] = now
            result.append(AddonSample(sample.metric, sample.raw_value, sample.value, sample.unit, sample.label, record, sample.history_threshold))
        for sample in samples:
            self.last_values[sample.metric] = sample.value
        if result:
            self.last_emit = now
        return result

    def reset_recording_baseline(self) -> None:
        """Force a complete initial state into a newly opened recording."""
        self.last_values.clear()
        self.last_recorded.clear()
        self.last_recorded_at.clear()
        self.last_emit = float("-inf")


def addon_metadata(definitions: list[AddonDefinition]) -> list[dict[str, Any]]:
    return [{"id": item.identifier, "type": item.kind, "stack": item.stack, "label": item.label, "enabled": item.enabled} for item in definitions]
