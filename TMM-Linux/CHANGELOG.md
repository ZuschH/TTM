# Changelog

## Bugfix 1.3.0-rc3 - 2026-11-22

- Remove third-party Sequent PDFs from the public source and release package;
  use official publisher links when no verified local copy is installed.
- Add a checksum-pinned downloader for online installations and locally built
  offline bundles, without placing vendor documents under the TMM MIT license.
- Add the MIT license and third-party notice directly to the Linux release.

## 1.3.0 - 2026-11-21

- Freeze the TMM Linux Master 1.3 feature set at development baseline r133.
- Normalize runtime, API, dashboard, systemd and documentation versions to 1.3.0.
- Establish patch-only Bugfix maintenance for the 1.3 line and publish the
  post-1.3 roadmap with tested Toshiba parameter-set import/export as its primary
  objective.

## Development revision r133

- Align the 3.3 V logic-source ground terminal and connection horizontally in the offline GPIO schematic, avoiding an unintended visual implication from the former diagonal line.

## Development revision r132

- Add an offline GPIO connection and safety schematic with physical 40-pin header numbers, BCM identities and TMM-supported input pins.
- Illustrate dry-contact and 3.3 V logic wiring while prominently prohibiting direct 5 V/24 V machine connections.
- Link the locally installed schematic from both configured GPIO cards and grey GPIO support-reference cards in the browser.
- Include and preflight the GPIO PDF in every installation archive.

## Development revision r131

- Keep every supported GPIO, Sequent field-I/O, Smart Fan and UPS hardware type visible as a grey support-reference card when it is not configured on the current TMM.
- Clearly distinguish unconfigured reference hardware from configured-but-disabled and configured-but-faulted devices.
- Prevent reference cards from offering actions, polling hardware or generating missing/stale hardware alerts while retaining offline documentation links for telephone support.

## Development revision r130

- Show a permanent, high-contrast electrical-safety warning directly on every Raspberry Pi GPIO configuration card.
- State explicitly that GPIO is limited to 3.3 V, that 5 V/24 V and machine signals must never be connected directly, and that a passive terminal HAT provides neither galvanic isolation nor overvoltage protection.
- Translate the warning into every supported dashboard language.

## Development revision r129

- Add a read-only Raspberry Pi GPIO source for passive screw-terminal HATs, with stable BCM-based channel identities and the same Live/Record/Off workflow as other field I/O.
- Support per-input pull-up, pull-down or floating configuration and optional active-low interpretation; newly added channels remain disabled by default.
- Reserve I²C, SPI and UART pins from the setup defaults, grant the collector only the required `gpio` group access, and keep all GPIO output operations outside TMM 1.3.
- Include GPIO channels in live cards, history, CSV export and condition-monitoring catalogs, with a complete initial 0/1 baseline after each recording reset.

## Development revision r128

- Calculate recording growth from occupied SQLite pages and add reusable database pages to effective remaining capacity, keeping forecasts correct after a logical database reset reuses an already allocated file.
- Scope growth samples to the current persistent recording generation instead of mixing measurements from previous investigations.
- Make proxy administration self-healing after an unexpected SQLite error so later archive/delete requests cannot remain permanently pending.
- Synchronize every add-on collector and the passive proxy decoder through `recording_info.created_at`, eliminating the race inherent in short-lived result-file notifications.
- Retry add-on SQLite maintenance locks without reporting a false card outage, discard pre-reset samples, and force a complete post-reset baseline including explicit digital 0 and 1 states.
- Bound live-data requests and update external-I/O cards as soon as either the channel metadata or latest values arrive, preventing a slow diagnostic request from freezing analogue live values.
- Report a stable recording explicitly when the current generation has accumulated enough observation time but shows no net database growth.

## Development revision r127

- Retry transient SQLite `database is locked`/`busy` responses instead of silently losing the accepted proxy diagnostic transaction.
- Increase the default non-blocking persistence buffer from 4,096 to 65,536 transactions while retaining bounded memory and uninterrupted serial forwarding.
- Expose queue capacity, permanent failures, lock retries, and success/error timestamps; clear stale active errors after recovery.
- Distinguish an active backlog from a recovered historical diagnostic gap in the bridge display.

