# Toshiba Modbus Monitor (TMM) — Version 1.0

Toshiba Modbus Monitor (TMM) monitors Toshiba variable-frequency drives over a
serial Modbus RTU connection. It runs as a background service on a Debian-based
host, records long-term data in SQLite, and provides a web dashboard.

By default TMM is a read-only monitor. Its optional parameter-management area
can create PCM002Z-compatible backups and write explicitly selected VF-AS1
parameters only after a fresh, verified safe-standstill check. It never offers
start, stop, direction, or frequency commands.

## Version 1.0 features

- Supports Toshiba VF-AS1, VF-S11, VF-S15, and VF-AS3J drives
- Monitors up to three drives on one two-wire RS-485 bus
- Provides configurable rates for fast, normal, diagnostic, and information data
- Retries failed requests and automatically resumes after communication errors
- Shows live values with color-coded warning and critical states
- Records measurements in SQLite with configurable retention
- Reduces storage use by recording status changes and significant analog changes
- Displays measurement history and exports data as CSV
- Decodes known alarms, trips, and diagnostic-memory entries
- Gives input terminals and the FM analog output a prominent hardware view
- Shows model, Modbus address, capacity code, series code, and available CPU or
  EEPROM version information
- Shows host CPU load, memory use, temperature, data-disk use, and communication
  quality
- Estimates daily database growth and remaining storage time
- Reports when estimated storage time is shorter than the requested retention
  period
- Provides English, German, French, and Japanese web interfaces; English is the
  default
- Provides a read-only REST API for external analysis
- Lets each measurement channel be switched Off, Live, or Record to reduce bus
  load and database growth
- Records communication interruption and recovery states in the history chart
- Supports investigation references and safe archive/reinitialize workflows
- Provides engineering conversion for current, voltage, motor/machine speed,
  torque, and mechanical power when the required nameplate values are entered
- Creates PCM002Z-compatible parameter backups and supports a controlled,
  verified partial restore for VF-AS1 drives
- Lets every dashboard category be collapsed; the state is remembered by the
  browser

## Monitored information

The exact values depend on the drive model and its published Toshiba
documentation. Available information includes:

- Output frequency and the effective frequency setpoint
- Operating state, direction, readiness, alarm, and trip state
- Output current, DC-link voltage, and output voltage
- Braking-resistor load (OLr) where the model provides it
- Input terminals such as F, R, S1, S2, and S3
- FM analog output where a documented readback value exists
- Current trip, alarm words, and up to four retained trips
- Operating values captured immediately before the latest trip
- Internal device and power-board temperatures on the VF-AS3J
- Identification and version information provided by the drive
- VF-AS1 diagnostic feedback: speed, torque, load and overload factors, input
  and output power, and calculated motor speed

Not every model exposes every value. TMM displays “not available” instead of
guessing. In particular, the VF-AS1, VF-S11, and VF-S15 do not publish a
documented numeric device-temperature monitor. The documented monitor registers
also do not expose inverter CPU load. CPU load shown in Diagnostics belongs to
the host system.

Current and voltage monitors are percentages as reported by the drive. TMM keeps
the original register word together with every scaled value. If the applicable
rated values are entered under Engineering, TMM additionally shows calculated
amperes, volts, torque, mechanical power, and machine speed. Calculated values
are aids for service work, not calibrated electrical measurements.

## Requirements

- A Debian-based Linux host with Python 3 and `systemd`
- Network access during initial installation for the required Python packages
- A USB-to-RS-485 converter, for example an FTDI/WaveShare 0403:6001 device
- A correctly wired two-wire RS-485 bus with a common reference, suitable
  termination, and a unique Modbus address for every drive

The supplied configuration uses:

- `/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_B001YLYP-if00-port0`
- Modbus RTU, slave address 1, 19200 bit/s, 8 data bits, even parity, 1 stop bit
- 5 Hz for fast values, 2 Hz for normal values, and 0.2 Hz for diagnostics

All devices on the bus must use the same baud rate and data format. The default
19200 bit/s setting corresponds to the VF-AS1 factory setting F800 = 1. If a site
uses another setting, follow the exact communication-parameter activation or
power-cycle procedure in the manual for that drive model.

## Installation

Copy the package to the host, open a terminal in the package directory, and run:

```sh
sudo ./install.sh
```

For an assisted first configuration, run the following after installation:

```sh
sudo /opt/tmm/setup.sh
```

