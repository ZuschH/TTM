#!/usr/bin/env python3
"""Per-user Windows notification-area controller for TMM."""

from __future__ import annotations

import ctypes
import json
import os
import subprocess
import tempfile
import threading
import time
import urllib.request
import webbrowser
from pathlib import Path
from tkinter import BooleanVar, StringVar, Tk, Toplevel, messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

import psutil
import pystray
import win32service
from PIL import Image, ImageDraw
from serial.tools import list_ports


APP_DIR = Path(__file__).resolve().parent
PROGRAM_DATA = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "TMM"
CONFIG_PATH = PROGRAM_DATA / "config.json"
SERVICE_NAME = "TMM"
SERVICE_AUTO = win32service.SERVICE_AUTO_START


def service_state() -> str:
    try:
        return psutil.win_service_get(SERVICE_NAME).status()
    except (psutil.Error, OSError):
        return "missing"


def service_is_automatic() -> bool:
    manager = service = None
    try:
        manager = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_CONNECT)
        service = win32service.OpenService(manager, SERVICE_NAME, win32service.SERVICE_QUERY_CONFIG)
        return win32service.QueryServiceConfig(service)[1] == SERVICE_AUTO
    except OSError:
        return False
    finally:
        if service:
            win32service.CloseServiceHandle(service)
        if manager:
            win32service.CloseServiceHandle(manager)


def elevate(command: str) -> bool:
    parameters = f'-NoProfile -NonInteractive -Command "{command}"'
    result = ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", parameters, None, 0)
    return result > 32


def icon_image(status: str) -> Image.Image:
    asset_names = {
        "running": "tmm-tray-16-healthy.png",
        "paused": "tmm-tray-16-warning.png",
        "stopped": "tmm-tray-16-stopped.png",
        "missing": "tmm-tray-16-error.png",
    }
    asset = APP_DIR / "static" / asset_names.get(status, asset_names["missing"])
    if asset.is_file():
        with Image.open(asset) as source:
            return source.convert("RGBA").resize((64, 64), Image.Resampling.NEAREST)
    color = {"running": "#54e6a5", "paused": "#f3c852", "stopped": "#9ca9a4"}.get(status, "#ef6464")
    image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((5, 5, 59, 59), radius=13, fill="#14201d", outline=color, width=4)
    draw.text((14, 17), "T", fill=color, stroke_width=1)
    draw.text((33, 17), "M", fill=color, stroke_width=1)
    return image


