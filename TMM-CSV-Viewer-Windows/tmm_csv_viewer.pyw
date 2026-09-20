"""Local launcher for the offline TMM CSV Viewer."""

from __future__ import annotations

import argparse
import contextlib
import http.server
import json
import os
import socket
import threading
import webbrowser
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
LANGUAGES = {"en", "de", "fr", "ja"}
SETTINGS_PATH = Path(os.environ.get("APPDATA", str(Path.home()))) / "TMM CSV Viewer" / "settings.json"
SETTINGS_LOCK = threading.Lock()


def saved_settings() -> dict[str, str]:
    """Read user preferences shared by all temporary viewer ports."""
    with SETTINGS_LOCK:
        try:
            data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
            language = str(data.get("language", "en"))
            return {"language": language if language in LANGUAGES else "en"}
        except (OSError, json.JSONDecodeError, TypeError):
            return {"language": "en"}


def save_settings(settings: dict[str, str]) -> dict[str, str]:
    language = str(settings.get("language", "en"))
    if language not in LANGUAGES:
        raise ValueError("unsupported language")
    with SETTINGS_LOCK:
        SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
        temporary = SETTINGS_PATH.with_suffix(".tmp")
        temporary.write_text(json.dumps({"language": language}) + "\n", encoding="utf-8")
        os.replace(temporary, SETTINGS_PATH)
    return {"language": language}


class ViewerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_json(self, status: int, payload: dict[str, str]) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802 - required handler name
        if self.path.split("?", 1)[0] == "/api/settings":
            self._send_json(200, saved_settings())
            return
        if self.path.split("?", 1)[0] == "/README.md":
            try:
                data = (APP_DIR / "README.md").read_bytes()
            except OSError:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/markdown; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802 - required handler name
        if self.path.split("?", 1)[0] != "/api/settings":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 1 <= length <= 1024:
                raise ValueError("invalid request size")
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            self._send_json(200, save_settings(payload))
        except (UnicodeDecodeError, ValueError, json.JSONDecodeError):
            self._send_json(400, {"error": "invalid settings"})


class ViewerServer(http.server.ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def available_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def run(port: int = 0, open_browser: bool = True) -> None:
    if not STATIC_DIR.is_dir():
        raise RuntimeError(f"Viewer assets not found: {STATIC_DIR}")
    selected_port = port or available_port()
    server = ViewerServer(("127.0.0.1", selected_port), ViewerHandler)
    url = f"http://127.0.0.1:{selected_port}/"
    if open_browser:
        threading.Timer(0.35, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        with contextlib.suppress(Exception):
            server.server_close()


def main() -> None:
    parser = argparse.ArgumentParser(description="TMM CSV Viewer")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    run(args.port, not args.no_browser)


if __name__ == "__main__":
    main()