## Development revision r126

- Run recording-database administration in a dedicated worker when TMM operates as a transparent proxy; proxy mode previously bypassed the normal collector loop that consumes these requests.
- Keep archive/delete work completely outside the timing-critical serial forwarding loop and preserve uninterrupted HMI priority.
- Include retained Modbus proxy evidence in archive/reset operations so a new investigation really starts with an empty live database.

## Development revision r125

- Assign every recording-database reinitialization a unique operation ID and expose its pending state through the API.
- Keep checking the exact accepted operation once per second until the collector returns an explicit success or error result.
- Prevent duplicate archive/delete requests while one is being tracked and report delayed confirmation without falsely claiming completion.

## Development revision r124

- Recognize an otherwise valid `config.json` followed only by one or more accidental closing braces.
- Offer a dedicated one-step repair instead of requiring a manual editor session for this unambiguous syntax error.
- Preserve the invalid original with metadata and a timestamped backup, reject all other trailing content, and atomically revalidate the repaired JSON before setup continues.

## Development revision r123

- Validate `/etc/tmm/config.json` before the setup assistant performs hardware discovery or opens a configuration workflow.
- Report the exact JSON error with nearby numbered lines instead of reducing it to an unexplained `Extra data` dialog.
- Detect concatenated complete JSON objects and offer an explicit choice between the first and last document.
- Preserve the invalid original with ownership, permissions, and a timestamped backup before atomically installing and revalidating the selected document.
- Leave running services untouched when repair is declined; a fresh SQLite recording remains independent from configuration repair.

## Development revision r122

- Refresh add-on state directly after an individual recording toggle so the disk button immediately reflects the persisted mode.
- Add explicit actions to stop history recording for the selected source or for every configured drive, communication metric, and add-on channel.
- Preserve Live channels when recording stops (`Record` becomes `Live`); channels recorded while hidden become `Off`, avoiding unwanted polling and storage work.
- Keep graph selection (`All` / `None`) visibly separate from acquisition and recording controls.

## Development revision r121

- Keep configured Smart Fan, UPS, and field-I/O sources in the Measurement history data-source dropdown before any sample has been recorded.
- Prevent the authoritative retained-metric catalogue from pruning a configured add-on merely because all of its channels are currently Off.
- Interpret disabled add-on channels consistently as `Off`, allowing the history-card controls to activate them directly.

## Development revision r120

- Restore Smart Fan and UPS measurements as selectable data sources directly inside their System cards.
- Offer Off, Live, Record, and Hide-from-Live modes for every system-card metric, using the existing validated add-on channel API.
- Expose the complete metric catalogue even when every system-card channel was previously disabled, so a source can always be enabled again through the web interface.

## Development revision r119

- Stop reporting `No recent card data` when an add-on intentionally has no Live or Record measurement channel selected.
- Treat the collector health probe as the authoritative card-contact signal in that state and show `Card communication verified — no measurement channels selected` in External I/O.
- Continue raising a critical alert immediately for a real driver or I²C error, and retain stale-data information for measurement channels that are actually active.

## Development revision r118

- Replace raw FastAPI `403` JSON in the dashboard with a localized, actionable explanation when remote administration is disabled.
- Point technicians to the exact `web.allow_remote_administration` setting and required `tmm-web` restart without weakening the default write protection.
- Handle rejected UPS policy changes inside the System card just like rejected cooling-policy changes instead of leaving an unhandled browser promise.

## Development revision r117

- Confirm every enabled Sequent card with one successful health cycle even when all of its user-facing channels are disabled.
- Replace stale driver or I²C errors immediately after a successful startup, configuration reload, or communication recovery without writing empty cycles continuously.
- Log a distinct `add-on communication verified` message after the first proven hardware poll so a worker start can no longer be mistaken for physical card verification.

## Development revision r116

