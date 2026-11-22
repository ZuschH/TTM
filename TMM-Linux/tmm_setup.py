#!/usr/bin/env python3
"""Dialog editor for TMM field-I/O sources and their input channels."""

from __future__ import annotations

import argparse
import copy
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Any

from tmm_addons import MULTIIO_INPUTS, SAFE_GPIO_INPUTS, SYSTEM_ADDON_METRICS, configured_addons


CARDS = {
    "raspberry_pi_gpio": ("Raspberry Pi GPIO screw-terminal HAT", "pi_gpio", "Raspberry Pi digital inputs", 0.05),
    "sequent_16inpind": ("16 LV Digital Inputs", "field_di", "External digital inputs", 0.02),
    "sequent_24b8vin": ("8 x 24-Bit Analog Inputs", "field_ai", "External analog inputs", 0.05),
    "sequent_multiio": ("Multi-IO", "field_multiio", "External Multi-IO", 0.05),
    "sequent_smart_fan": ("Smart Fan", "system_fan", "System cooling", 2.0),
    "sequent_super_watchdog": ("Super Watchdog & UPS", "system_ups", "System UPS & watchdog", 1.0),
}
INVERTER_MODELS = ("VF-AS1", "VF-AS3J", "VF-S11", "VF-S15")


class Cancelled(Exception):
    pass


def dialog(*args: str, allow_cancel: bool = False) -> str:
    result = subprocess.run(["dialog", "--stdout", "--title", "TMM · Setup", *args], text=True, capture_output=True)
    if result.returncode and not allow_cancel:
        raise Cancelled
    return result.stdout.strip()


def menu(prompt: str, choices: list[tuple[str, str]], default: str = "") -> str:
    prefix = ["--default-item", default] if default else []
    flat = [value for pair in choices for value in pair]
    return dialog(*prefix, "--menu", prompt, "23", "94", "16", *flat)


def checklist(prompt: str, choices: list[tuple[str, str, bool]]) -> set[str]:
    flat = [value for tag, label, selected in choices for value in (tag, label, "on" if selected else "off")]
    return {line.strip().strip('"') for line in dialog("--separate-output", "--checklist", prompt, "25", "100", "18", *flat).splitlines() if line.strip()}


def inputbox(prompt: str, default: Any = "") -> str:
    return dialog("--inputbox", prompt, "10", "88", str(default))


def yesno(prompt: str, default: bool = True) -> bool:
    args = [] if default else ["--defaultno"]
    return subprocess.run(["dialog", "--title", "TMM · Setup", *args, "--yesno", prompt, "12", "90"]).returncode == 0


def message(text: str) -> None:
    subprocess.run(["dialog", "--title", "TMM · Setup", "--msgbox", text, "20", "96"])


def mode(channel: dict[str, Any]) -> str:
    if not channel.get("enabled", False): return "off"
    return "record" if channel.get("record", True) else "live"


def set_mode(channel: dict[str, Any], value: str) -> None:
    channel.update(enabled=value != "off", live=value != "off", record=value == "record")


def channel_key(channel: dict[str, Any]) -> str:
    if channel.get("metric"): return str(channel["metric"])
    return f"{channel.get('signal', 'input')}:{int(channel['channel'])}"


def default_channels(kind: str) -> list[dict[str, Any]]:
    if kind in SYSTEM_ADDON_METRICS:
        return [{"metric": metric, "label": label, "unit": unit, "change_threshold": 0.0, "enabled": False, "live": False, "record": False} for metric, (label, unit) in SYSTEM_ADDON_METRICS[kind].items()]
    if kind == "raspberry_pi_gpio":
        return [{"channel": pin, "label": f"GPIO {pin}", "pull": "down", "active_low": False, "enabled": False, "live": False, "record": False} for pin in SAFE_GPIO_INPUTS]
    if kind == "sequent_16inpind":
        return [{"channel": n, "label": f"Digital input {n}", "enabled": False, "live": False, "record": False} for n in range(1, 17)]
    if kind == "sequent_24b8vin":
        return [{"channel": n, "label": f"Analog input {n}", "gain": 1, "scale": 1.0, "offset": 0.0, "unit": "V", "decimals": 3, "change_threshold": 0.0, "enabled": False, "live": False, "record": False} for n in range(1, 9)]
    if kind == "sequent_multiio":
        result = []
        for signal, (count, unit, _method) in MULTIIO_INPUTS.items():
            result.extend({"signal": signal, "channel": n, "label": f"{signal.replace('_', ' ').title()} {n}", "scale": 1.0, "offset": 0.0, "unit": unit, "decimals": 3, "change_threshold": 0.0, "enabled": False, "live": False, "record": False} for n in range(1, count + 1))
        return result
    return []