The assistant detects connected USB serial converters where possible, offers
their stable `/dev/serial/by-id/...` paths, and asks for the serial format,
inverter model and address, polling rates, database location, retention, web
port, investigation reference, and optional contact details. It creates a
timestamped backup of the existing configuration before writing the validated
settings and can restart both TMM services afterwards.

The installer creates the program, configuration, and data directories and then
starts two background services. Running it again updates the application without
overwriting the existing configuration or database.

TMM uses these technical names:

- Program: `/opt/tmm`
- Configuration: `/etc/tmm/config.json`
- Default database: `/var/lib/tmm/measurements.sqlite3`
- Version file: `/opt/tmm/VERSION`
- Collector service: `tmm.service`
- Web service: `tmm-web.service`
- Unprivileged system account: `tmm`

Check the services and live log with:

```sh
systemctl status tmm
systemctl status tmm-web
journalctl -u tmm -f
```

Open the dashboard from another computer on the local network:

```text
http://<HOST-IP-ADDRESS>:8080/
```

The installed user manual can be opened from the dashboard or directly at
`/README.md`. Interactive API documentation is available at `/docs`.

## Using the dashboard

Select the language in the upper-right corner. The browser stores the selection
locally. The dashboard contains:

- **Device information:** model, address, and available version codes
- **Messages:** information, warnings, critical conditions, alarms, and trips
- **Terminals & analog output:** digital inputs and FM output
- **Diagnostic memory:** current and retained faults and captured trip values
- **Current measurements:** latest values from every connected drive
- **Measurement history:** chart for the selected value
- **Communication:** success rate, retries, bus load, and host health
- **Storage & export:** data size, retention, remaining time, and CSV download
- **Measurement channels:** per-channel Off, Live, and Record modes
- **Engineering:** optional nameplate values and machine-speed factor
- **Recording:** investigation reference, archive, and reinitialize controls
- **Parameters:** PCM002Z-compatible backup, import preview, partial restore,
  and an auditable parameter-change list

Yellow indicates a warning, red indicates a critical condition, and blue is
informational. These colors are monitoring aids. They do not replace drive
protection functions or assessment by qualified personnel.

## Configuration

`/etc/tmm/config.json` is a JSON text file. Back it up before editing it. Restart
both services after a change:

```sh
sudo systemctl restart tmm
sudo systemctl restart tmm-web
```

Register addresses are Toshiba communication numbers written as strings such as
`"0xFD00"`. TMM does not apply a Modbus minus-one address offset.

### Optional product contact

The dashboard footer can show a site-specific support or operator contact. Add
the optional `product` object at the top level of the configuration:

```json
"product": {
  "contact_name": "Operations support",
  "contact_url": "mailto:support@example.com"
}
```

`contact_url` accepts `https://`, `http://`, `mailto:`, or a plain email address.
Leave `contact_name` empty, or omit the entire `product` object, to hide the
contact row. Existing configurations without this object remain valid.

### Multiple drives

Built-in profiles are named `VF-AS1`, `VF-S11`, `VF-S15`, and `VF-AS3J`. Device
names and Modbus slave addresses must be unique:

```json
"inverters": [
  {"name": "AS1-4037", "model": "VF-AS1", "slave_id": 1, "enabled": true},
  {"name": "S15-Pump", "model": "VF-S15", "slave_id": 2, "enabled": true}
]
```

Profiles select the documented monitor registers automatically. Custom register
lists are supported, but should only be added after checking the communication
manual for the exact drive model.

### Measurement channels and engineering values

The dashboard can change channels without editing JSON. `Off` stops polling the
channel, `Live` polls it but retains only its current value, and `Record` also
writes relevant changes to history. `operating_status` remains enabled because
it is required for safe monitoring and parameter-write interlocks.

### Live-card order

The **Current measurements** cards can be arranged by drag and drop. The order
is saved atomically in `web.live_card_order` in `config.json`, remains after a
service restart, and has no effect on Modbus polling or recording.

The optional `engineering` object belongs to one inverter. Leave values absent
until they have been verified from the motor/drive documentation:

```json
"engineering": {
  "machine_speed_factor": 1.0,
  "machine_speed_unit": "rpm",
  "rated_output_current_a": 98.0,
  "rated_output_voltage_v": 400.0,
  "motor_rated_power_kw": 55.0,
  "motor_rated_speed_rpm": 1780
}
```

