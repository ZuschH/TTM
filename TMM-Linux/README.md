# Toshiba Modbus Monitor (TMM) - Linux Master Version 1.3

Release baseline: development revision r133

Toshiba Modbus Monitor (TMM) monitors Toshiba variable-frequency drives over a
serial Modbus RTU connection. It runs as a background service on a Debian-based
host, records long-term data in SQLite, and provides a web dashboard.

TMM can use multiple independent USB-to-RS485 adapters. Each physical bus has a
stable ID and a `/dev/serial/by-id/...` device path; every inverter is assigned
to exactly one bus. Slave addresses must be unique only within that bus.

Passive Raspberry Pi screw-terminal HATs can be configured as digital input
sources. TMM uses BCM numbering, selectable internal pull resistors and
optional active-low interpretation. GPIO inputs are strictly 3.3 V logic and
must never be connected directly to 5 V, 24 V or unisolated industrial signals.

By default TMM is a read-only monitor. Its optional parameter-management area
can create PCM002Z-compatible backups and write explicitly selected VF-AS1
parameters only after a fresh, verified safe-standstill check. It never offers
start, stop, direction, or frequency commands.

## Version 1.3 capabilities

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
- Organizes live cards in sortable source groups with up to four columns
- Supports Raspberry Pi GPIO inputs plus Sequent digital, analog, Multi-IO, Smart Fan, and Super Watchdog &
  UPS cards with independent per-channel Off, Live, Record, and Live-hide modes
- Provides multi-axis history charts, selectable step/linear/spline curves,
  pan, zoom, fullscreen, temporary analysis markers, and CSV export
- Protects the Pi thermally by throttling collection at 75 °C and pausing it if
  a throttled system overheats again
- Includes guided setup, safe uninstall, and a verified offline installation
  bundle for air-gapped field deployments

## Communication bridge in version 1.3

Version 1.3 provides an inline Modbus communication bridge using two independent
USB-to-RS485 adapters:

```text
HMI / master <-> TMM upstream port <-> TMM downstream port <-> inverter / slave
```

The implemented production path is a deterministic transparent proxy with
passive monitoring and strict HMI priority:

1. TMM receives one complete RTU request from the HMI-side adapter.
2. It forwards the exact bytes to the inverter-side adapter without correction,
   retries, command creation, or write de-duplication.
3. It receives and immediately returns the exact inverter response to the HMI.
4. After forwarding, it places the transaction into a bounded, non-blocking
   memory queue. A background worker records raw frames, CRC state, function,
   address, latency, and outcome in SQLite.
5. The same worker passively adopts configured TMM measurements contained in
   valid HMI read responses. This creates no additional bus traffic and uses
   the normal change-aware SQLite storage path.
6. If storage cannot keep up, TMM drops and counts diagnostic queue entries;
   it never delays serial forwarding to preserve a log entry.

Partial requests and CRC-invalid requests are never forwarded. Passive decoding
is enabled by default and never writes to a serial port. In the current
HMI-priority revision, scheduled TMM polling is suppressed at runtime even when
an older configuration still requests it. TMM therefore monitors only values
already read by the HMI and cannot occupy the inverter link with an independent
request. A future guarded polling mode may be reintroduced only after collision
detection and an automatic circuit breaker have been validated under machine
load.
HMI and TMM transactions are identified separately in diagnostics and the raw
RTU evidence logbook. The diagnostics also show how many HMI reads and matching
measurements were adopted during the last 60 seconds. Measurements not read by
the HMI are not available from the inverter in this production-safe mode.
SQLite work, passive decoding, and retention deletion run outside the serial
forwarding thread. Queue statistics and dropped diagnostic records are exposed
in the bridge runtime diagnostics.

Configured Sequent I²C cards continue to run in independent worker threads while
transparent proxy mode is active. Their polling cadence, channel selection,
change thresholds, and SQLite storage remain independent of HMI traffic and
scheduled inverter reads.

An inline software bridge adds two USB adapters, the host, its power supply, and
the operating system to the communication path. For machinery where loss of HMI
control affects availability or safety, use an external normally-closed hardware
bypass that reconnects HMI and inverter directly when TMM is unavailable.

## Condition monitoring in version 1.3

- Creates SQLite milestones from technician-defined measurement conditions
- Supports comparison, Boolean negation, delay, tolerance, and hysteresis
- Displays persistent milestones directly in the measurement-history chart

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

