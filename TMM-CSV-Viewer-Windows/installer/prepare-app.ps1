[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$installerDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Split-Path -Parent $installerDir
$appDir = Join-Path $installerDir "staging\app"
$candidate = Join-Path $installerDir ("staging\app.build-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $candidate | Out-Null
foreach ($file in @("tmm_csv_viewer.pyw", "README.md", "CHANGELOG.md")) {
    $source = Join-Path $projectDir $file
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw "Required viewer file missing: $source" }
    Copy-Item -LiteralPath $source -Destination (Join-Path $candidate $file)
}
Copy-Item -LiteralPath (Join-Path $projectDir "static") -Destination (Join-Path $candidate "static") -Recurse
$runtimePython = Join-Path $installerDir "staging\runtime\python.exe"
if (-not (Test-Path -LiteralPath $runtimePython -PathType Leaf)) { throw "Runtime staging missing. Run prepare-runtime.ps1 first." }
& $runtimePython -m py_compile (Join-Path $candidate "tmm_csv_viewer.pyw")
if ($LASTEXITCODE -ne 0) { throw "Viewer launcher failed compilation." }
Get-ChildItem -LiteralPath $candidate -Directory -Filter "__pycache__" -Recurse | Remove-Item -Recurse -Force
$files = @(Get-ChildItem -LiteralPath $candidate -File -Recurse | Sort-Object FullName | ForEach-Object {
    [ordered]@{path=$_.FullName.Substring($candidate.Length + 1).Replace("\", "/"); size=$_.Length; sha256=(Get-FileHash -Algorithm SHA256 $_.FullName).Hash.ToLowerInvariant()}
})
([ordered]@{product="TMM CSV Viewer"; version="1.1.1"; files=$files} | ConvertTo-Json -Depth 4) | Set-Content -Encoding UTF8 (Join-Path $candidate "VIEWER-APP-MANIFEST.json")
if (Test-Path $appDir) { Move-Item -LiteralPath $appDir -Destination (Join-Path $installerDir ("staging\app.previous-" + (Get-Date -Format "yyyyMMdd-HHmmss"))) }
Move-Item -LiteralPath $candidate -Destination $appDir
Write-Host "Viewer application prepared: $appDir"