def complete_channels(card: dict[str, Any]) -> list[dict[str, Any]]:
    kind = str(card["type"])
    defaults = default_channels(kind)
    existing = {channel_key(item): item for item in card.get("channels", []) if isinstance(item, dict) and ("channel" in item or "metric" in item)}
    return [dict(item, **existing.get(channel_key(item), {})) for item in defaults]


def new_card(kind: str) -> dict[str, Any]:
    _title, identifier, label, interval = CARDS[kind]
    result: dict[str, Any] = {"id": identifier, "type": kind, "label": label, "stack": 0, "interval_seconds": interval, "enabled": False, "channels": default_channels(kind)}
    if kind == "sequent_smart_fan":
        result["control"] = {"mode": "monitor", "minimum_power_percent": 25, "start_temperature_c": 45, "full_temperature_c": 70, "manual_power_percent": 25, "failsafe_power_percent": 100}
    return result


def edit_channels(card: dict[str, Any]) -> None:
    kind = str(card["type"])
    channels = complete_channels(card)
    card["channels"] = channels
    chosen = checklist("Select each channel to enable. Disabled channels retain their settings.", [(channel_key(item), f"{channel_key(item):18} {mode(item):6} · {item.get('label', '')}", bool(item.get("enabled"))) for item in channels])
    for item in channels:
        if channel_key(item) not in chosen:
            set_mode(item, "off")
            continue
        item["label"] = inputbox(f"{channel_key(item)} · display label", item.get("label", channel_key(item)))
        selected_mode = menu(f"{item['label']} · usage", [("live", "Live view only"), ("record", "Live view and SQLite history"), ("off", "Disabled")], mode(item) if mode(item) != "off" else "record")
        set_mode(item, selected_mode)
        if selected_mode == "off": continue
        if kind == "raspberry_pi_gpio":
            item["pull"] = menu("Internal resistor", [("down", "Pull-down (open input = 0)"), ("up", "Pull-up (open input = 1)"), ("none", "No internal resistor")], str(item.get("pull", "down")))
            item["active_low"] = yesno("Invert this input (LOW is active)?", bool(item.get("active_low", False)))
        if kind == "sequent_24b8vin":
            item["gain"] = int(inputbox("Documented hardware gain (0-7; TMM does not write it)", item.get("gain", 1)))
        if kind in {"sequent_24b8vin", "sequent_multiio"}:
            item["scale"] = float(inputbox("Engineering scale multiplier", item.get("scale", 1)))
            item["offset"] = float(inputbox("Engineering offset", item.get("offset", 0)))
            item["unit"] = inputbox("Engineering unit", item.get("unit", ""))
            item["decimals"] = int(inputbox("Displayed decimal places (0-6)", item.get("decimals", 3)))
            item["change_threshold"] = float(inputbox("SQLite change threshold", item.get("change_threshold", 0)))


def edit_card(card: dict[str, Any]) -> None:
    kind = str(card["type"]); title = CARDS[kind][0]
    while True:
        choices = [("identity", "Card ID and display label"), ("stack", "Polling interval" if kind == "raspberry_pi_gpio" else "Stack address and polling interval")]
        choices.append(("channels", "Configure individual channels"))
        if kind == "sequent_smart_fan": choices.append(("fan", "Cooling policy"))
        choices.append(("back", "Back"))
        location = "BCM GPIO header" if kind == "raspberry_pi_gpio" else f"Stack: {card.get('stack', 0)}"
        choice = menu(f"{title}\n\nID: {card.get('id')}\nLabel: {card.get('label')}\n{location}\nInterval: {card.get('interval_seconds')} s", choices)
        if choice == "back": return
        if choice == "identity":
            card["id"] = inputbox("Stable card ID (letters, numbers, _ and -)", card.get("id", CARDS[kind][1]))
            card["label"] = inputbox("Display label", card.get("label", title))
        elif choice == "stack":
            if kind not in {"sequent_super_watchdog", "raspberry_pi_gpio"}: card["stack"] = int(inputbox(f"Stack address (0-{'1' if kind == 'sequent_smart_fan' else '7'})", card.get("stack", 0)))
            else: card["stack"] = 0
            card["interval_seconds"] = float(inputbox("Polling interval in seconds", card.get("interval_seconds", CARDS[kind][3])))
        elif choice == "channels": edit_channels(card)
        elif choice == "fan":
            control = card.setdefault("control", {})
            control["mode"] = menu("Cooling mode", [("monitor", "Monitor only"), ("automatic", "Automatic"), ("manual", "Manual")], str(control.get("mode", "monitor")))
            for key, label, default in (("minimum_power_percent", "Minimum power (%)", 25), ("start_temperature_c", "Start temperature (°C)", 45), ("full_temperature_c", "Full-speed temperature (°C)", 70), ("manual_power_percent", "Manual power (%)", 25), ("failsafe_power_percent", "Failsafe power (%)", 100)):
                control[key] = float(inputbox(label, control.get(key, default)))


