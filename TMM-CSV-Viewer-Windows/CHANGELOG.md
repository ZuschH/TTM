# Changelog

## 1.1.1 — 2026-11-21

- Aligns the offline importer with the TMM Linux Master 1.3.0 CSV contract.
- Accepts UTF-8 with or without BOM, comma/semicolon/tab delimiters, quoted
  fields, embedded line breaks, Windows and Linux line endings, and decimal
  commas used by technician-edited Windows files.
- Preserves unknown columns and future measurement channels verbatim and marks
  unfamiliar imported channels instead of silently dropping them.
- Adds normalized UTF-8 CSV export and automated import → display-model →
  export round-trip tests, including a generated 24-hour, 86,400-row fixture.

## 1.1.0 — 2026-09-23

- Aligns offline analysis with the TMM 1.1 history workflow.
- Adds safe bounded-spline curves alongside hold-last-value and linear modes.
- Adds temporary click-to-add analysis markers with visible snapshot tables and
  individual deletion controls.
- Keeps separate digital logic-analyzer lanes and per-unit chart scales for
  clear comparison of differently scaled measurements.
