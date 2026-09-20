# Toshiba Modbus Monitor (TMM)

TMM is a read-only Toshiba Modbus RTU monitoring system for supported Toshiba
inverters. It records value changes in SQLite, provides a local web dashboard,
exports CSV data, supports PCM002Z-compatible parameter backups, and includes a
Windows CSV viewer for offline analysis.

## Version 1.0.0

This first public release contains:

- `TMM-Windows/` — Windows service, dashboard, system-tray controller and
  reproducible Inno Setup installer sources.
- `TMM-Linux/` — Linux systemd deployment, dashboard and interactive first-run
  setup helper.
- `TMM-CSV-Viewer-Windows/` — standalone offline CSV viewer for Windows.

Read the README in the relevant directory before installation. The Windows and
Linux monitor packages are independent deployments; only install the package
for the intended host system.

## Safety

TMM is designed for monitoring. Parameter-write and PCM restore workflows use
standstill checks, but the responsible technician must independently verify
that the drive and connected machinery are in a safe condition before any
configuration change. Do not use TMM as a safety function.

## License

Released under the [MIT License](LICENSE).
