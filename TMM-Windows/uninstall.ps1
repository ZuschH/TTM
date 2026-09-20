[CmdletBinding()]
param(
    [switch]$RemoveData
)

$ErrorActionPreference = "Stop"
$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    throw "Run this uninstaller from an elevated PowerShell window (Run as administrator)."
}

$programDir = Join-Path $env:ProgramFiles "TMM"
$python = Join-Path $programDir ".venv\Scripts\python.exe"
$serviceScript = Join-Path $programDir "tmm_service.py"

Stop-Service -Name "TMM" -Force -ErrorAction SilentlyContinue
Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
    Where-Object {$_.CommandLine -match [regex]::Escape((Join-Path $programDir "tmm_tray.pyw"))} |
    ForEach-Object {Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue}
$trayShortcut = Join-Path ([Environment]::GetFolderPath("Startup")) "Toshiba Modbus Monitor.lnk"
Remove-Item -LiteralPath $trayShortcut -Force -ErrorAction SilentlyContinue
if ((Test-Path $python) -and (Test-Path $serviceScript)) {
    & $python $serviceScript remove
} elseif (Get-Service -Name "TMM" -ErrorAction SilentlyContinue) {
    sc.exe delete TMM | Out-Null
}

Get-NetFirewallRule -DisplayName "Toshiba Modbus Monitor Web" -ErrorAction SilentlyContinue | Remove-NetFirewallRule
if (Test-Path $programDir) {
    Rename-Item $programDir ((Split-Path $programDir -Leaf) + ".remove") -ErrorAction SilentlyContinue
    Write-Host "Program files are marked for removal. Delete '$programDir.remove' after this window closes."
}
if ($RemoveData) {
    Remove-Item -Recurse -Force (Join-Path $env:ProgramData "TMM")
} else {
    Write-Host "Configuration and database retained in $env:ProgramData\TMM"
}
