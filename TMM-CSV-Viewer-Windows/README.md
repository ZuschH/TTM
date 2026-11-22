# TMM CSV Viewer

TMM CSV Viewer is a separate, offline Windows tool for inspecting CSV exports
created by Toshiba Modbus Monitor. It does not require a running TMM service,
a Modbus connection, or internet access.

## Features

- opens the standard TMM CSV export format;
- validates the required columns and skips malformed measurement rows;
- detects inverters and measurements automatically;
- displays the durable investigation reference included in newer TMM exports;
- offers inverter, measurement, and time-range filters;
- provides All, None, Analog values, Operating status, and Terminals selection
  presets while retaining individual channel checkboxes;
- groups measurements into frequency, load, temperature, status, event, and
  device-information sections;
- gives unlike units their own chart areas and scales;
- recognizes the extended VF-AS1 speed-feedback, calculated-speed, torque,
  current-component, load-factor, overload-factor, and power channels;
- displays the machine speed already calculated and recorded by TMM from the
  configured per-drive transmission factor;
- displays the calculated output current in amperes and output voltage in volts
  when TMM was configured with the corresponding rated reference values;
- draws every digital status as a separate logic-analyzer lane, using colored
  blocks for active periods so simultaneous signals never obscure each other;
- decodes the F, R, S1, S2, and S3 terminal bits into individual on/off
  tracks, with automatic or manually selectable inverter layout;
- decodes current and retained operating-status words into separate tracks for
  Trip, emergency stop, alarm, running, direction, coast stop, and readiness;
- shows a prioritized operating-state summary, hexadecimal raw word, and all
  active status bits in the pointer tooltip;
- derives alarm activations, alarm clearances, trip occurrences, and trip
  clearances from actual state transitions and lists them in an event table;
- shows retained `past_trip_1` through `past_trip_4` values in a separate trip
  memory table because their CSV read time is not the original fault time;
- keeps retained trip frequency, status, current, DC-input voltage, and output
  voltage in a dedicated latest-trip snapshot instead of drawing them as live
  measurement curves;
- lists capacity, series, CPU, CPU2, and EEPROM values in a dedicated device
  information table instead of treating static raw values as curves;
- limits the chart selector to meaningful time-series measurements and status
  words, preventing diagnostic codes from distorting the numeric axes;
- recognizes TMM communication-state records, shades unreachable periods,
  interrupts held curves and digital tracks while communication is unavailable,
  reports online/degraded/unreachable in the tooltip, and lists status
  transitions in the event table;
- supports mouse-wheel zooming, click-and-drag navigation, and view reset;
- reconstructs change-only recordings at the visible window boundaries:
  the last recorded value is held until the next change, preventing invented
  ramps between sparse records;
- offers hold-last-value, linear, and bounded spline curve styles; digital
  signals always retain their factual rectangular representation;
- calculates time-weighted averages instead of treating irregular change
  records as cyclic samples;
- retains local minima and maxima when large datasets are reduced for drawing;
- draws multiple selected measurements in one interactive chart;
- shows pointer values, temporary click-to-add analysis markers with snapshots,
  and basic statistics;
- processes the CSV in the browser on the local Host-System only.
- offers the complete user interface in US-English, German, French, and
  Japanese; the chosen language is retained in the local user profile, including
  when a later viewer launch uses a different loopback port.
- includes the recognizable TMM product footer, version information, and a
  local link to this user manual.

## Privacy and data handling

The selected CSV is read and analysed solely in the local browser session. The
viewer does not upload the CSV, does not require an internet connection, and
does not modify the source file. It can therefore be used to inspect recordings
received from a remote TMM installation without connecting to that installation.

## Windows installation

Use the self-contained `TMM-CSV-Viewer-Setup-1.1.1.exe` package. It installs a
separate local viewer below `%ProgramFiles%\TMM CSV Viewer`, creates a Start
Menu entry, and can optionally add a desktop shortcut. The viewer starts a
local browser page on a free loopback port; no Windows service, Modbus adapter,
database, or running TMM Monitor is required.

The viewer includes a private Python runtime and needs no separately installed
Python on a normal target system.

## Run from source

On Windows, use a Python 3 installation:

```powershell
python .\tmm_csv_viewer.pyw
```

For development without automatically opening a browser:

```powershell
python .\tmm_csv_viewer.pyw --no-browser --port 8090
```

Then open `http://127.0.0.1:8090/`.

## Supported CSV columns

```text
observed_at,inverter,slave_id,metric,register_address,raw_value,value,unit
```

## Building the Windows installer

On a Windows build host with Inno Setup 7, prepare the runtime and application
staging before compiling:

```powershell
.\installer\prepare-runtime.ps1 -PythonExe 'C:\Program Files\TMM\runtime\python.exe'
.\installer\prepare-app.ps1
.\installer\build-installer.ps1
```

Any working 64-bit Python installation can replace the `-PythonExe` value. The
viewer itself uses only the Python standard library. The final executable is
written to `installer\output\TMM-CSV-Viewer-Setup-1.1.1.exe`.
In addition to Toshiba data, the viewer recognizes the optional TMM V1.1
`metric_label` export column used by Linux add-ons. Sequent external I/O
channels retain their configured names, units and scaling in offline analysis.
Digital `on/off` channels are drawn as stepped, colored digital tracks; analog
channels are grouped under **External I/O** and use their exported engineering
unit (for example `bar`). Older V1.0 CSV files remain fully supported.

## Linux Master 1.3 CSV compatibility

Viewer 1.1.1 accepts the current Linux Master 1.3.0 export schema, including
communication samples and `system.thermal_protection` records. It preserves
unknown columns and future channel names unchanged and offers a normalized
UTF-8 export after inspection. See `docs/master-1.3-csv-compatibility.md` for
the precisely verified interchange contract and current limits.
