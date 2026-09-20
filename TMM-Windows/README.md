# Toshiba Modbus Monitor for Windows — V1.0.0

This is the Windows edition of Toshiba Modbus Monitor (TMM) V1.0.0. It keeps
the read-only Modbus, drive-profile, SQLite, alarm, history, CSV, and multilingual
web features of the Linux edition while replacing operating-system integration
with Windows-native components.

## Supported host systems

- 64-bit Windows 10 or 11, or Windows Server 2019 or newer
- An RS-485 adapter exposed as a Windows COM port
- An administrator account for installation

The standard installation is self-contained: it includes a private Python
runtime and does not require Python to be installed separately on the host
system. The setup executable is not code-signed in V1.0.0, so Windows may show
a publisher warning before installation.

## Architecture

One automatic Windows Service named `TMM` supervises two child processes:

- the Modbus collector, which owns the COM port and writes SQLite;
- the read-only web server, which reads SQLite and serves the dashboard.

Program files are installed in `%ProgramFiles%\TMM`. Configuration, measurements,
and logs are stored in `%ProgramData%\TMM`, so they remain separate from the
application and survive an ordinary software update.

The service normally runs as `LocalSystem`. It starts without an interactive user
session. The dashboard listens on TCP port 8080. The installer adds a Private
network firewall rule unless `-NoFirewallRule` is specified.

## Installation

1. Run `TMM-Setup-1.0.0.exe` as an administrator.
2. Select the COM port, baud rate, inverter family, Modbus address, and desired
   database location in the setup assistant.
3. Finish setup and open `http://localhost:8080/` on the host system.

The setup creates the automatic Windows service named `TMM`, optionally adds a
Private-network firewall rule, and starts the notification-area controller for
the installing user. Program files are installed below `%ProgramFiles%\TMM`;
configuration, logs, backups, and measurements remain below `%ProgramData%\TMM`.

An upgrade preserves the existing `config.json` and SQLite recording. To change
connection or storage settings later, use the tray controller's **Configuration**
entry or the dashboard's local administration pages.

### Source-tree installation for development

For development testing only, an elevated PowerShell window can run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install.ps1
```

Edit `%ProgramData%\TMM\config.json` and restart the service when necessary:

```powershell
Restart-Service TMM
```

The source installer is safe to run again after an interrupted installation. It retains
`config.json`, refreshes the program files and Python dependencies, repairs the
service registration, and starts the service again.

Open `http://localhost:8080/` on the host. From another computer, use the host's
IP address. The firewall rule intentionally applies only to the Private network
profile.

## Default communication

The example uses Modbus RTU at 19200 bit/s, 8 data bits, even parity, and 1 stop
bit. The default slave address is 1. Every device on the two-wire bus must use the
same serial format and a unique slave address.

## Extended VF-AS1 monitoring

The VF-AS1 profile also reads the drive's native speed-feedback, torque,
torque-current, exciting-current, motor/inverter load, overload-factor, and
input/output-power monitors. `FE90` is exposed as `calculated_motor_speed` in
rpm because Toshiba derives it from output frequency and the configured motor
pole parameter; it must not be mistaken for encoder-measured shaft speed.

These extended values use the `diagnostic` sampling class (five seconds in the
example configuration). This keeps their additional Modbus transactions from
reducing the fast sampling rate used for frequency, current, operating status,
and terminal signals. Installations that require another rate can override the
individual profile registers in an inverter entry.

## Measurement channels

The dashboard can configure every profile channel separately for each inverter:

- **Off** removes the register from Modbus polling and reduces bus load;
- **Live** polls the register and shows its latest value without adding it to
  measurement history or CSV exports;
- **Record** polls it and stores changes using the configured incremental
  thresholds.

Changes are written atomically to `config.json` and applied by the running
collector without restarting the service. Operating status remains protected
and recorded because it is required for trustworthy state and future safe-write
checks. A configured inverter may also express these choices directly:

```json
"channels": {
  "input_power": "off",
  "output_power": "live",
  "input_terminal_status": "record"
}
```

The history selector includes the input-terminal status. TMM renders F, R, S1,
S2, and S3 as separate digital tracks, so simultaneous rectangular signals do
not obscure one another.

### Live-card order

