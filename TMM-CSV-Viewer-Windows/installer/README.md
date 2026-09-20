# TMM CSV Viewer Windows installer

The viewer installer is self-contained and does not install a Windows service.
It includes a private 64-bit Python runtime because the viewer starts a local
loopback web server for its offline browser interface.

Build from an elevated PowerShell window on a Windows x64 host with Inno Setup
7 installed:

```powershell
.\installer\prepare-runtime.ps1 -PythonExe 'C:\Program Files\TMM\runtime\python.exe'
.\installer\prepare-app.ps1
.\installer\build-installer.ps1
```

`prepare-runtime.ps1` can also use any other working 64-bit Python executable.
The viewer has no third-party Python dependencies. The generated setup is
`installer\output\TMM-CSV-Viewer-Setup-1.0.0.exe`.
