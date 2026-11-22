# Toshiba Modbus Monitor (TMM)

TMM is a read-only Toshiba Modbus RTU monitoring system for supported Toshiba
inverters. It records value changes in SQLite, provides a local web dashboard,
exports CSV data, supports PCM002Z-compatible parameter backups, and includes a
Windows CSV viewer for offline analysis.

## Current release candidates

### TMM Linux Master 1.3.0 RC3

The Linux Master has reached its 1.3 feature freeze. RC3 is the prerelease for
the final 24-hour machine test; later changes to the 1.3 line are published only
as **Bugfixes**. Highlights include the deterministic transparent proxy,
external I/O and GPIO sources, recording administration, condition-monitoring
logic, improved diagnostics and a field-service-oriented dashboard.

The public package does not redistribute Sequent Microsystems manuals or
schematics. It links to the official publisher files and provides an optional
checksum-pinned downloader for local/offline installations.

See `TMM-Linux/RELEASE_POLICY.md`, `TMM-Linux/ROADMAP.md` and the Linux README.
Version 1.4 targets tested Toshiba parameter-set import/export as its primary
objective and Condition Monitoring Milestones as a mandatory product goal.

The Windows monitor and Windows CSV Viewer remain at their separately published
version until their dedicated porting and 24-hour-test alignment is complete.

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
