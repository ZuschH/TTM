# TMM CSV Viewer 1.1.1

Windows CSV Viewer 1.1.1 aligns offline CSV analysis with the TMM Linux Master
1.3.0 export contract and prepares the 24-hour field-acceptance test.

## Highlights

- Reads UTF-8 CSV with or without BOM, comma/semicolon/tab delimiters, quoted
  fields and embedded line breaks.
- Accepts both Windows and Linux line endings as well as decimal-comma values
  from technician-edited Windows files.
- Preserves unknown columns and future measurement channels during normalized
  re-export; unfamiliar channels are visibly labelled instead of discarded.
- Adds **Export normalized CSV** for an auditable offline inspection round trip.
- Covers inverter readings, digital signals, external analog values,
  communication data and thermal-protection records.

## Verification

- Automated import → viewer data model → normalized export → re-import tests
  pass for Master-shaped and Windows-localized Golden Files.
- The generated 24-hour fixture with 86,400 rows parsed successfully in
  1,176 ms in the development environment.
- Full evidence and the target-hardware field test are documented in
  `TEST-RESULTS-2026-11-21.md` and `BUILD-24H-TEST.md`.

## Known limitation

TMM Linux Master 1.3 stores Condition Monitoring milestones but does not yet
include them in `/api/v1/export.csv`. Viewer 1.1.1 preserves compatible custom
or future rows but cannot display an event stream that the Master does not
export. Versioned milestone support is a defined TMM 1.4 objective.

## Artifact

`tmm-csv-viewer-windows-1.1.1-24h-test-source-r2.zip`

SHA-256:

```text
9a40114adf30108d687741b1551b78c9d05dd16c0d19d0abf416a6da4fa97f14
```