## Raspberry Pi GPIO and Sequent external I/O add-ons

A passive GPIO screw-terminal HAT is available as `raspberry_pi_gpio`. Setup
offers the conflict-free BCM pins 4, 5, 6, 12, 13, 16–27; GPIO 2/3 (I²C),
7–11 (SPI) and 14/15 (UART) are deliberately omitted from the defaults. Every
input can use an internal pull-down, pull-up or no pull resistor and may be
interpreted as active LOW. GPIO channels start disabled and TMM never drives an
output. Their values participate in Live view, SQLite history, CSV export and
condition monitoring exactly like other digital inputs.

The GPIO header is **not industrial I/O**: it is limited to 3.3 V logic and has
no galvanic isolation or overvoltage protection. Use an appropriate isolated
interface for 5 V/24 V machine signals.

The GPIO card links to a locally installed, browser-readable wiring schematic.
It identifies physical header pins and BCM numbers side by side, marks the pins
offered by TMM and illustrates safe dry-contact and 3.3 V input wiring. The
schema remains available on the grey support-reference card even when GPIO is
not configured on that TMM.

For telephone support, the dashboard also shows supported but unconfigured
field-I/O and system HATs as grey reference cards. These catalog entries never
poll hardware, never raise availability alarms and expose no enable/configure
controls; they simply keep the visual vocabulary consistent across TMM sites.

### Sequent Microsystems cards

Version 1.3 includes optional Linux-only acquisition add-ons for the
Sequent Microsystems cards **Sixteen LV Digital Inputs** (`sequent_16inpind`),
**Eight 24-Bit Analog Inputs DAQ** (`sequent_24b8vin`) and **Multi-IO**
(`sequent_multiio`). They use the
Raspberry Pi I²C bus and do not share the Toshiba RS-485 collector.

Each physical card is declared once with its hardware `stack` address (0–7).
The digital card is read as one 16-bit bitmap at a default 20 ms interval. The
analog card is read at a default 50 ms interval; its readings can be scaled per
channel using `value = volts * scale + offset`. For example,
`scale: 25, unit: "bar"` converts 0–10 V to 0–250 bar.
The optional `gain` field documents the expected board range; TMM never applies
it. Configure gain and calibration with Sequent's own tool before monitoring.

The Multi-IO add-on is deliberately **read-only** in TMM. It can acquire its
four opto-isolated digital inputs, two 0–10 V inputs, two 4–20 mA inputs and
two PT100 temperatures. Frequency, duty-cycle and counter signals can be added
per digital input in `config.json`. TMM never writes Multi-IO relays, analog
outputs, LEDs, the motor driver, servos, RTC, calibration data or watchdog.

Copy the disabled examples from `config.example.json` into the active
`config.json`, set `enabled` to `true`, and install the vendor packages on the
Pi:

```sh
sudo python3 -m pip install SM16inpind SM24b8vin SMmultiio
```

TMM's setup assistant installs the optional Smart Fan driver separately. Its
current wheel still lists the unmaintained `RPi.GPIO` C extension even though
the driver implementation uses `gpiozero` and `smbus2`. TMM therefore installs
those actual dependencies explicitly and installs `SMsfan` without the stale
dependency metadata. This prevents an unnecessary native `RPi.GPIO` build on
modern aarch64 systems, including Python 3.13.

I²C must be enabled first (for Raspberry Pi OS: `sudo raspi-config`). A missing
card or driver is shown in the **External I/O** dashboard category and is
stored at most once per second, so an unplugged card cannot flood the database.
The dedicated Multi-IO current inputs are recorded in mA; they are never
silently interpreted as voltage inputs. The 24-bit Analog Inputs DAQ card
continues to use the explicit voltage-plus-scaling model described above.

### Offline Sequent documentation

The public TMM source and release archives do **not** redistribute Sequent
Microsystems PDFs. By default, the dashboard links directly to the official
publisher files. During an online installation, `fetch-sequent-docs.sh` may
download those files and accepts them only after their pinned SHA-256 checksums
match. The offline-bundle builder performs the same verified download so the
locally built service bundle remains usable without internet access. Copyright
and all other rights in those documents remain with Sequent Microsystems; URLs
and checksums are listed in `static/docs/sequent/README.md`. Before wiring,
select the schematic revision that matches the physical card.

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