- Prevent the Smart Fan setup path from attempting to compile the obsolete `RPi.GPIO` C extension on aarch64 Python 3.13.
- Install the current `SMsfan` wheel without its inaccurate legacy dependency metadata and install the dependencies its implementation actually imports (`gpiozero` and `smbus2`) explicitly.
- Apply the same dependency handling to interactive setup, configured-driver repair, normal offline installation, and offline-bundle preparation.

## Development revision r115

- Add compound Condition Monitoring rules with validated `AND`, `OR`, `XOR`, and grouped `NOT` expression nodes while retaining compatibility with existing single-operand rules.
- Add a technician-facing multi-operand rule editor with live syntax-coloured expression preview, per-operand comparison settings, and clear add/remove controls.
- Define `XOR` as exactly one matching operand and require a current value from every referenced measurement before evaluating a compound expression.
- Store the complete logic tree, trigger, current operand values, and individual match results in every new milestone snapshot.
- Show the compound expression both in saved-rule cards and in the recent-milestone list.

## Development revision r114

- Move proxy transaction logging, passive HMI-response decoding, measurement storage, and retention cleanup from the serial forwarding loop into a bounded background persistence worker.
- Make persistence submission non-blocking: if storage cannot keep up, diagnostic records are dropped and counted instead of delaying HMI traffic.
- Process retention deletion in bounded 1,000-row batches outside the forwarding thread instead of performing an unbounded hourly delete inline.
- Enforce HMI-priority mode by suppressing all configured scheduled TMM Modbus requests while retaining passive observation of valid HMI responses.
- Publish persistence queue depth, high-water mark, processed count, dropped count, and worker errors in proxy runtime diagnostics.

## Development revision r113

- Increase the horizontal clearance between the temporary history ruler and its live-value flyout from 14 to 28 pixels on both sides.
- Retain the automatic right-to-left flyout switch while making the inspected position easier to see.

## Development revision r112

- Reconstruct F, R, S1, S2, and S3 history lanes from every stored `input_terminal_status` word instead of relying on potentially incomplete independently persisted derived rows.
- Apply the configured inverter model's terminal-bit layout during reconstruction, including the VF-AS3J mapping.
- Keep terminal lanes synchronized across upgrades, configuration changes, and recordings made before an individual derived lane existed.

## Development revision r111

- Position the history value flyout to the right of the temporary ruler while it fits and move it completely to the ruler's left side before it reaches the chart edge.
- Keep the inspected curve position and ruler visible instead of clamping the flyout over them at the right side of the chart.

## Development revision r110

- Carry each analogue series' last known value to the right edge of the visible history interval, matching TMM's change- and threshold-based SQLite recording semantics.
- Keep this last-known-value hold entirely in the renderer; no synthetic samples are written to SQLite.
- Prevent stable live signals from appearing to stop merely because another selected series has a newer stored change point.

## Development revision r109

- Create temporary history markers exclusively with a right-click inside the chart and suppress the chart's browser context menu for that gesture.
- Reserve the primary mouse button for panning and double-click fullscreen so entering fullscreen no longer creates one or two accidental markers.
- Ignore middle-button clicks for marker creation and suppress their auxiliary-click action inside the chart.

## Development revision r108

- Clip analogue curves to the numeric plot rectangle so the retained pre-viewport sample cannot draw across left or right axis labels after wheel zooming or panning.
- Clip digital state bars to their dedicated lane area while preserving continuous states at viewport boundaries.

## Development revision r107

- Redraw the history canvas after section expansion, dashboard reordering, fullscreen changes, tab visibility changes, and real container resizes.
- Ignore zero-size hidden layouts instead of resetting the canvas to an unusable bitmap and retry after the browser has completed layout.
- Exclude empty or invalid series from axis calculation so channels without retained history cannot create infinite domains or suppress valid curves.
- Prevent older overlapping history requests from overwriting a newer channel selection and retain successfully loaded series when one request fails.
- Cap canvas pixel density at 2x to keep large multi-channel plots responsive on high-DPI displays.

## Development revision r106

