#!/usr/bin/env bash
# Run both MythicMind lenses end to end (POSIX shells).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== Python lens: batch evaluation =="
( cd pylab && python -m mythicmind batch ../examples/fixtures )

echo
echo "== C# lens: build =="
dotnet build -c Release runtime/MythicMind.Runtime.csproj

echo
echo "== C# lens: deterministic replay check =="
dotnet run -c Release --project runtime -- replay-check examples/encounters/the-night-gate.json
dotnet run -c Release --project runtime -- replay-check examples/encounters/market-haggle.json

echo
echo "All lenses ran successfully."
