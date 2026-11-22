# TMM Linux Master 1.3.0 RC3

This is the feature-frozen Linux Master 1.3 release candidate for the final
24-hour machine test. It is a prerelease, not the final 1.3.0 release.

## Validation

- 154 automated tests passed.
- Python modules, shell scripts and browser JavaScript passed syntax checks.
- The release archive was inspected to confirm that it contains no Sequent
  Microsystems PDF files.
- The optional documentation downloader retrieved all ten official files and
  verified their pinned SHA-256 checksums.

## Licensing and documentation

TMM is released under the MIT License. Sequent Microsystems manuals and
schematics are not redistributed and are not covered by that license. The UI
uses official publisher links unless verified local copies were installed.

## Scope

This release updates `TMM-Linux/` only. The Windows monitor and Windows CSV
Viewer retain their separately published versions pending their dedicated
alignment and 24-hour test.

Archive SHA-256:

`97d0102bb58d8474db08601b2740820bad99c3694d21fa23ff3b96a73cce268d`