- Start every configured Sequent add-on collector alongside the transparent Modbus proxy instead of limiting I²C polling to classic direct-Modbus mode.
- Keep each Sequent card on its existing independent worker and SQLite connection so HAT timing remains isolated from HMI forwarding and scheduled inverter reads.
- Stop and join all add-on workers cleanly when the proxy service terminates.

## Development revision r105

- Reduce the configurable scheduled-polling silence guard and inter-poll gap minimum from 50 ms to 5 ms.
- Automatically shorten the upstream wait resolution to the configured silence guard so sub-100-ms bus gaps can actually be detected.
- Use a conservative 20-ms silence guard and 20-ms inter-poll gap for new proxy configurations while retaining the bounded downstream response timeout and passive HMI decoding.

## Development revision r104

- Decode valid HMI Modbus read transactions passively and store matching configured inverter measurements through the normal change-aware SQLite path.
- Keep passive decoding entirely read-only and isolated from transparent forwarding; decoding or SQLite failures cannot intentionally interrupt HMI traffic.
- Show adopted HMI reads and measurements in communication diagnostics and mark adopted values in the RTU evidence logbook.
- Preserve optional idle-window polling for configured measurements that the HMI does not request.

## Development revision r103

- Implement optional independent TMM monitoring through the proxy-owned downstream port in verified HMI idle windows.
- Preserve HMI priority with a configurable silence guard, one-register reads, a response timeout capped at 250 ms, queued-data checks, and minimum spacing between TMM requests.
- Store normal TMM measurements through the existing change-aware SQLite path while identifying HMI and TMM-originated RTU transactions separately in diagnostics and the evidence logbook.
- Add guided proxy setup for idle-window polling and document its safety limits and operation.

## Development revision r102

- Classify CRC-invalid HMI requests as `request_crc_error`, include them in the communication CRC-error counter, and do not forward them to the inverter.
- Keep partial frames distinct from CRC failures so the summary and RTU evidence logbook describe the same fault consistently.

## Development revision r101

- Add an expandable Modbus RTU evidence logbook to Communication diagnostics.
- Show recent HMI requests and inverter responses as raw hexadecimal bytes together with received and independently calculated CRC, validity, outcome, slave/function bytes, and latency.
- Keep the logbook collapsed by default and fetch its bounded data only while opened or explicitly refreshed.

## Development revision r100

- Add a conservative fallback for adapter reversal detection: repeated drive-side activity while no HMI-side request has ever arrived now reports inconsistent traffic direction even when frame reconstruction is incomplete.
- Keep the stricter repeated CRC-valid Modbus request evidence as the preferred reversal proof and expose the evidence type and burst counters through runtime diagnostics.

## Development revision r99

- Detect repeated, valid Modbus master requests arriving on the configured inverter-side adapter and report a probable adapter reversal without changing configuration automatically.
- Present adapters as friendly A/B roles with their short USB serial number while retaining the full stable path as a tooltip.
- Surface a suspected reversal as a critical dashboard message and red endpoint highlighting in all supported languages.

## Development revision r98

- Prevent stale dashboard HTML, JavaScript, and CSS with explicit no-store/no-cache response headers.
- Advance both dashboard asset versions together so the connected-adapter indicators become visible immediately after an update.

## Development revision r97

- Show a permanent green confirmation when both configured serial converters are detected by the host.
- Mark each detected endpoint with a green card border and an explicit connected badge; keep missing endpoints red.
- Create endpoint badges dynamically as a fallback for an older cached dashboard document.

## Development revision r96

- Identified every missing proxy adapter by its HMI/drive role and stable device
  path in clear text.
- Highlighted the affected endpoint card and added a critical dashboard message
  when a configured USB serial converter is not connected.

## Development revision r95

- Added automatic proxy reconnect after an adapter disappears, is busy, or
  raises a serial I/O error; the collector no longer exits on these failures.
- Published the current runtime state and last connection error to the web UI.
- Added physical adapter-presence checks and rejected accidentally concatenated
  `/dev/serial/by-id/...` paths during configuration validation.

## Development revision r94

- Removed the optional external hardware bypass from the proxy readiness
  checklist; it is now a neutral availability note rather than a failed check.