Machine speed is calculated from motor speed times `machine_speed_factor`.
Current and voltage are converted from the drive's percentage values only when
the matching rated value is supplied. Power, torque, and speed calculations are
clearly labelled as calculated values.

### Sampling rates

```json
"polling": {
  "interval_seconds": 1.0,
  "intervals": {
    "fast": 0.2,
    "normal": 0.5,
    "diagnostic": 5.0,
    "information": 3600.0
  },
  "retries": 2,
  "retry_delay_seconds": 0.15,
  "reconnect_delay_seconds": 2.0
}
```

An interval of `0.2` seconds means five polls per second. VF-AS1 and VF-S11 limit
Modbus function 03 to one 16-bit word per request, which TMM handles
automatically. VF-S15 and VF-AS3J can read suitable nearby registers in blocks.

At the default 19200 bit/s, begin around 2 Hz when monitoring three VF-AS1-class
drives. The supplied 5 Hz fast interval is suitable for the default single-drive
configuration, subject to observed response time and bus quality. For higher
multi-drive rates, 38400 bit/s can reduce wire time, but every bus participant
must be changed and the result must be verified using the communication
diagnostics. Do not assume that a requested rate is achieved: check retries,
timeouts, poll duration, and estimated bus load.

### Change-only history

The live snapshot is updated after every poll. Historical digital states and raw
status words, however, are stored only when they change. An analog value is stored
when its cumulative difference from the last recorded value reaches its threshold:

```json
"change_logging": {
  "enabled": true,
  "initial_snapshot_on_start": true,
  "communication_unreachable_after_transport_errors": 3,
  "default_analog_delta": 0.1,
  "successful_cycle_interval_seconds": 60.0,
  "thresholds": {
    "output_frequency": 0.05,
    "frequency_setpoint": 0.05,
    "output_current": 0.1,
    "dc_input_voltage": 0.1,
    "output_voltage": 0.1,
    "braking_resistor_load": 1.0,
    "fm_analog_output": 0.5,
    "inverter_internal_temperature": 1.0,
    "power_board_temperature": 1.0
  }
}
```

This block belongs inside the `storage` section. Thresholds use displayed units
such as Hz, percent, or °C. Unchanged successful cycles are retained once per
minute by default, while errors and value changes are retained immediately.
Compact diagnostic aggregates preserve communication statistics. Set `enabled`
to `false` to store every successful reading in history.

### Retention and CSV export

```json
"storage": {
  "database": "/var/lib/tmm/measurements.sqlite3",
  "retention_days": 365,
  "cleanup_interval_seconds": 3600,
  "export_max_rows": 250000
}
```

TMM periodically removes records older than `retention_days`. A value of `0`, or
omitting the setting, means unlimited retention. CSV export is limited to
`export_max_rows` rows so a very large download does not overload the host.

The storage projection needs at least five minutes of data. It uses the actual
database size, free disk space, and observed growth. If retention is expected to
limit growth before the disk fills, the dashboard says so. The result is an
estimate, not a guaranteed deadline.

### Warning and critical limits

```json
"alerts": {
  "system": {
    "cpu_percent": {"warning": 80, "critical": 95},
    "temperature_celsius": {"warning": 70, "critical": 80},
    "memory_percent": {"warning": 85, "critical": 95},
    "disk_percent": {"warning": 85, "critical": 95}
  },
  "metrics": {
    "output_current": {"warning": 90, "critical": 110},
    "dc_input_voltage": {"warning": 110, "critical": 120},
    "braking_resistor_load": {"warning": 70, "critical": 90},
    "inverter_internal_temperature": {"warning": 70, "critical": 85},
    "power_board_temperature": {"warning": 80, "critical": 95}
  }
}
```

These are useful starting values, not universal engineering limits. Verify them
for the motor, drive, braking resistor, enclosure, ambient conditions, and site
requirements. Set an entry to `null` to disable its default threshold.

### Investigation reference and recording lifecycle

Set `recording.reference` to an identifier such as a commission number, site,
or investigation title. The dashboard includes it with the active recording and
archive name. Use **Archive and start new recording** for normal turnover: the
services close the active database safely, move it to an `archive` directory
next to the configured database, and start a new empty SQLite recording.

Permanent deletion is deliberately guarded by typing `DELETE` three times. It
exists only for invalid test recordings. Use archive in normal operation.

### PCM002Z parameter backup and controlled restore

