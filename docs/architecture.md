# Architecture

MythicMind is two independent programs that share a philosophy and a data
directory. This document describes how each is built and where the seams are.

## Overview

```
          PRODUCES behaviour                 JUDGES behaviour
        ┌────────────────────┐            ┌────────────────────┐
        │   C# .NET 9 lens    │  JSON      │    Python lens      │
        │   runtime/          │  transcript│    pylab/           │
        │                     │───────────▶│                     │
        │  World → Goals →    │            │  Fixtures → Axes →  │
        │  Memory → Replay    │            │  Reasons → Report   │
        └────────────────────┘            └────────────────────┘
                  ▲                                   ▲
                  │ encounters/*.json                 │ fixtures/*.json
                  └───────────────────────────────────┘
                              examples/
```

The two lenses do not import each other. They meet only through JSON on disk.
This keeps each side simple and independently testable, and lets a team adopt
just one lens if that is all they need.

## The Python lens (`pylab/mythicmind/`)

| Module        | Responsibility                                                        |
|---------------|-----------------------------------------------------------------------|
| `model.py`    | Frozen dataclasses for `Persona`, `Scenario`, `DialogueTurn`, `Fixture`; JSON loading and validation. |
| `scoring.py`  | The four axis heuristics. Each returns an `AxisScore` carrying value **and** reasons. `evaluate_fixture` combines them with explicit weights. |
| `report.py`   | `BatchReport`: axis means, threshold flagging, and text/JSON rendering. |
| `cli.py`      | `argparse`-based CLI with `eval`, `explain`, `batch` subcommands.      |
| `__main__.py` | Enables `python -m mythicmind`.                                        |

**Key property:** zero third-party dependencies. Everything is Python stdlib,
so the lens runs anywhere Python ≥ 3.10 does, with nothing to install.

### Data flow