class ConfigDialog:
    def __init__(self, on_saved):
        self.on_saved = on_saved
        self.root = Tk()
        self.root.title("TMM configuration")
        self.root.geometry("690x550")
        self.root.minsize(620, 480)
        self.data = self._load()
        self.values: dict[str, StringVar | BooleanVar] = {}
        self._build()

    def _load(self) -> dict:
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("The JSON root must be an object.")
            return data
        except Exception as error:
            messagebox.showerror("TMM configuration", f"Could not load configuration:\n{error}")
            return {}

    def _value(self, key: str, value, boolean: bool = False):
        variable = BooleanVar(value=bool(value)) if boolean else StringVar(value=str(value))
        self.values[key] = variable
        return variable

    def _build(self):
        outer = ttk.Frame(self.root, padding=12)
        outer.pack(fill="both", expand=True)
        tabs = ttk.Notebook(outer)
        tabs.pack(fill="both", expand=True)
        connection = ttk.Frame(tabs, padding=12)
        sampling = ttk.Frame(tabs, padding=12)
        storage = ttk.Frame(tabs, padding=12)
        tabs.add(connection, text="Connection")
        tabs.add(sampling, text="Sampling")
        tabs.add(storage, text="Storage & web")

        serial = self.data.get("serial", {})
        inverter = (self.data.get("inverters") or [{}])[0]
        ports = [port.device for port in list_ports.comports()]
        self._row(connection, 0, "COM port", "serial.device", serial.get("device", "COM3"), ports)
        self._row(connection, 1, "Baud rate", "serial.baudrate", serial.get("baudrate", 19200), ["9600", "19200", "38400"])
        self._row(connection, 2, "Parity", "serial.parity", serial.get("parity", "E"), ["E", "N", "O"])
        self._row(connection, 3, "Timeout (seconds)", "serial.timeout", serial.get("timeout_seconds", 0.75))
        self._row(connection, 4, "Device name", "device.name", inverter.get("name", "VFAS1-4037PL"))
        self._row(connection, 5, "Model", "device.model", inverter.get("model", "VF-AS1"), ["VF-AS1", "VF-AS3J", "VF-S11", "VF-S15"])
        self._row(connection, 6, "Modbus address", "device.slave", inverter.get("slave_id", 1))
        enabled = self._value("device.enabled", inverter.get("enabled", True), True)
        ttk.Checkbutton(connection, text="Device enabled", variable=enabled).grid(row=7, column=1, sticky="w", pady=6)

        intervals = self.data.get("polling", {}).get("intervals", {})
        for row, (label, key, default) in enumerate((
            ("Fast interval (s)", "fast", 0.2), ("Normal interval (s)", "normal", 0.5),
            ("Diagnostic interval (s)", "diagnostic", 5.0), ("Information interval (s)", "information", 3600.0),
        )):
            self._row(sampling, row, label, f"interval.{key}", intervals.get(key, default))
        polling = self.data.get("polling", {})
        self._row(sampling, 4, "Retries", "polling.retries", polling.get("retries", 2))
        self._row(sampling, 5, "Retry delay (s)", "polling.retry_delay", polling.get("retry_delay_seconds", 0.15))

        store = self.data.get("storage", {})
        web = self.data.get("web", {})
        self._row(storage, 0, "Database", "storage.database", store.get("database", ""))
        self._row(storage, 1, "Retention (days)", "storage.retention", store.get("retention_days", 365))
        self._row(storage, 2, "Export maximum rows", "storage.export", store.get("export_max_rows", 250000))
        self._row(storage, 3, "Web port", "web.port", web.get("port", 8080))

        buttons = ttk.Frame(outer)
        buttons.pack(fill="x", pady=(12, 0))
        ttk.Button(buttons, text="Advanced JSON…", command=self._advanced).pack(side="left")
        ttk.Button(buttons, text="Cancel", command=self.root.destroy).pack(side="right")
        ttk.Button(buttons, text="Save", command=self._save).pack(side="right", padx=8)
        for page in (connection, sampling, storage):
            page.columnconfigure(1, weight=1)

    def _row(self, parent, row, label, key, value, choices=None):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=(0, 12), pady=6)
        variable = self._value(key, value)
        if choices:
            widget = ttk.Combobox(parent, textvariable=variable, values=choices)
        else:
            widget = ttk.Entry(parent, textvariable=variable)
        widget.grid(row=row, column=1, sticky="ew", pady=6)

    def _apply_form(self):
        def number(key, integer=False, minimum=None):
            raw = self.values[key].get().strip()
            value = int(raw) if integer else float(raw)
            if minimum is not None and value < minimum:
                raise ValueError(f"{key} must be at least {minimum}.")
            return value

        serial = self.data.setdefault("serial", {})
        serial["device"] = self.values["serial.device"].get().strip().upper()
        if not serial["device"].startswith("COM"):
            raise ValueError("The serial device must be a COM port.")
        serial["baudrate"] = number("serial.baudrate", True, 1)
        serial["parity"] = self.values["serial.parity"].get().strip().upper()
        serial["timeout_seconds"] = number("serial.timeout", minimum=0.01)
        devices = self.data.setdefault("inverters", [{}])
        if not devices:
            devices.append({})
        devices[0].update(name=self.values["device.name"].get().strip(), model=self.values["device.model"].get().strip(),
                          slave_id=number("device.slave", True, 1), enabled=bool(self.values["device.enabled"].get()))
        if devices[0]["slave_id"] > 247:
            raise ValueError("The Modbus address must be between 1 and 247.")
        polling = self.data.setdefault("polling", {})
        intervals = polling.setdefault("intervals", {})
        for key in ("fast", "normal", "diagnostic", "information"):
            intervals[key] = number(f"interval.{key}", minimum=0.01)
        polling["retries"] = number("polling.retries", True, 0)
        polling["retry_delay_seconds"] = number("polling.retry_delay", minimum=0)
        store = self.data.setdefault("storage", {})
        store["database"] = self.values["storage.database"].get().strip()
        store["retention_days"] = number("storage.retention", True, 1)
        store["export_max_rows"] = number("storage.export", True, 1)
        self.data.setdefault("web", {})["port"] = number("web.port", True, 1)
        if self.data["web"]["port"] > 65535:
            raise ValueError("The web port must be between 1 and 65535.")

    def _advanced(self):
        window = Toplevel(self.root)
        window.title("Advanced JSON")
        window.geometry("760x650")
        editor = ScrolledText(window, wrap="none", font=("Consolas", 10), undo=True)
        editor.pack(fill="both", expand=True, padx=10, pady=10)
        editor.insert("1.0", json.dumps(self.data, indent=2, ensure_ascii=False))
        def save_json():
            try:
                parsed = json.loads(editor.get("1.0", "end"))
                if not isinstance(parsed, dict):
                    raise ValueError("The JSON root must be an object.")
                self._persist(parsed)
                window.destroy()
                self.root.destroy()
            except Exception as error:
                messagebox.showerror("Invalid JSON", str(error), parent=window)
        ttk.Button(window, text="Save", command=save_json).pack(pady=(0, 10))

    def _save(self):
        try:
            self._apply_form()
            self._persist(self.data)
            self.root.destroy()
        except Exception as error:
            messagebox.showerror("Invalid configuration", str(error), parent=self.root)

    def _persist(self, data: dict):
        payload = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        json.loads(payload)
        handle, temporary = tempfile.mkstemp(prefix="tmm-config-", suffix=".json")
        os.close(handle)
        Path(temporary).write_text(payload, encoding="utf-8")
        source = temporary.replace("'", "''")
        target = str(CONFIG_PATH).replace("'", "''")
        command = (
            f"Copy-Item -LiteralPath '{target}' -Destination '{target}.bak' -Force; "
            f"Copy-Item -LiteralPath '{source}' -Destination '{target}' -Force; "
            f"Remove-Item -LiteralPath '{source}' -Force; Restart-Service -Name TMM"
        )
        if not elevate(command):
            raise RuntimeError("Administrator approval was cancelled.")
        self.on_saved()

    def run(self):
        self.root.mainloop()


