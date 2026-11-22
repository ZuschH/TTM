# TMM Linux Master 1.3 release policy

## Feature freeze

TMM Linux Master 1.3 is feature-frozen at release baseline r133. Version 1.3.0
is the first public release from that baseline. No new hardware source, protocol
mode, dashboard function, data model or parameter operation is added to the 1.3
line.

## Allowed changes

Every later change to the 1.3 line is classified and published as a **Bugfix**.
Allowed work is limited to:

- correcting behavior that contradicts the 1.3 documentation or verified
  release behavior;
- reliability, security and compatibility fixes that preserve existing
  interfaces;
- corrections to translations, installation, documentation and diagnostics;
- tests that reproduce a defect and prevent its recurrence.

If a proposed change requires a new configuration field, API contract, hardware
capability, workflow or database meaning, it belongs to a later feature version
unless it is strictly necessary for a safe, backward-compatible defect repair.

## Versioning and changelog

- Bugfix releases increment the patch number: 1.3.1, 1.3.2, and so on.
- Each changelog section begins with `Bugfix 1.3.x` and describes the observed
  defect, its correction and its verification.
- The `VERSION` file is the authoritative runtime version. API metadata,
  dashboard footer, release archive and offline-bundle manifest must agree with
  it.
- A bugfix is not released until the complete automated test suite passes and
  its affected hardware or workflow has a documented verification result.

## Compatibility promise

Bugfixes preserve existing 1.3 configuration files, SQLite recordings, REST
responses and CSV exports. Any unavoidable incompatibility must stop the release
until an explicit migration and rollback procedure exists.
