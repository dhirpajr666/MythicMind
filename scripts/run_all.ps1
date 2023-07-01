# Run both MythicMind lenses end to end (Windows PowerShell).
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Host "== Python lens: batch evaluation ==" -ForegroundColor Cyan
Push-Location pylab
python -m mythicmind batch ..\examples\fixtures
Pop-Location

Write-Host "`n== C# lens: build ==" -ForegroundColor Cyan
dotnet build -c Release runtime\MythicMind.Runtime.csproj

Write-Host "`n== C# lens: deterministic replay check ==" -ForegroundColor Cyan
dotnet run -c Release --project runtime -- replay-check examples\encounters\the-night-gate.json
dotnet run -c Release --project runtime -- replay-check examples\encounters\market-haggle.json

Write-Host "`nAll lenses ran successfully." -ForegroundColor Green
