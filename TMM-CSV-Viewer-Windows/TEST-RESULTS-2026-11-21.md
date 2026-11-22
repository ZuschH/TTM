# CSV Viewer 1.1.1 verification result

Executed on 2026-11-21 in the development environment.

| Check | Result |
| --- | --- |
| `node tests/test_csv_codec.js` | Passed |
| Master 1.3-shaped Golden File, UTF-8 BOM, quoted commas/newlines | Passed |
| Windows semicolon + decimal-comma + CRLF Golden File | Passed |
| Import → viewer data model → normalized export → re-import | Passed |
| Digital, analog, communication, thermal, condition-shaped and unknown records | Passed |
| Generated 24-hour 86,400-row fixture | Passed in 1,176 ms |
| `node --check static/csv-codec.js` | Passed |
| `node --check static/app.js` | Passed |
| `python3 -m py_compile tmm_csv_viewer.pyw` | Passed |
| Release ZIP integrity (`unzip -t`) | Passed |

The local HTTP server cannot be bound inside this sandbox, so a full browser
click-through and an Inno Setup `.exe` build must be performed on the Windows
build/test host. This is an environment restriction, not an application error.