- Corrected the implementation-phase display to mark passive observation as
  complete and transparent proxy forwarding as the active phase.

## Development revision r93

- Replaced stale active-polling diagnostics with proxy transaction statistics
  whenever transparent proxy mode is enabled.
- Added forwarded/error counts, telegram rate and age, response latency, CRC
  errors, timeouts, and partial-request counts to the Communication category.
- Prevented historical polling errors from being presented as current proxy
  failures.
- Added a runtime heartbeat so “active” now means that the proxy process has
  both ports open and is alive, rather than merely configured as enabled.

## Development revision r92

- Made the bridge renderer tolerant of mixed HTML/JavaScript update states and
  absent optional nodes instead of aborting the complete dashboard refresh.
- Added stable IDs for bridge help and warning elements and a new static asset
  revision to force consistent browser loading after an update.

## Development revision r91

- Added bridge state to the established dashboard metadata response so the
  active proxy remains visible even if the dedicated bridge request fails.
- Added cache-busting to live bridge requests and replaced the misleading
  catch-all “backend reload pending” state with the actual request error.

## Development revision r90 — active transparent proxy

- Added an exclusive two-adapter Modbus RTU proxy mode between an HMI/master
  and inverter/slave; active TMM polling is disabled whenever this mode runs.
- Forwarded complete HMI requests and inverter responses byte-identically,
  without synthesizing, correcting, retrying, or de-duplicating commands.
- Added SQLite transaction logging with raw frames, slave and function codes,
  CRC state, response latency, timeout outcome, and timestamps.
- Added guided `/dev/serial/by-id/...` endpoint selection to `setup.sh` and
  exposed active proxy state in the multilingual web interface.
- Rejected partial requests instead of forwarding incomplete commands and kept
  frame-log failures isolated from the time-critical forwarding path.

## Development revision r89

- Added named multi-adapter RS485 buses using mandatory stable
  `/dev/serial/by-id/...` paths.
- Added a dialog-based serial topology editor to `setup.sh` for selecting every
  detected adapter and configuring one to three enabled or disabled inverters.
- Added per-inverter bus assignment and allowed equal Modbus slave addresses on
  different physical buses while rejecting duplicates on the same bus.
- Routed polling, PCM backups, preflight checks, and verified parameter writes
  through the collector belonging to the selected inverter's bus.

## Development revision r88

- Replaced the raw `404 Not Found` bridge badge during a mixed frontend/backend
  update with a localized, non-alarming backend-reload status.
- The design-only topology, phases, observations, and safety checks now remain
  visible while an older web process is still serving the API.

## Development revision r87 — 1.3 communication bridge foundation

- Added a multilingual Communication Bridge & Bus Observer dashboard category
  with the intended HMI–TMM–inverter topology.
- Added a read-only bridge-design API describing both serial endpoints,
  implementation phases, planned observations, and safety-readiness checks.
- Kept the entire bridge foundation hard-disabled: no serial port is opened and
  no traffic is forwarded in this revision.
- Raised the development version to 1.3.0-dev and documented deterministic
  forwarding, write de-duplication, watchdog, and hardware-bypass requirements.

## Development revision r86

- Corrected the VF-AS3J access profile against Toshiba E6582143: monitor values
  are now read with the dedicated one-word request instead of direct blocks
  whose address interpretation depends on inverter parameter `F830`.
- Retained the documented `FC90`-`FC92`, `FD04`-`FD05`, `FD28`, and `FE40`
  monitor objects while preventing them from being combined into requests.

## Development revision r85

- Fixed incomplete Linux updates being able to install the condition-aware
  collector without its `tmm_conditions.py` companion module.
- Added a complete release-file and Python syntax preflight before modifying an
  installation, plus an installed-module import check before service restart.

## Development revision r84

- Grouped known condition operands by monitored source and added live syntax
  highlighting for operands, operators, values, units, and durations.
- Applied the same stable per-measurement colours to saved rules and milestones.

## Development revision r83

- Corrected the remaining-storage forecast to use measured SQLite page growth
  instead of dividing the complete database and WAL size by recording age.