def validate_config(config: dict[str, Any]) -> None:
    configured_addons(config)
    identifiers = [str(item.get("id", "")) for item in config.get("addons", []) if isinstance(item, dict)]
    if len(identifiers) != len(set(identifiers)): raise ValueError("Every Sequent card needs a unique ID")
    bridge = config.get("communication_bridge", {})
    if isinstance(bridge, dict) and isinstance(bridge.get("scheduled_polling"), dict):
        scheduled = bridge["scheduled_polling"]
        if scheduled.get("enabled", False):
            if float(scheduled.get("idle_guard_seconds", 0.02)) < 0.005: raise ValueError("Proxy idle guard must be at least 0.005 seconds")
            if not 0.02 <= float(scheduled.get("response_timeout_seconds", 0.1)) <= 0.25: raise ValueError("Proxy poll timeout must be between 0.02 and 0.25 seconds")
            if float(scheduled.get("minimum_gap_seconds", 0.02)) < 0.005: raise ValueError("Proxy poll gap must be at least 0.005 seconds")


def save(path: Path, config: dict[str, Any]) -> Path:
    validate_config(config)
    backup = path.with_name(f"{path.name}.before-setup-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    shutil.copy2(path, backup)
    stat = path.stat()
    with tempfile.NamedTemporaryFile("w", dir=path.parent, prefix=".tmm-setup-", encoding="utf-8", delete=False) as handle:
        json.dump(config, handle, ensure_ascii=False, indent=2); handle.write("\n"); temporary = Path(handle.name)
    os.chmod(temporary, stat.st_mode)
    try: os.chown(temporary, stat.st_uid, stat.st_gid)
    except PermissionError: pass
    os.replace(temporary, path)
    return backup


def serial_adapters() -> list[str]:
    directory = Path("/dev/serial/by-id")
    return sorted(str(path) for path in directory.iterdir() if path.is_symlink()) if directory.is_dir() else []


def existing_buses(config: dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(config.get("serial_buses"), list):
        return [copy.deepcopy(item) for item in config["serial_buses"] if isinstance(item, dict)]
    legacy = copy.deepcopy(config.get("serial", {}))
    return [{"id": "default", **legacy}] if legacy else []


def run_proxy(path: Path) -> int:
    config = json.loads(path.read_text(encoding="utf-8"))
    adapters = serial_adapters()
    if len(adapters) < 2:
        message("Proxy operation requires two different adapters below /dev/serial/by-id.\n\nConnect both adapters and run setup again.")
        return 1
    current = config.get("communication_bridge", {})
    if not isinstance(current, dict): current = {}
    hmi_old = current.get("hmi_port", {}) if isinstance(current.get("hmi_port"), dict) else {}
    drive_old = current.get("drive_port", {}) if isinstance(current.get("drive_port"), dict) else {}
    choices = [(device, Path(device).name) for device in adapters]
    hmi_device = menu("Adapter connected to the HMI / master", choices, str(hmi_old.get("device", adapters[0])))
    remaining = [(device, label) for device, label in choices if device != hmi_device]
    drive_default = str(drive_old.get("device", remaining[0][0]))
    if drive_default == hmi_device or drive_default not in {item[0] for item in remaining}: drive_default = remaining[0][0]
    drive_device = menu("Adapter connected to the inverter / slave", remaining, drive_default)
    baudrate = int(menu("Modbus baud rate on both sides", [(str(value), str(value)) for value in (9600, 19200, 38400)], str(hmi_old.get("baudrate", 19200))))
    parity = menu("Parity on both sides", [(value, value) for value in ("E", "N", "O")], str(hmi_old.get("parity", "E")))
    response_timeout = float(inputbox("Maximum inverter response time in seconds", current.get("response_timeout_seconds", 0.75)))
    enabled = yesno("Enable transparent proxy mode now?\n\nHMI telegrams have absolute priority. TMM observes matching HMI reads passively and sends no independent Modbus requests.", True)
    scheduled_old = current.get("scheduled_polling", {}) if isinstance(current.get("scheduled_polling"), dict) else {}
    scheduled_enabled = False
    idle_guard = float(scheduled_old.get("idle_guard_seconds", 0.02))
    poll_timeout = float(scheduled_old.get("response_timeout_seconds", 0.1))
    minimum_gap = float(scheduled_old.get("minimum_gap_seconds", 0.02))
    bridge = {
        **current, "enabled": enabled, "mode": "transparent_proxy",
        "response_timeout_seconds": response_timeout, "idle_read_timeout_seconds": 0.1,
        "scheduled_polling": {"enabled": scheduled_enabled, "passive_decode": True,
                              "idle_guard_seconds": idle_guard,
                              "response_timeout_seconds": poll_timeout, "minimum_gap_seconds": minimum_gap},
        "hmi_port": {"device": hmi_device, "baudrate": baudrate, "parity": parity, "stopbits": 1, "bytesize": 8},
        "drive_port": {"device": drive_device, "baudrate": baudrate, "parity": parity, "stopbits": 1, "bytesize": 8},
    }
    review = (f"Mode: {'ENABLED' if enabled else 'disabled'}\n"
              f"HMI: {hmi_device}\nDrive: {drive_device}\nFormat: {baudrate} 8{parity}1\n"
              f"Response timeout: {response_timeout:g} s\n"
              "Passive adoption of matching HMI read values: ENABLED\n"
              "Independent TMM polling: DISABLED (HMI-priority mode)")
    if not yesno("Review transparent proxy configuration:\n\n" + review + "\n\nBack up and save?", False): return 0
    config["communication_bridge"] = bridge
    backup = save(path, config)
    message(f"Proxy configuration saved.\n\nBackup: {backup}\n\nRestart both TMM services to apply it.")
    return 0


def run_serial(path: Path) -> int:
    config = json.loads(path.read_text(encoding="utf-8"))
    current = existing_buses(config)
    detected = serial_adapters()
    if not detected:
        message("No stable serial adapter was found below /dev/serial/by-id.\n\nConnect the adapters and run setup again.")
        return 1
    selected = checklist(
        "Select every USB-to-serial adapter TMM may use. Stable by-id paths are stored; ttyUSB numbers are never saved.",
        [(str(index), Path(device).name, any(bus.get("device") == device for bus in current)) for index, device in enumerate(detected)],
    )
    chosen = [device for index, device in enumerate(detected) if str(index) in selected]
    if not chosen:
        message("At least one serial adapter must be selected.")
        return 1
    buses: list[dict[str, Any]] = []
    used_ids: set[str] = set()
    for index, device in enumerate(chosen, 1):
        old = next((item for item in current if item.get("device") == device), {})
        identifier = inputbox(f"Bus ID for\n{device}", old.get("id", f"bus{index}"))
        if not identifier.replace("_", "").replace("-", "").isalnum() or identifier in used_ids:
            raise ValueError(f"Invalid or duplicate bus ID: {identifier}")
        baudrate = int(menu(f"{identifier} · baud rate", [(str(value), str(value)) for value in (9600, 19200, 38400)], str(old.get("baudrate", 19200))))
        parity = menu(f"{identifier} · parity", [(value, value) for value in ("E", "N", "O")], str(old.get("parity", "E")))
        timeout = float(inputbox(f"{identifier} · response timeout in seconds", old.get("timeout_seconds", 0.75)))
        buses.append({"id": identifier, "device": device, "baudrate": baudrate, "parity": parity,
                      "stopbits": 1, "bytesize": 8, "timeout_seconds": timeout})
        used_ids.add(identifier)
    old_inverters = [copy.deepcopy(item) for item in config.get("inverters", []) if isinstance(item, dict)]
    count = int(inputbox("Number of configured inverters (1-3)", min(3, max(1, len(old_inverters)))))
    if not 1 <= count <= 3:
        raise ValueError("TMM supports one to three configured inverters")
    inverters: list[dict[str, Any]] = []
    names: set[str] = set(); addresses: set[tuple[str, int]] = set()
    for index in range(count):
        old = old_inverters[index] if index < len(old_inverters) else {}
        enabled = yesno(f"Enable inverter {index + 1}?", bool(old.get("enabled", True)))
        name = inputbox(f"Inverter {index + 1} · unique display name", old.get("name", f"Drive {index + 1}"))
        model = menu(f"{name} · model", [(value, value) for value in INVERTER_MODELS], str(old.get("model", "VF-AS3J")))
        old_bus_id = str(old.get("bus_id", buses[0]["id"]))
        default_bus_id = old_bus_id if old_bus_id in used_ids else buses[0]["id"]
        bus_id = menu(f"{name} · serial bus", [(bus["id"], Path(bus["device"]).name) for bus in buses], default_bus_id)
        slave_id = int(inputbox(f"{name} · Modbus slave address (1-247)", old.get("slave_id", 1)))
        if not name.strip() or name in names: raise ValueError(f"Invalid or duplicate inverter name: {name}")
        if not 1 <= slave_id <= 247: raise ValueError(f"Invalid slave address for {name}")
        if enabled and (bus_id, slave_id) in addresses: raise ValueError(f"Duplicate slave {slave_id} on bus {bus_id}")
        updated = old | {"name": name.strip(), "model": model, "bus_id": bus_id, "slave_id": slave_id, "enabled": enabled}
        updated.setdefault("channels", {})
        inverters.append(updated); names.add(name); addresses.add((bus_id, slave_id))
    if not any(item["enabled"] for item in inverters):
        raise ValueError("At least one inverter must be enabled")
    review = [f"{bus['id']}: {bus['device']} · {bus['baudrate']} 8{bus['parity']}{bus['stopbits']}" for bus in buses]
    review += [f"{'ON ' if item['enabled'] else 'OFF'} {item['name']} · {item['model']} · {item['bus_id']}:{item['slave_id']}" for item in inverters]
    if not yesno("Review serial topology:\n\n" + "\n".join(review) + "\n\nBack up and save?", False): return 0
    config["serial_buses"] = buses
    config["serial"] = {key: value for key, value in buses[0].items() if key != "id"}
    config["inverters"] = inverters
    backup = save(path, config)
    message(f"Serial topology saved.\n\nBackup: {backup}\n\nRestart both TMM services to apply it.")
    return 0


def run(path: Path) -> int:
    original = json.loads(path.read_text(encoding="utf-8")); config = copy.deepcopy(original)
    addons = [item for item in config.setdefault("addons", []) if isinstance(item, dict)]
    by_type = {str(item.get("type")): item for item in addons}
    for kind in CARDS:
        if kind not in by_type:
            by_type[kind] = new_card(kind); addons.append(by_type[kind])
    config["addons"] = addons
    chosen = checklist("Enable or disable every supported field-I/O source independently:", [(kind, title, bool(by_type[kind].get("enabled"))) for kind, (title, *_rest) in CARDS.items()])
    for kind, card in by_type.items():
        if kind in CARDS: card["enabled"] = kind in chosen
    while True:
        choice = menu("Select a source for individual configuration. No change is written before Review and save.", [(kind, f"{'ON ' if by_type[kind].get('enabled') else 'OFF'} · {CARDS[kind][0]} · {'BCM GPIO' if kind == 'raspberry_pi_gpio' else 'stack ' + str(by_type[kind].get('stack', 0))} · {sum(bool(ch.get('enabled')) for ch in by_type[kind].get('channels', []))} channels") for kind in CARDS] + [("review", "Review and save"), ("cancel", "Exit without saving")])
        if choice == "cancel": return 0
        if choice != "review": edit_card(by_type[choice]); continue
        try: validate_config(config)
        except Exception as error: message(f"Configuration is invalid:\n\n{error}"); continue
        lines = [f"{'ENABLED ' if by_type[k].get('enabled') else 'disabled'} · {CARDS[k][0]} · {'BCM GPIO' if k == 'raspberry_pi_gpio' else 'stack ' + str(by_type[k].get('stack', 0))} · {sum(bool(ch.get('enabled')) for ch in by_type[k].get('channels', []))} channels" for k in CARDS]
        if not yesno("Review:\n\n" + "\n".join(lines) + "\n\nBack up and save these settings?", False): continue
        backup = save(path, config)
        message(f"Field-I/O configuration saved.\n\nBackup: {backup}\n\nDriver reconciliation and service restart follow in setup.sh.")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--config", type=Path, required=True); parser.add_argument("--serial", action="store_true"); parser.add_argument("--proxy", action="store_true"); args = parser.parse_args()
    if os.geteuid() != 0: raise SystemExit("Please run with sudo")
    if not shutil.which("dialog"): raise SystemExit("dialog is not installed")
    try: return run_proxy(args.config) if args.proxy else (run_serial(args.config) if args.serial else run(args.config))
    except Cancelled: return 0
    except (OSError, ValueError, json.JSONDecodeError) as error: message(f"Setup stopped:\n\n{error}"); return 1


if __name__ == "__main__": raise SystemExit(main())
