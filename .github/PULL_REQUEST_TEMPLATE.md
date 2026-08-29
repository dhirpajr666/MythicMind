## What this changes

## Why

## Checklist

- [ ] `python -m compileall mythicmind` passes (from `pylab/`)
- [ ] `python -m mythicmind batch ../examples/fixtures` runs
- [ ] `dotnet build -c Release runtime/MythicMind.Runtime.csproj` passes and both
      example encounters pass `replay-check` (if `runtime/` was touched)
- [ ] New scoring behavior ships with a fixture that demonstrates it
