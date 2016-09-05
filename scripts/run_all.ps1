# Run both MythicMind lenses end to end (Windows PowerShell).
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Host "== Python lens: batch evaluation ==" -ForegroundColor Cyan
Push-Location pylab
python -m mythicmind batch ..\examples\fixtures
Pop-Location
