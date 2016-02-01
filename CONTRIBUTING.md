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

