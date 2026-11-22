# Windows CSV Viewer 1.1.1 — 24-hour acceptance package

## Scope

This package is the Windows-offline companion for TMM Linux Master 1.3.0. It
does not alter the Linux Master or its REST/CSV interfaces.

## Automated evidence

Run from the project directory:

```text
node tests/test_csv_codec.js
node --check static/csv-codec.js
node --check static/app.js
python tmm_csv_viewer.pyw --no-browser --port 8090
```

The codec acceptance test covers import → viewer data model → normalized export
round trips. It includes the Golden Files in `tests/golden/` and generates a
24-hour 86,400-row recording at runtime, keeping the repository compact.

## Field-test procedure

1. Export a full CSV from a Linux Master 1.3.0 RC1 system after at least 24
   hours.
2. Open it with Viewer 1.1.1. Confirm the displayed sample count, period and
   investigation reference.
3. Inspect a digital lane, an external analog channel, communication data and
   `system.thermal_protection` where present.
4. Use **Export normalized CSV**, reopen the resulting file and compare the
   summary and selected channels.
5. Retain the original and normalized CSV with the test record.

## Known limitations

- The Master currently does not put condition-monitoring milestones into its
  normal CSV export. The Viewer cannot render a stream that is not exported;
  it preserves compatible future/custom rows instead.
- The Viewer performs parsing locally in the browser. The included acceptance
  fixture proves 24-hour import parsing, but final responsiveness must still be
  verified on the target Windows hardware with the actual export size.
- This source package is build-ready. Producing the signed Inno Setup `.exe`
  requires the Windows build host, private Python runtime staging and Inno
  Setup 7 as documented in `installer/README.md`.