class TrayApp:
    def __init__(self):
        self.icon = pystray.Icon("TMM", icon_image("stopped"), "Toshiba Modbus Monitor")
        self.icon.menu = pystray.Menu(
            pystray.MenuItem(self.status_label, None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Open dashboard", self.open_dashboard, default=True),
            pystray.MenuItem("Start", self.start, enabled=lambda _item: service_state() != "running"),
            pystray.MenuItem("Stop", self.stop, enabled=lambda _item: service_state() == "running"),
            pystray.MenuItem("Start with Windows", self.toggle_automatic, checked=lambda _item: service_is_automatic()),
            pystray.MenuItem("Configuration…", self.configuration),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit tray", self.exit),
        )

    def status_label(self, _item=None):
        return f"Status: {service_state().capitalize()}"

    def open_dashboard(self, _icon=None, _item=None):
        webbrowser.open("http://localhost:8080/")

    def start(self, _icon=None, _item=None):
        elevate("Start-Service -Name TMM")

    def stop(self, _icon=None, _item=None):
        elevate("Stop-Service -Name TMM -Force")

    def toggle_automatic(self, _icon=None, _item=None):
        start_type = "Manual" if service_is_automatic() else "Automatic"
        elevate(f"Set-Service -Name TMM -StartupType {start_type}")

    def configuration(self, _icon=None, _item=None):
        threading.Thread(target=lambda: ConfigDialog(self.refresh).run(), daemon=True).start()

    def refresh(self):
        self.icon.update_menu()

    def exit(self, _icon=None, _item=None):
        self.icon.stop()

    def watch(self):
        previous = None
        while self.icon.visible:
            state = service_state()
            healthy = False
            if state == "running":
                try:
                    with urllib.request.urlopen("http://127.0.0.1:8080/api/v1/health", timeout=1.5) as response:
                        health = json.load(response)
                        healthy = response.status == 200 and health.get("status") == "healthy"
                except Exception:
                    pass
            display = "running" if healthy else ("paused" if state == "running" else state)
            if display != previous:
                self.icon.icon = icon_image(display)
                self.icon.title = f"Toshiba Modbus Monitor — {state}"
                self.icon.update_menu()
                previous = display
            time.sleep(3)

    def run(self):
        def setup(icon):
            icon.visible = True
            threading.Thread(target=self.watch, daemon=True).start()
        self.icon.run(setup=setup)


if __name__ == "__main__":
    TrayApp().run()
