#!/usr/bin/env bash
# Run both MythicMind lenses end to end (POSIX shells).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== Python lens: batch evaluation =="
( cd pylab && python -m mythicmind batch ../examples/fixtures )

echo
echo "== C# lens: build =="
