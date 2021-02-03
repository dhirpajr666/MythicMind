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

```
fixture.json → Fixture.load → evaluate_fixture
                                   ├─ score_consistency → AxisScore(+reasons)
                                   ├─ score_goals       → AxisScore(+reasons)
                                   ├─ score_safety      → AxisScore(+reasons)
                                   └─ score_latency     → AxisScore(+reasons)
                                        ↓ weighted mean
                                   EvaluationResult → BatchReport → text/JSON
```

## The C# lens (`runtime/src/`)

| File                     | Responsibility                                                        |
|--------------------------|-----------------------------------------------------------------------|
| `DeterministicRng.cs`    | SplitMix64 PRNG; stable across platforms (unlike `System.Random`).    |
| `WorldState.cs`          | Flags, resources, NPC roster, and ordered `Snapshot()` for serialisation. |
| `Npc.cs`                 | Persona, prioritised `Goal` list, bounded ring-buffer memory, goal selection. |
| `EncounterDefinition.cs` | JSON schema for encounters + `ToWorld()` materialisation.             |
| `Simulator.cs`           | Tick loop; produces an `EncounterTranscript`.                         |
| `Program.cs`             | Console entrypoint; `run` and `replay-check` verbs.                   |

### The tick loop

Each tick, for every NPC in stable id order:

1. Select the highest-priority goal whose flag preconditions are satisfied
   (ties broken by goal name → deterministic).
2. Apply the goal's `sets_flags` to the shared world.
3. Drift mood slightly toward warmth, with a *seeded* per-(npc, tick) jitter so
   personalities feel alive without breaking reproducibility.
4. Append a memory trace (oldest evicted past capacity 16).