The **Current measurements** cards can be arranged by drag and drop. The order
is saved atomically in `web.live_card_order` in `config.json`, remains after a
service restart, and has no effect on Modbus polling or recording.

## PCM002Z parameter backup

The local dashboard can create a read-only native `.pcm` parameter backup. Select
an original PCM002Z `.pcm` file for the configured inverter model. TMM validates
its header, uses its communication-number list as the model-specific template,
reads every listed register through the collector, and writes a fresh ASCII file
with Windows CRLF line endings. Completed files are kept in
`%ProgramData%\TMM\parameter-backups` and are downloadable from the dashboard.
Each displayed backup can also be deleted locally after an explicit confirmation.
When deleting a partial `.pcm` backup, TMM deletes its paired diagnostic `.txt`
report as the same backup artifact.
The backup list is filtered by its inverter selector and marks the newest
device-specific `.pcm` file as the current reference used for import and write
validation.

Normal monitoring pauses during this operation because only the collector may
own the serial port. PCM002Z can access some VF-AS1 communication numbers through
Toshiba's native protocol that the drive rejects in Modbus mode with exception
`0x02`. TMM updates every readable value and, for inaccessible addresses, retains
the value from the selected template. Such output is named `-partial.pcm` and is
accompanied by a text report listing every retained address. It must not be
mistaken for a fully refreshed backup. This function never writes to the
inverter. PCM files also include volatile monitor registers, so a backup must not
yet be treated as an automatically safe restore set.

### Import preview

The PCM import preview compares a selected target file with the newest parameter
backup and never writes to the inverter. It lists only changed raw values and
assigns each to a server-controlled safety class: configuration candidate,
communication setting, special PCM parameter, monitor/internal register, or a
VF-AS1 register known to be unreadable through Modbus. Only ordinary
configuration candidates are marked selectable for a future write stage; every
other class remains blocked. Creating a current backup before comparison is
mandatory, preventing an old database or PCM file from being mistaken for the
connected drive's present state.

TMM validates the PCM002Z header against the configured inverter family at all
three stages: reading a backup, creating an import preview, and writing a
selected partial restore. A filename alone is never considered model evidence.
For multi-inverter installations, the newest backup is selected only from files
created for the same configured inverter name.

Before any parameter write, that device-specific backup must be current. The
default maximum age is 60 minutes and is shown in the import preview. Adjust
`storage.parameter_write_max_backup_age_minutes` for a different commissioning
window; set it to `0` only when intentionally disabling this freshness check.

### Controlled partial restore

For a VF-AS1, the local dashboard can write between one and 32 selected
configuration candidates from an import preview. A matching PCM002Z `.csv`
file is required as an independent source for each parameter's permitted raw
range. Communication settings, special parameters, monitor/internal registers,
and known Modbus-unreadable addresses remain blocked by the server regardless
of what the browser displays.

The operator must enter `WRITE` followed by every selected four-digit address
in ascending order, for example `WRITE 0014 0015`. The collector is the only
component that accesses the serial port. Immediately before each individual
write it confirms standstill three times (zero output frequency, no run status,
no F/R input command, and no active trip, alarm, or emergency-stop status),
performs Modbus function 06, reads the register
back, and writes a verified audit entry to SQLite. A batch stops at its first
failure. TMM never rolls back already verified earlier writes automatically;
the result explicitly reports such a partial completion and the audit log
preserves every applied change.

The dashboard also provides a write-precondition check. It performs the same
three fresh standstill polls through the collector and reports whether a write
would currently be blocked. This is advisory only: TMM repeats the complete
check immediately before every actual parameter write.

The import view displays the selected count and the exact confirmation text to
enter. The write button stays disabled until at least one, and at most 32,
configuration candidates are selected.

TMM binds a write request to the exact target PCM file used for its import
preview. If that file, or the selected inverter, changes after previewing, the
write is blocked until a fresh comparison is made.

The dashboard also shows the latest verified parameter changes from the current
recording (time, inverter, communication number, old value, requested value,
and read-back value). This audit is read-only and is retained with the SQLite
recording when it is archived. Its complete current-recording audit can also be
downloaded as a separate CSV file; that export includes the investigation
reference of its SQLite recording, the source backup filename, and the SHA-256
fingerprint of the target PCM file.

Only one parameter-write request can be pending at a time. A second browser
click or another local client receives a conflict response instead of replacing
the first request.

