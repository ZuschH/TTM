# TMM Windows installer build

This directory contains the reproducible Inno Setup build for the offline
`TMM-Setup-1.0.0.exe` package.

## Layout

```text
installer/
  TMM.iss                 Inno Setup definition
  build-installer.ps1     validated build entry point
  staging/
    app/                   staged TMM application files
    runtime/               private 64-bit Python runtime and installed wheels
  output/                  generated setup executable
```

`staging` and `output` are generated build directories. They are deliberately
separate from the source tree and must not contain configuration, databases, or
logs from a development installation.

## Build prerequisites

- Windows 10 or Windows 11, x64 compatible
- Inno Setup 7
- PowerShell 5.1 or newer
- Official CPython 3.14.7 x64 on the build computer

Prepare the clean private runtime and offline wheel cache with:

```powershell
.\installer\prepare-runtime.ps1
```

The script uses the Python launcher when it is available. On a build host where
the launcher is intentionally absent, it also looks for the standard Python
3.14 locations and for an existing TMM private runtime. A specific verified
Python executable can always be selected explicitly:

```powershell
.\installer\prepare-runtime.ps1 -PythonExe 'C:\Program Files\TMM\runtime\python.exe'
```

The selected executable must still be exactly the required x64 Python version;
the script verifies that before it copies any runtime files.

If the build host has no internet or cannot reach the package index, reuse the
already working private TMM runtime without downloading wheels:

```powershell
.\installer\prepare-runtime.ps1 -PythonExe 'C:\Program Files\TMM\runtime\python.exe' -ReuseInstalledPackages
```

Offline mode copies that runtime's installed packages, verifies each pinned
version from `requirements.txt`, and runs the same private-runtime import test.
It is therefore suitable only when the selected TMM installation is known to be
working and uses the expected release runtime.

The script verifies the exact Python version and architecture, excludes packages
installed globally on the build computer, downloads only binary wheels, installs
them into the staged runtime, verifies Tkinter and every TMM dependency, and
writes a hash manifest. No compiler or Python installation is needed on target
computers.

Stage and validate only the approved application files with:

```powershell
.\installer\prepare-app.ps1
```

This step deliberately excludes tests, development artwork, databases, logs,
existing configuration, old packages, and build scripts. It compiles every
Python module using the private runtime, validates the example JSON, checks the
required web/tray assets, and writes a per-file SHA-256 manifest.

After both staging steps have completed, build with:

```powershell
.\installer\build-installer.ps1
```

The resulting self-contained setup is written to:

```text
installer\output\TMM-Setup-1.0.0.exe
```

`build-installer.ps1` prints its SHA-256 checksum. Keep that value with the
release file so the copied setup executable can be verified on another host:

```powershell
Get-FileHash .\installer\output\TMM-Setup-1.0.0.exe -Algorithm SHA256
```

## Release sequence

Use a clean copy of the source tree and run the three commands in this exact
order from its root directory in an elevated PowerShell window:

```powershell
.\installer\prepare-runtime.ps1
.\installer\prepare-app.ps1
.\installer\build-installer.ps1
```

The first command downloads the pinned binary dependency wheels and is therefore
the only step requiring internet access. The staged private runtime, staged
application manifest, and final setup executable can then be retained for
offline deployment. The installer preserves existing `%ProgramData%\TMM`
configuration and recordings during an upgrade.

## Uninstallation and recorded data

The uninstaller retains configuration, recordings, archives and logs by
default. At its start it explicitly asks whether all TMM data should be removed.
Choosing **Yes** removes `%ProgramData%\TMM` and, when configured elsewhere,
the exact SQLite database file together with its WAL/SHM sidecars. Silent
uninstallations always retain recorded data.