The Parameters page accepts an original PCM002Z `.pcm` file for the selected
model as a register template. TMM reads a new device-specific backup and keeps
template values where the drive documents a register as unreadable. Backups are
stored next to the database in `parameter-backups/` and can be downloaded or
removed from the dashboard.

A `.pcm` or PCM002Z `.csv` can be imported for a preview. TMM classifies entries
as candidate, monitor, communication, special, or unsupported. Only explicitly
selected candidate registers can be written, and the current implementation
allows writes only for VF-AS1. Before every batch it requires three fresh polls
confirming a safe standstill with no trip, alarm, emergency stop, or running bit.
Each value is read back and every successful change is written to the audit log.

Parameter writing is safety-critical. Use it only with authorization, a verified
machine-safe condition, a fresh backup, and a review of the exact drive manual.
Remote administration is disabled by default. To intentionally administer from
a trusted remote workstation, set `web.allow_remote_administration` to `true`.

## Using an external data disk

For long-term recording, prefer an SSD or NVMe device over a USB flash drive.
After permanently mounting the disk at `/mnt/tmm-data`, run:

```sh
sudo install -d -o tmm -g tmm -m 0750 /mnt/tmm-data
sudo systemctl edit tmm.service
sudo systemctl edit tmm-web.service
```

Add this drop-in to both services:

```ini
[Unit]
RequiresMountsFor=/mnt/tmm-data
```

Set `storage.database` to `/mnt/tmm-data/measurements.sqlite3`. Stop both services
before moving an existing database, and move any `-wal` and `-shm` sidecar files
together with the main database.

## Interfaces and security

TMM uses Modbus function 03 for monitoring and, only for the controlled VF-AS1
parameter workflow described above, function 06 to write one verified holding
register at a time. Services run under the unprivileged `tmm` system account.

Important HTTP endpoints:

- `GET /api/v1/health` — status and freshness
- `GET /api/v1/metadata` — devices and available metrics
- `GET /api/v1/metrics/latest` — current values
- `GET /api/v1/metrics/history` — measurement history
- `GET /api/v1/poll-cycles` — recent communication cycles
- `GET /api/v1/diagnostics` — communication and host health
- `GET /api/v1/storage` — database and storage information
- `GET /api/v1/export.csv` — CSV export with optional metric and time range
- `POST /api/v1/channels` and `POST /api/v1/engineering` — dashboard settings
- `POST /api/v1/recording/reinitialize` — archive or guarded deletion
- `GET/POST /api/v1/parameter-backups` — parameter backup management
- `POST /api/v1/parameter-import-preview` and `POST /api/v1/parameter-write`
  — controlled parameter workflow
- `GET /README.md` — this installed manual

The dashboard has no user authentication. Operate it only on a trusted local
network, or place it behind a properly secured reverse proxy.

## Maintenance and troubleshooting

Stop or restart the services:

```sh
sudo systemctl stop tmm tmm-web
sudo systemctl restart tmm tmm-web
```

Run one foreground collection cycle:

```sh
sudo systemctl stop tmm
sudo -u tmm /opt/tmm/.venv/bin/python \
  /opt/tmm/tmm_monitor.py \
  --config /etc/tmm/config.json --once
sudo systemctl start tmm
```

Common communication problems include reversed A/B wires, a missing common
reference, incorrect parity or baud rate, duplicate slave addresses, unsuitable
termination, and a response timeout that is too short. Modbus exception `0x03`
often means that the specific model rejects a register or block length. TMM uses
model-specific profiles and single-register reads for VF-AS1 and VF-S11 to avoid
unsupported blocks.

Inspect recent stored data directly with:

```sh
sudo sqlite3 /var/lib/tmm/measurements.sqlite3 \
  "SELECT observed_at, inverter, metric, value, unit FROM samples ORDER BY id DESC LIMIT 20;"
```

SQLite uses WAL mode and commits one complete poll cycle as a transaction. For a
backup, briefly stop both services or use a SQLite-compatible online backup
method.

## Tests and technical basis

The automated protocol, profile, database, and API tests do not require a
connected drive:

```sh
python3 -m unittest discover -s tests -v
```

Register definitions are based on the applicable Toshiba communication manuals
for the supported product families, including E6581315 for the TOSVERT VF-AS1
series. Before using another variant, verify its exact model designation against
the corresponding Toshiba documentation.

---

**Product:** Toshiba Modbus Monitor (TMM)  
**Version:** 1.0.0  
**Operating mode:** long-term monitoring with optional guarded parameter service