The setup assistant uses the `dialog` package and offers a persistent main menu.
If necessary, it offers to install `dialog` before continuing. Its dedicated
**Configure transparent HMI proxy** workflow requires two detected adapters and
assigns one stable `/dev/serial/by-id/...` path to the HMI side and another to
the inverter side. It configures their shared Modbus format and response timeout,
then explicitly enables or disables proxy mode. The same workflow enables
passive adoption of matching HMI read values. HMI-priority mode always disables
independent TMM requests; the assistant therefore no longer offers idle-window
polling controls. The proxy remains the exclusive owner of both ports, and
monitoring never opens a competing serial connection.

Its dedicated
**Configure serial buses and inverters** workflow detects adapters exclusively
by their stable `/dev/serial/by-id/...` links. Select one or more converters,
give every physical bus a unique name, and configure its baud rate, parity, and
timeout. The same workflow configures one to three inverters individually:
enabled state, display name, model, assigned bus, and Modbus slave address.
Slave addresses must be unique only within one physical bus, so two separate
buses may both use slave address 1. TMM never stores volatile `/dev/ttyUSB*`
names. Existing per-inverter channel selections are retained; nothing is saved
before review, a timestamped backup, and atomic validation.

The dedicated
**Configure field I/O sources and channels** workflow presents every supported source
as an independent checkbox. Each card retains its settings when disabled and has
its own editor for ID, label, stack address, polling interval, and—in the case of
field I/O—every individual channel. A channel can be disabled, shown live only,
or shown live and recorded. Analog and Multi-IO channels additionally expose
engineering scale, offset, unit, decimals, and SQLite change threshold. Smart Fan
has a separate cooling-policy editor. Nothing is written before the final review;
setup validates the draft, creates a timestamped backup, and replaces the JSON
atomically. The first menu also offers direct editing of `config.json` with
`nano` without changing other settings; use
`sudo /opt/tmm/setup.sh --edit-config` to open it directly.

The assistant can additionally enable, disable, or configure every optional
field-I/O source independently. For a configured source it
checks for `/dev/i2c-1`, optionally installs `i2c-tools` and the vendor Python
drivers, probes stack levels 0–7 without changing any card output, and writes a
minimal field-test declaration. The original configuration is backed up before
any change.

For enabled Sequent cards, setup reconciles the required drivers with the
configuration and installs them when needed: Smart Fan (`SMsfan`), Super
Watchdog & UPS (`SMwdt`), and the appropriate I/O drivers. It also loads the
I²C device driver and persists it for later starts. Setup does not actively probe
the Super Watchdog, because even a read can enable its watchdog function.

For the first analog field test, configure one known 0–10 V channel and set the
matching input range with Sequent's own tool before starting TMM. The setup asks
for the engineering conversion. The
Multi-IO setup creates a safe read-only declaration for all its input channels.
Further channels can subsequently be added in `config.json` using the documented
examples.

The assistant detects connected USB serial converters where possible, offers
their stable `/dev/serial/by-id/...` paths, and asks for the serial format,
inverter model and address, polling rates, database location, retention, web
port, investigation reference, and optional contact details. It creates a
timestamped backup of the existing configuration before writing the validated
settings and can restart both TMM services afterwards.

The installer creates the program, configuration, and data directories and then
starts two background services. Running it again updates the application without
overwriting the existing configuration or database.

## Uninstallation

To remove the TMM program and its system services while preserving configuration
and recorded measurements for a later reinstallation, run:

```sh
sudo /opt/tmm/uninstall.sh
```

For permanent removal of the local configuration, SQLite database, exports,
backups, and archives as well, use the deliberately explicit purge command:

```sh
sudo /opt/tmm/uninstall.sh --purge
```

The uninstaller does not remove shared packages such as Python, `i2c-tools` or
`dialog`, and keeps the `tmm` system user. This avoids disrupting other services
on the Pi.

## Offline installation bundle

For installations without internet access, create an offline bundle beforehand
on a **matching Raspberry Pi OS release and CPU architecture** with internet
access:

```sh
sudo ./prepare-offline-bundle.sh /media/usb/tmm-offline-bundle
```

The bundle contains the Debian packages (including their dependencies), Python
distributions for TMM, and all supported Sequent drivers. Copy the complete
TMM project directory and the bundle to the target Pi, then install entirely
locally:

```sh
sudo ./install.sh --offline-bundle /media/usb/tmm-offline-bundle
```

