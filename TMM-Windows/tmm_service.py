#!/usr/bin/env python3
"""Windows Service supervisor for the TMM collector and web server."""

from __future__ import annotations

import os
import subprocess
import threading
from pathlib import Path

import servicemanager
import psutil
import win32event
import win32service
import win32serviceutil


APP_DIR = Path(__file__).resolve().parent
PROGRAM_DATA = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "TMM"
CONFIG_PATH = Path(os.environ.get("TMM_CONFIG", str(PROGRAM_DATA / "config.json")))
LOG_DIR = PROGRAM_DATA / "logs"
PRIVATE_PYTHON_EXE = APP_DIR / "runtime" / "python.exe"
LEGACY_PYTHON_EXE = APP_DIR / ".venv" / "Scripts" / "python.exe"
PYTHON_EXE = PRIVATE_PYTHON_EXE if PRIVATE_PYTHON_EXE.is_file() else LEGACY_PYTHON_EXE


class TMMService(win32serviceutil.ServiceFramework):
    _svc_name_ = "TMM"
    _svc_display_name_ = "Toshiba Modbus Monitor"
    _svc_description_ = "Read-only Toshiba Modbus RTU monitoring and web dashboard"

    def __init__(self, args: list[str]):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.resume_event = threading.Event()
        self.suspended = threading.Event()
        self.process_lock = threading.RLock()
        self.processes: list[tuple[str, subprocess.Popen[bytes], object]] = []

    def GetAcceptedControls(self) -> int:
        return super().GetAcceptedControls() | win32service.SERVICE_ACCEPT_POWEREVENT

    def SvcOtherEx(self, control: int, event_type: int, data: object) -> None:
        if control != win32service.SERVICE_CONTROL_POWEREVENT:
            return
        if event_type == 4:  # PBT_APMSUSPEND
            self.suspended.set()
            servicemanager.LogInfoMsg("TMM preparing collector for Windows suspend")
            self._stop_child("collector")
            servicemanager.LogInfoMsg("TMM collector stopped before Windows suspend")
        elif event_type in (7, 18):  # PBT_APMRESUMESUSPEND / PBT_APMRESUMEAUTOMATIC
            servicemanager.LogInfoMsg(f"TMM received Windows resume event {event_type}")
            self.resume_event.set()

    def SvcStop(self) -> None:
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self._stop_children()

    def SvcDoRun(self) -> None:
        servicemanager.LogInfoMsg("TMM service starting")
        try:
            self._start_children()
            while win32event.WaitForSingleObject(self.stop_event, 1000) == win32event.WAIT_TIMEOUT:
                if self.resume_event.is_set():
                    self.resume_event.clear()
                    self.suspended.clear()
                    servicemanager.LogInfoMsg("TMM restarting after Windows resume")
                    self._stop_children()
                    if win32event.WaitForSingleObject(self.stop_event, 5000) != win32event.WAIT_TIMEOUT:
                        break
                    self._start_children()
                with self.process_lock:
                    failed = next(((name, process) for name, process, _log in self.processes if process.poll() is not None), None)
                if failed is not None:
                    name, process = failed
                    servicemanager.LogWarningMsg(
                        f"TMM {name} process exited with code {process.returncode}; restarting child"
                    )
                    delay_ms = 30000 if name == "collector" and process.returncode == 75 else 5000
                    self._restart_child(name, delay_ms=delay_ms)
        except Exception as error:
            servicemanager.LogErrorMsg(f"TMM service failed: {error}")
            raise
        finally:
            self._stop_children()
            servicemanager.LogInfoMsg("TMM service stopped")

    def _start_children(self) -> None:
        if not CONFIG_PATH.is_file():
            raise FileNotFoundError(f"configuration not found: {CONFIG_PATH}")
        if not PYTHON_EXE.is_file():
            raise FileNotFoundError(f"virtual-environment Python not found: {PYTHON_EXE}")
        for name in ("collector", "web"):
            self._start_child(name)

    def _start_child(self, name: str) -> None:
        with self.process_lock:
            if name == "collector" and self.suspended.is_set():
                return
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            commands = {
                "collector": [str(PYTHON_EXE), str(APP_DIR / "tmm_monitor.py"), "--config", str(CONFIG_PATH)],
                "web": [str(PYTHON_EXE), str(APP_DIR / "tmm_web.py"), "--config", str(CONFIG_PATH)],
            }
            command = commands[name]
            flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
            log = (LOG_DIR / f"{name}.log").open("ab", buffering=0)
            process = subprocess.Popen(command, cwd=APP_DIR, stdout=log, stderr=subprocess.STDOUT, creationflags=flags)
            self.processes.append((name, process, log))

    def _stop_child(self, name: str) -> None:
        with self.process_lock:
            selected = [entry for entry in self.processes if entry[0] == name]
            self.processes = [entry for entry in self.processes if entry[0] != name]
            self._stop_processes(selected)

    def _restart_child(self, name: str, delay_ms: int = 5000) -> None:
        self._stop_child(name)
        if win32event.WaitForSingleObject(self.stop_event, delay_ms) == win32event.WAIT_TIMEOUT:
            self._start_child(name)

    def _stop_children(self) -> None:
        with self.process_lock:
            selected = self.processes
            self.processes = []
            self._stop_processes(selected)

    def _stop_processes(self, entries: list[tuple[str, subprocess.Popen[bytes], object]]) -> None:
        targets: list[psutil.Process] = []
        for _name, process, _log in entries:
            if process.poll() is not None:
                continue
            try:
                parent = psutil.Process(process.pid)
                targets.extend(parent.children(recursive=True))
                targets.append(parent)
            except (psutil.Error, ProcessLookupError):
                pass
        unique = {process.pid: process for process in targets}
        # Stop descendants before their Python-launcher parents so no orphan can
        # retain COM3, port 8080, or an inherited SQLite/log handle.
        for process in unique.values():
            try:
                process.terminate()
            except psutil.Error:
                pass
        _gone, alive = psutil.wait_procs(list(unique.values()), timeout=10)
        for process in alive:
            try:
                process.kill()
            except psutil.Error:
                pass
        if alive:
            psutil.wait_procs(alive, timeout=5)
        for _name, process, log in entries:
            if process.poll() is None:
                try:
                    process.kill()
                    process.wait(timeout=5)
                except (OSError, subprocess.TimeoutExpired):
                    pass
            log.close()


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(TMMService)