An optional per-drive engineering factor records machine speed directly in
SQLite and CSV. TMM uses the native `calculated_motor_speed` value as its source:

```json
"engineering": {
  "machine_speed_factor": 0.1,
  "machine_speed_unit": "rpm",
  "rated_output_current_a": 10.0,
  "rated_output_voltage_v": 400.0
}
```

The resulting value is `machine_speed = calculated_motor_speed × factor`. A
factor of `0.1`, for example, converts 1500 rpm at the motor to 150 rpm at the
machine. Omit `machine_speed_factor` to disable the derived channel. The unit is
a label and does not perform another conversion.

The optional rated values also turn the inverter's percentage monitors into
engineering values:

- `actual_output_current = output_current [%] × rated_output_current_a / 100`
- `actual_output_voltage = output_voltage [%] × rated_output_voltage_v / 100`

These are calculated values, not additional Modbus registers. Use the applicable
reference values from the inverter/motor setup. Omitting a reference value
disables only its derived channel.

These four engineering settings can be edited in the dashboard on the local
Host-System. TMM validates them, atomically updates `config.json`, and passes the
new values to the running collector without restarting the Windows service.
Previously calculated live values are invalidated so the next successful source
read immediately establishes a correctly scaled baseline. Remote configuration
requires the explicit `web.allow_remote_administration` opt-in.

Optional motor nameplate power and speed add two estimated mechanical channels:

- `rated torque [Nm] = 9550 × rated power [kW] / rated speed [rpm]`
- `actual_motor_torque [Nm] = torque monitor [%] × rated torque / 100`
- `mechanical_power [kW] = actual torque [Nm] × calculated motor speed [rpm] / 9550`

Both nameplate values must be entered together. These results depend on the
drive's torque estimate and are engineering aids rather than calibrated shaft
measurements.

## Service and logs

### Investigation reference and new recordings

The Recording section assigns a durable text reference to each database, for
example a commission number, machine, and test purpose. CSV exports carry the
same value in `investigation_reference`, so an exported dataset remains
self-identifying outside TMM.

Starting a new recording safely checkpoints and closes SQLite, moves the old
database to `ProgramData\TMM\archive`, and creates a clean database with the new
reference. Permanent deletion is deliberately hidden in the danger zone and
requires the word `DELETE` three times. Recording administration is restricted to
the local Host-System unless `web.allow_remote_administration` is explicitly set
to `true`.

### Safe source upgrade

Run `install.ps1` from an elevated PowerShell window. The script first stages
and hashes the complete application while the existing service is still
available. It then stops TMM, copies every staged file explicitly, verifies the
installed hashes, validates the retained JSON configuration, and starts TMM.
Finally it checks both the health API and `/static/app.js`. A partial copy can
therefore no longer be reported as a successful upgrade; on verification
failure the service remains stopped for safe diagnosis.

The compiled installer performs the same application-manifest verification
before registering or starting the updated service. Configuration and database
files under `ProgramData` remain outside the application replacement.

Useful PowerShell commands:

```powershell
Get-Service TMM
Start-Service TMM
Stop-Service TMM
Restart-Service TMM
Get-Content "$env:ProgramData\TMM\logs\collector.log" -Wait
Get-Content "$env:ProgramData\TMM\logs\web.log" -Wait
```

Service lifecycle messages are also written to Windows Event Viewer. If either
child process exits unexpectedly, the service fails and Windows Service Control
Manager restarts it according to the configured recovery action.

## Notification-area controller

The installer starts a TMM notification-area controller and adds it to the
common Windows Startup folder, so it starts within each interactive user's
session. It is independent of the LocalSystem service: the icon remains
available when monitoring is stopped. A left click opens
`http://localhost:8080/`. The context menu displays service state and provides
Open dashboard, Start, Stop, Start with Windows, Configuration, and Exit tray.

The icon is green when the service and device health are good, yellow while the
service is starting or reports degraded/stale health, grey when the service is
stopped, and red when the service is missing. Administrative operations request
Windows UAC approval. The configuration dialog provides common connection,
sampling, storage, and web settings plus an advanced JSON editor. Saving creates
`config.json.bak`, replaces the configuration, and restarts TMM.