The installer validates the CPU architecture and uses `apt --no-download` plus
`pip --no-index`; it therefore does not fall back to the internet. Keep the
bundle with the service documentation, so a field technician can use it without
preparation. Afterward, `setup.sh` finds all Sequent Python drivers already in
the TMM virtual environment.

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
- **Communication bridge & bus observer:** active transparent HMI forwarding,
  stable endpoint assignment, independently calculated CRC evidence, and
  separately identified HMI and idle-window TMM transactions, including counts
  for measurements passively adopted from valid HMI reads
- **Storage & export:** data size, retention, remaining time, and CSV download
- **Measurement channels:** per-channel Off, Live, and Record modes

The history canvas observes its actual container size and redraws after section
expansion, dashboard reordering, fullscreen changes, window resizing, and return
from a background tab. Selected channels without valid retained samples are
excluded from scale calculation, while the remaining curves continue to render.
During zooming and panning, curves and digital state bars are clipped to their
plot regions; axis labels and surrounding controls therefore remain unobstructed.
- **Engineering:** optional nameplate values and machine-speed factor
- **Recording:** investigation reference, archive, and reinitialize controls
- **Parameters:** PCM002Z-compatible backup, import preview, partial restore,
  and an auditable parameter-change list

Yellow indicates a warning, red indicates a critical condition, and blue is
informational. These colors are monitoring aids. They do not replace drive
protection functions or assessment by qualified personnel.

### History analysis

History can combine analog and digital channels. Digital channels are rendered
as dedicated state lanes. Analog channels are automatically grouped by unit and
order of magnitude onto independently scaled axes; a channel can instead be
assigned manually to any of four axes. Curves can use step, linear, or bounded
spline rendering. Scroll to zoom, drag to pan, double-click for fullscreen, and
use the reset button to restore the complete interval. Right-click inside the
chart to add a temporary marker and a snapshot table below it. Left clicks are
reserved for panning and the fullscreen gesture; middle clicks do not create
markers. Markers remain in the browser session only and can be removed
individually.

Because history recording is change-based, the chart carries the most recently
stored analogue value forward to the right edge of the visible interval. This
is a display-only last-known-value hold; it does not insert artificial samples
into SQLite.

The live value flyout follows the temporary ruler without covering it: it is
shown to the right while sufficient space remains and automatically moves to
the left side near the chart's right edge.

The F, R, S1, S2, and S3 history lanes are reconstructed from the inverter's
authoritative `input_terminal_status` word when history is requested. This
keeps all terminal lanes synchronized and also makes older recordings usable
when their separately derived terminal rows are incomplete.

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
names must be globally unique. A Modbus slave address must be unique on its
assigned physical bus, but may be reused on a different bus:

```json
"serial_buses": [
  {
    "id": "production_line",
    "device": "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_BG03FPPT-if00-port0",
    "baudrate": 19200,
    "parity": "E",
    "stopbits": 1,
    "bytesize": 8,
    "timeout_seconds": 0.75
  },
  {
    "id": "test_bench",
    "device": "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_BG041YSU-if00-port0",
    "baudrate": 19200,
    "parity": "E",
    "stopbits": 1,
    "bytesize": 8,
    "timeout_seconds": 0.75
  }
],
"inverters": [
  {"name": "AS3-Machine", "model": "VF-AS3J", "bus_id": "production_line", "slave_id": 1, "enabled": true},
  {"name": "S15-Test", "model": "VF-S15", "bus_id": "test_bench", "slave_id": 1, "enabled": true}
]
```

Each named bus opens its own serial converter. Polling, parameter backups,
preflight reads, and verified writes are routed through the bus assigned to the
respective inverter. New named-bus configurations accept stable
`/dev/serial/by-id/...` paths only. The older single `serial` object remains
readable so an existing installation can be migrated in the setup assistant.

Profiles select the documented monitor registers automatically. Custom register
lists are supported, but should only be added after checking the communication
manual for the exact drive model.

### Measurement channels and engineering values

The dashboard can change channels without editing JSON. `Off` normally stops
polling the channel, `Live` polls it but retains only its current value, and
`Record` also writes relevant changes to history. `operating_status` remains
internally polled because it is required for safe monitoring and parameter-write
interlocks, even while its user-facing mode is `Off`.

A fresh installation starts with every user-facing measurement channel set to
`Off`; TMM never guesses which process data should be retained. The operator
must deliberately select `Live` or `Record`. Internally required safety and
configured alert monitors may still be polled while shown as `Off`, but their
values are not written to measurement history unless recording is selected.

