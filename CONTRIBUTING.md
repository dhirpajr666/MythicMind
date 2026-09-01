# Contributing to MythicMind

Thanks for considering a contribution. MythicMind is two independent lenses — a
stdlib-only Python evaluation harness under `pylab/` and a deterministic .NET 9
encounter runtime under `runtime/` — that meet only through JSON on disk.

## Development setup

- **Python 3.10+** for the evaluation lens. There is nothing to install; the
  package uses the standard library only.

```bash
cd pylab
python -m compileall mythicmind
python -m mythicmind batch ../examples/fixtures
python -m mythicmind explain ../examples/fixtures/gatekeeper-oath.json
```

- **.NET SDK 9.0** for the runtime lens.

```bash
dotnet build -c Release runtime/MythicMind.Runtime.csproj
dotnet run -c Release --project runtime -- replay-check examples/encounters/the-night-gate.json
```

## Before you open a pull request

1. `python -m compileall mythicmind` must pass and the CLI must run against the
   example fixtures (both from `pylab/`).
2. `dotnet build -c Release runtime/MythicMind.Runtime.csproj` must succeed if
   `runtime/` was touched, and both example encounters must pass `replay-check`.
3. Every new scoring rule needs a written rationale in the reason list and a
   fixture that demonstrates it.
4. Keep the Python lens dependency-free; the zero-dependency rule is part of
   the design contract.

## Pull requests

- One topic per PR, conventional commit titles (`feat:`, `fix:`, `docs:`...).
- Describe the motivation, not just the diff.
- By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
