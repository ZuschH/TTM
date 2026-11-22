# TMM Linux Master 1.4 roadmap

Version 1.3 remains feature-frozen. The following work explicitly targets
version 1.4 and does not enter 1.3 except as an independently justified bugfix.

## Primary objective: tested Toshiba parameter-set import and export

The next feature line shall provide a reproducible, audited workflow for Toshiba
inverter parameter sets. A successful implementation must do more than parse or
write a CSV file: it must prove identity, compatibility, safety and round-trip
fidelity.

### 1. Canonical interchange contract

- Define one versioned, UTF-8 interchange schema shared by Linux Master and the
  Windows CSV Viewer.
- Preserve model family, exact drive identity where available, parameter address,
  raw word, signed/unsigned interpretation, display value, unit, source format,
  export timestamp and schema version.
- Specify delimiter, decimal separator, quoting, line endings and byte-order-mark
  handling explicitly; accept documented Windows and PCM002Z variants without
  silently changing values.
- Retain unknown and unsupported parameters losslessly instead of discarding them.

### 2. Import validation before any write

- Reject malformed, duplicate, ambiguous and out-of-range entries with row-level
  diagnostics.
- Compare source model/family and capacity metadata with the connected inverter.
- Classify every difference as unchanged, writable, unsupported, identity-critical
  or safety-critical.
- Produce a deterministic preview and require explicit technician selection; an
  import must never imply an automatic full-device restore.

### 3. Guarded execution and evidence

- Reuse fresh safe-standstill checks before every selected write.
- Read the current value, write one parameter, read it back and persist the result
  before continuing.
- Stop on the first failed safety check or verification mismatch; never claim an
  atomic rollback that the inverter cannot guarantee.
- Export an immutable audit report containing requested, previous, read-back and
  final values plus timestamps and device identity.

### 4. Test programme and acceptance gates

- Golden-file tests for PCM002Z and the canonical interchange schema.
- Round-trip tests: export -> import -> export must preserve all supported and
  unknown records byte-for-byte where the format permits, otherwise semantically.
- Cross-platform fixtures proving identical interpretation in Linux Master and
  Windows CSV Viewer.
- Hardware-in-the-loop tests for each supported Toshiba family, including wrong
  model, interrupted communication, rejected parameter, verification mismatch
  and recovery after a partial batch.
- Release acceptance requires signed test evidence and successful restore to a
  non-production test inverter before any production recommendation.

## Explicit 1.4 objective: Condition Monitoring Milestones

Version 1.4 shall turn the condition and milestone foundation from 1.3 into a
complete, testable service workflow. Milestones must remain meaningful after a
collector restart, database archive, long-running investigation and transfer to
the Windows CSV Viewer.

- Preserve the exact rule ID and revision, Boolean expression, thresholds,
  tolerance, hysteresis and minimum duration that produced each milestone.
- Record condition entry, recovery and acknowledgement as distinct, immutable
  events with timestamps, severity and the triggering measurement snapshot.
- Allow technicians to add clearly distinguished manual milestones and service
  notes without altering automatically generated evidence.
- Correlate milestones with the measurement history, communication diagnostics,
  trips and parameter-change audit while retaining the original source data.
- Export and import milestones through a versioned interchange contract shared
  with the Windows Viewer; unknown future fields must be preserved losslessly.
- Test rule changes, AND/OR/XOR expressions, collector restarts, clock/time-zone
  handling, database reinitialization and duplicate-event prevention.
- Provide a deterministic timeline and filters suitable for both remote service
  analysis and a documented machine investigation.

Parameter-set interchange remains the primary 1.4 objective. Condition
Monitoring Milestones are the second explicit and mandatory 1.4 product goal;
neither is considered complete without automated cross-platform fixtures and
documented acceptance evidence.

## Windows CSV Viewer alignment

The Windows CSV Viewer should be advanced in its dedicated Windows task, where
its existing code, packaging and UI history are available. That task should use
this roadmap as its contract and return the following artifacts for integration:

1. the current Windows project and version inventory;
2. a field-by-field comparison with Linux CSV and PCM002Z exports;
3. shared golden fixtures and expected validation errors;
4. a proposal for displaying schema version, drive identity and unsupported
   parameters without data loss;
5. a proposal for displaying and round-tripping versioned Condition Monitoring
   Milestones without losing rule or event evidence;
6. automated Windows round-trip test results.

Linux Master remains the authority for guarded device communication. The Windows
Viewer remains an offline inspection and preparation tool unless a later release
explicitly defines and verifies a different responsibility.

## Subsequent candidates

After both declared 1.4 objectives are accepted, candidates may include richer
offline comparison reports, signed service packages and additional analytics.
They remain secondary to the parameter interchange and milestone contracts.

## GitHub release gate for 1.3.0

- Complete version consistency and automated regression checks.
- Verify installation and upgrade on a clean supported Raspberry Pi OS image.
- Repeat the 24-hour transparent-proxy test on the release archive.
- Verify database archive/delete/reinitialization and digital baseline creation.
- Select and add an explicit repository license; no license is assumed by this
  roadmap.
- Review bundled third-party PDF redistribution notices and Python dependencies.
- Publish SHA-256, release notes, supported hardware, rollback procedure and known
  limitations with the GitHub release.