### Condition Monitoring and milestones

The **Condition Monitoring & milestones** category turns live measurements into
auditable events without requiring program code. Each operand selects a source
and metric and compares it with `>`, `>=`, `<`, `<=`, `=`, `!=`, or Boolean
`NOT`. The web editor can add further operands and combine them with `AND`,
`OR`, or `XOR`. `XOR` is true when exactly one operand is true. The displayed
rule expression updates immediately, so the technician can verify the complete
logic before saving it.

`AND` requires every operand to be true. `OR` requires at least one true
operand. The minimum duration applies to the completed expression, not to each
operand separately. Hysteresis and equality tolerance remain individual
settings for every operand. Severity and the Enabled switch apply to the rule
as a whole.

Rules are stored under `condition_monitoring.rules` in `config.json`. Runtime
state survives collector restarts. When a condition becomes active, and again
when it clears, TMM writes an immutable row to the SQLite `milestones` table.
The row retains the rule ID, rule revision, name, severity, triggering value,
unit, operator, target, and a JSON snapshot. For compound rules, that snapshot
also contains the complete expression and the observed result of every
operand. Editing a rule increments its revision and never rewrites older
milestones.

Equality on analogue values uses `tolerance`; it is not a raw floating-point
comparison. Hysteresis changes the release boundary and prevents a rule from
repeatedly entering and clearing around its threshold. The duration timer
advances only while the complete expression remains true. Every operand must
have supplied at least one current value before TMM can evaluate the expression.
A channel used by a rule must therefore be internally polled; choose Live or
Record if it is not already a safety or alert monitor.

Persistent milestones appear as severity-coloured vertical markers in the
history chart and as a recent-event list in the Condition Monitoring category.
Temporary chart markers remain browser-local and are not SQLite milestones.

### Live-card order

The **Current measurements** cards can be arranged by drag and drop. The order
is saved atomically in `web.live_card_order` in `config.json`, remains after a
service restart, and has no effect on Modbus polling or recording.

The dashboard categories can also be arranged vertically. Their order is a
per-browser user preference stored locally by the web browser. The server-side
order is used only as the initial fallback when that browser has no saved
preference. Added or removed categories do not invalidate an existing layout.

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

An interval of `0.2` seconds means five polls per second. VF-AS1, VF-S11, and
VF-S15 limit Modbus function 03 to one 16-bit word per request, which TMM
handles automatically. VF-AS3J can read suitable nearby registers in blocks.
The VF-S15 profile has been verified against a physical drive; enable its
Modbus-RTU mode with parameter `F829 = 1` and restart the drive after changing
that setting.

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

Live-card colours use the alert limits under `alerts.metrics`. `warning` and
`critical` are upper limits. A metric may additionally define the pair
`warning_low` and `critical_low` for lower-limit monitoring. Normal analogue
signals are green, the first relevant deviation or warning-limit violation is
yellow, and three consecutive abnormal updates become red. Crossing a critical
limit is red immediately. Add-on analogue channels use their
`change_threshold` as the deviation deadband.
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

The storage projection needs at least five minutes of real size samples. It
uses the change in allocated SQLite pages over time and the free disk space.
Fixed database overhead and the bounded WAL file are therefore not mistaken
for continuing growth. The result is an estimate, not a guaranteed deadline.

When estimated free-space runtime is shorter than the selected retention period,
TMM displays a blue storage information message. No message is shown when the
selected storage medium is expected to cover the configured retention period.

### Pi thermal protection

At 75 °C TMM doubles its collection interval and records the transition in
SQLite and CSV. If the temperature returns below 70 °C, normal timing resumes.
If 75 °C is reached again while throttled, collection pauses until the Pi has
cooled below 70 °C. Both throttling and pausing are shown as dashboard alerts.

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
model-specific profiles and single-register reads for VF-AS1, VF-S11, and
VF-S15 to avoid unsupported blocks.

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

**Product:** Toshiba Modbus Monitor (TMM)<br>
**Version:** 1.3.0<br>
**Operating mode:** long-term monitoring with optional guarded parameter service

Version 1.3 is feature-frozen. Maintenance of this line is limited to documented
bugfix releases as defined in `RELEASE_POLICY.md`. Planned product development is
tracked separately in `ROADMAP.md`.