The dashboard footer uses the detailed TMM product mark and reads its version
from the API. Optional contact information can be added through Advanced JSON:

```json
"product": {
  "contact_name": "Operations support",
  "contact_url": "mailto:support@example.com"
}
```

`contact_url` accepts `https://`, `http://`, `mailto:`, or a plain email address.
Leave both values empty to hide the contact row.

## COM-port behavior

At automatic Windows startup, especially in a virtual machine with USB
pass-through, the service can be ready before Windows exposes the USB converter
as its configured COM port. TMM therefore waits up to 90 seconds for the port
before its first poll. It starts monitoring automatically as soon as the port
appears. Adjust `polling.windows_serial_startup_wait_seconds` (or set it to `0`
to disable the wait) when a host requires a different boot delay.

A Windows COM port is exclusive. Close vendor tools, terminal programs, and
other Modbus applications before starting TMM. A valid Modbus exception returned
by a drive does not cause TMM to close and reopen the COM port; the remaining
register groups continue on the existing connection. Actual serial transport
errors still trigger a controlled reconnect.

The Windows Service listens for suspend as well as automatic and user-initiated
resume events. Before Windows enters standby, it stops the collector process
tree and thereby releases the COM handle while the FTDI driver is still active.
After resume it waits five seconds for USB hardware stabilization and starts the
children again. As a fallback, ten consecutive `Access is denied` failures
cause the collector to exit so Windows Service Recovery can restart TMM cleanly.
The fallback count is configurable as `polling.windows_access_denied_restart_after`.
The supervisor normally restarts only the failed child process, so a collector
recovery does not take down the dashboard. Windows Service Recovery remains a
final fallback for an unexpected supervisor failure.

If the FTDI virtual COM driver remains locked, the collector exits with the
dedicated recovery code 75. The supervisor waits 30 seconds before trying the
collector again, avoiding a rapid restart loop. TMM intentionally does not
disable the device through Plug and Play: some FTDI/Windows combinations can
complete that operation only during a system reboot. Configuration failures use
a different exit code.

## External data drive

Stop the service, create a permanent directory on the external volume, grant the
service account write access, and set `storage.database` to an absolute Windows
path such as `D:\TMM-Data\measurements.sqlite3`. Use a drive that receives the same
drive letter before the service starts. A volume mount point is safer than a
removable drive letter for unattended operation.

## Change-based recording and initial snapshots

With `storage.change_logging.enabled` set to `true`, raw or digital values are
stored only when they change. Analog values are stored after their configured
increment threshold is reached. This substantially reduces long-term database
growth.

At every collector-process start, TMM records the first successful value of
every available register once. This initial snapshot establishes a known state
for a new recording session, even when all values are unchanged from the
previous process. It is enabled by default:

```json
"initial_snapshot_on_start": true
```

Set the option to `false` only when suppressing identical values across service
restarts is more important than having a complete session baseline.

TMM also records `communication_status` only when its state changes: `2` means
online, `1` means degraded, and `0` means unreachable. A valid Modbus exception
proves that the drive answered and is not counted as a transport error;
unsupported registers therefore do not create availability events. Other read
failures accumulate across register groups. This is important for long polls:
one late successful read during power-up must not hide the preceding outage.
The unreachable state is recorded after three transport errors by default.
Configure the threshold inside `storage.change_logging`:

```json
"communication_unreachable_after_transport_errors": 3
```

An unreachable state cannot distinguish drive power-off from a disconnected
RS-485 cable or another transport interruption; it deliberately reports the
observable communication condition.

## Removal

Run from an elevated PowerShell window:

```powershell
.\uninstall.ps1
```

Configuration and measurements are retained by default. Use
`.\uninstall.ps1 -RemoveData` only when permanent deletion is intended.

## Verification and scope

The release is verified by automated protocol, decoder, configuration, SQLite,
parameter-safety, and web-data tests, plus installation checks that compile and
hash every shipped application file. The Windows service, standby/resume
recovery, automatic startup, COM-port reconnect handling, CSV exports,
database growth, upgrade installation, and removal have also been exercised on
a Windows host with an FTDI RS-485 adapter and a Toshiba VF-AS1 drive.

As with every industrial monitoring tool, confirm the configured COM port,
Modbus address, serial format, scaling values, and parameter-write safety
conditions on the specific installation before operational use.