- Fixed database overhead no longer causes a false capacity warning shortly
  after installation; forecasts wait for five minutes of real growth samples.

## Development revision r82 — 1.2 Condition Monitoring foundation

- Added persistent condition rules with `>`, `>=`, `<`, `<=`, `=`, `!=`, and
  `NOT` operators, minimum duration, equality tolerance, and hysteresis.
- Added versioned SQLite milestones for condition entry and return events plus
  persistent runtime state across collector restarts.
- Added a multilingual Condition Monitoring category for creating, editing,
  enabling, and deleting rules and reviewing recent milestones.
- Added severity-coloured milestone markers to the measurement-history chart.

## Development revision r81

- Changed fresh installations to opt-in channel selection: no inverter,
  communication, field-I/O, UPS, or cooling channel records by default.
- Safety and alert registers may remain internally polled without being shown
  or written to measurement history.
- Added complete disabled channel templates for new Smart Fan and UPS cards.
- Changed explicit Record selections to be stored in configuration now that a
  missing channel entry consistently means Off.

## Development revision r80

- Added green, yellow, and red card surfaces for analogue measurements and
  decoded status words.
- Analogue changes respect each channel's configured change threshold; three
  consecutive abnormal updates escalate from yellow to red.
- Added optional lower warning and critical threshold evaluation in the live
  display alongside the existing upper thresholds.

## Development revision r79

- Applied the subtle inactive/active card surfaces to binary signals across
  every live-view category, including inverter terminals and external I/O.
- Added state highlighting to the UPS battery-runtime card: mains/charging is
  active, while battery operation is inactive.

## Development revision r78

- Fixed dashboard category-order saves being rejected after the External I/O
  and System power & cooling categories were added.
- Category order is now retained per browser/user, with the server-side order
  used as a fallback for a browser without a saved preference.
- Saved layouts tolerate categories added or removed by later revisions.

## Development revision r77

- Storage information is now shown only when the configured retention period
  exceeds the estimated capacity of the selected storage medium.
- The capacity notice uses the blue information severity requested for this
  advisory condition.

## Development revision r76

- Expanded the maximum three live cards per row across the full container width.
- Removed redundant add-on group names from individual live-card titles.
- Added distinct inactive and active surface colors for digital signal cards.

## Development revision r75

- Added a `dialog`-based Sequent card manager to `setup.sh`.
- Cards can be enabled or disabled independently and retain their settings.
- Added per-card stack, identity, interval, channel-mode, engineering-scaling,
  change-threshold, and Smart Fan policy dialogs.
- Drafts are validated, backed up, and atomically saved only after review.
- Fixed empty Sequent driver arrays under Bash `set -u`.
- Corrected the VF-S15 regression expectation to its verified single-word reads.

All notable changes to Toshiba Modbus Monitor (TMM) are documented here.

## 1.1.0 — 2026-09-23

### Added

- Sequent Digital Inputs, Analog Inputs DAQ, Multi-IO, Smart Fan, and Super
  Watchdog & UPS integration with independent channel controls.
- Sortable live-card groups and a four-column live view.
- Advanced history analysis: independent analog axes, step/linear/spline
  curves, pan, zoom, fullscreen, tooltips, temporary markers, and CSV export.
- Pi thermal protection with recorded throttle and pause transitions.
- Guided `dialog`-capable setup, direct configuration editing, safe uninstall,
  and verified offline installation bundles.

### Changed

- External I/O is now configuration-focused; active channels appear in the
  sortable live view and history workflow.
- Storage exhaustion before the configured retention period now raises a
  warning, escalating to critical below seven days.
- Live-card values and units are aligned independently for easier scanning.
- French and Japanese translations cover system UPS and cooling controls.

### Fixed

- Per-channel Live-view visibility for field I/O and Multi-IO cards.
- Initial digital states are retained for history rendering.
- Smart Fan policy values are reflected promptly in the dashboard.
- VF-S15 Modbus polling now uses the documented single-register reads; the
  profile is verified on physical hardware with `F829 = 1`.
