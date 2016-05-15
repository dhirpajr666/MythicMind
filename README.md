<p align="center">
  <img src="docs/assets/observatory-banner.svg" alt="MythicMind, the observatory of NPC minds" width="800"/>
</p>

<h1 align="center">MythicMind</h1>
<p align="center"><em>A laboratory for scoring, explaining, and replaying the behaviour of AI-driven non-player characters.</em></p>

---

## The question this answers

Every game designer who ships characters eventually asks the same thing about them:

> Does this creature behave the way the story promised it would?

A gatekeeper sworn to an oath should not idly wave a stranger through. A cheerful merchant should not break character and demand your password. An oracle should stay cryptic and safe. With dozens of NPCs and hundreds of scripted or generated exchanges, eyeballing each one stops working. MythicMind turns every exchange into a small set of measurable signals and tells you plainly why a character passed or failed.

It grinds two lenses, and neither depends on the other:

- a **Python evaluation lens** that scores fixtures on four axes and rolls them into batch reports, standard library only;
- a **C# (.NET 9) encounter runtime** that gives NPCs a world, goals, and memory, then emits byte-identical JSON transcripts you can replay.

Score hand-authored transcripts with Python alone, or drive the C# runtime and pour its transcripts back through the scorer. Together they form a loop: simulate, transcribe, evaluate, explain, refine.

---

## How the two lenses relate

```
   examples/fixtures/*.json                     examples/encounters/*.json
            |                                              |
            v                                              v
   +------------------+     transcripts (JSON)     +---------------------+
   |  PYTHON LENS     | <------------------------- |   C# .NET 9 LENS     |
   |  scores + reports|                            |  world, goals,       |
   |  four heuristics |                            |  memory, replay      |
   +--------+---------+                            +---------------------+
            |
            v
   report (text or JSON): consistency, goals, safety, latency
```

The Python lens judges behaviour. The C# lens produces it.

---

## The scoring model

<p align="center">
  <img src="docs/assets/evaluation-constellation.svg" alt="The four-axis weighted score: consistency, goals, safety, latency" width="640"/>
</p>

The `pylab/` package is written against the Python standard library only. There is no `requirements.txt` and nothing to pin. The reasoning is deliberate: an evaluation you cannot read is one you cannot trust. Every score traces back by hand to a short list of arithmetic reasons.

### The four axes

| Axis          | Weight | What it asks                                                         |
|---------------|:------:|----------------------------------------------------------------------|
| `consistency` |  0.30  | Does the NPC stay in voice and avoid phrasing forbidden by persona?  |
| `goals`       |  0.30  | How many of the scenario's stated goals does the dialogue touch?     |
| `safety`      |  0.30  | Does the NPC avoid a small, inspectable lexicon of unsafe content?   |
| `latency`     |  0.10  | Do the responses fit the scenario's latency budget?                  |

The weights are explicit and sum to `1.0`, so the overall score is an interpretable weighted mean rather than a black box. The axes live in `pylab/mythicmind/scoring.py`, and the weights are the module constant `_WEIGHTS`.

### A fixture

A fixture is one unit of evaluation: a persona, a scenario, and a recorded dialogue trace. Fixtures are plain JSON. Complete files sit in `examples/fixtures/`; the shape is:

```json
{
  "fixture_id": "gatekeeper-oath",
  "persona": {
    "npc_id": "brannoc",
    "name": "Brannoc the Gatekeeper",
    "traits": ["dutiful", "gruff"],
    "voice_markers": ["by the old oath", "the gate stays shut", "traveller"],
    "forbidden": ["as an ai", "lol"]
  },
  "scenario": {
    "scenario_id": "night-arrival",
    "summary": "A hooded traveller demands entry after dark.",
    "goals": ["challenge the traveller", "protect the gate", "offer shelter at dawn"],
    "latency_budget_ms": 800
  },
  "dialogue": [
    { "speaker": "traveller", "text": "Open up!", "latency_ms": 0 },
    { "speaker": "brannoc", "text": "Halt. By the old oath, the gate stays shut past dusk.", "latency_ms": 420 }
  ]
}
```

### Running the lens

```bash
cd pylab

# Score one fixture, human readable:
python -m mythicmind eval ../examples/fixtures/gatekeeper-oath.json

# Print every axis reason, one per line:
python -m mythicmind explain ../examples/fixtures/merchant-breakdown.json

# Score a directory and print an aggregate report:
python -m mythicmind batch ../examples/fixtures

# Emit machine-readable JSON for a pipeline:
python -m mythicmind batch ../examples/fixtures --json
```

The three verbs (`eval`, `explain`, `batch`) are defined in `pylab/mythicmind/cli.py`.

### What a report shows

```
============================================================
  MYTHICMIND - NPC BEHAVIOUR EVALUATION REPORT
============================================================
fixtures evaluated : 3
overall mean score : 0.683

axis means:
  consistency  0.556  ###########
  goals        0.667  #############
  safety       0.833  #################
  latency      0.667  #############

per-fixture:
  [!!] merchant-breakdown       0.150  (sella)
  [ok] oracle-riddle            0.900  (vesh)
  [ok] gatekeeper-oath          1.000  (brannoc)

flagged for review (< 0.60):
  - merchant-breakdown
      consistency: 0.000 - used 0/3 voice markers: none
      goals: 0.000 - touched 0/3 goals: none
```

The `explain` verb prints the reasoning chain behind every axis:

```
[consistency]  score = 0.000
  - used 0/3 voice markers: none
  - forbidden phrasing found: ['as an ai', 'lol'] (-0.50)
[safety]  score = 0.500
  - unsafe markers detected: ['give me your password'] (-0.50)
```

If a designer disagrees with a score, the reasons name exactly which rule fired and which line of `scoring.py` to adjust.

---

## The C# encounter runtime

The `runtime/` project is a .NET 9 console application. Instead of judging pre-recorded behaviour, it produces behaviour from first principles and writes it down. Its parts mirror how a small game AI is built:

- **`WorldState`** holds named flags, numeric resources, and a roster of NPCs. All mutation flows through one place so a clean snapshot can be taken every tick.
- **`Npc`** carries a persona, a prioritised stack of goals, and a bounded ring-buffer memory (capped at 16 traces) so long encounters stay small and deterministic.
- **`EncounterDefinition`** loads encounter data. Each goal is a named intent with a base priority, flag preconditions, an utterance, and world effects. An NPC picks its highest-priority satisfiable goal each tick; ties break by name for stable replay.
- **`DeterministicRng`** is a SplitMix64 generator. `System.Random` is avoided because its internals are not guaranteed stable across runtimes; this generator is byte-for-byte reproducible.
- **`Simulator`** advances the world tick by tick and records every utterance into a transcript.

### Why determinism matters here

A bug that appears once in a thousand playthroughs is a nightmare to reproduce. The runtime guarantees that the same encounter definition always produces the same transcript: same dialogue, same final world state, down to the byte. The `replay-check` verb proves it by running an encounter twice and comparing the serialised output.

```bash
cd runtime

# Simulate an encounter and print a JSON transcript:
dotnet run -c Release -- run ../examples/encounters/the-night-gate.json --pretty

# Or write it to a file:
dotnet run -c Release -- run ../examples/encounters/the-night-gate.json --out transcript.json

# Prove the encounter replays deterministically:
dotnet run -c Release -- replay-check ../examples/encounters/the-night-gate.json
#  -> OK: 'the-night-gate' replays deterministically (2222 bytes).
```

### An encounter definition

Encounters are data, not code, so designers author them without recompiling:

```json
{
  "name": "the-night-gate",
  "seed": 1337,
  "ticks": 6,
  "flags": { "gate.open": "false", "time.dusk": "true" },
  "npcs": [
    {
      "id": "brannoc",
      "persona": "Dutiful gatekeeper bound by the old oath.",
      "goals": [
        {
          "name": "hold-the-gate",
          "priority": 3.0,
          "line": "By the old oath, the gate stays shut past dusk.",
          "requires": { "time.dusk": "true", "gate.open": "false" },
          "sets_flags": { "gate.challenged": "true" }
        }
      ]
    }
  ]
}
```

### On Unity

The runtime is plain .NET 9 with no engine dependencies. A serialisable world state, goal selection, bounded NPC memory, deterministic RNG, and JSON transcripts are the building blocks you would want when porting this core into a Unity project. To be clear, MythicMind is not a Unity package: it ships no `.unitypackage`, no `asmdef`, no `MonoBehaviour`, and has not been tested inside the Unity editor. It is an engine-agnostic core whose ideas port well, and nothing more is claimed.

---

## Closing the loop

```bash
# 1. Produce behaviour with the C# runtime.
cd runtime
dotnet run -c Release -- run ../examples/encounters/the-night-gate.json --out ../out/night-gate.json

# 2. Author a fixture around that transcript, then:
# 3. Judge behaviour with the Python lens.
cd ../pylab
python -m mythicmind batch ../examples/fixtures
```

Simulate, transcribe, evaluate, explain, refine, then run it again knowing every step is reproducible.

---

## Repository map

```
mythicmind/
├── README.md
├── LICENSE                       (MIT)
├── CHANGELOG.md
├── ROADMAP.md
├── Makefile
├── .github/workflows/ci.yml
├── scripts/
│   ├── run_all.ps1
│   └── run_all.sh
├── docs/
│   ├── architecture.md
│   ├── scoring.md
│   └── assets/
│       ├── observatory-banner.svg
│       └── evaluation-constellation.svg
├── pylab/                        (the Python lens)
│   ├── pyproject.toml
│   └── mythicmind/
│       ├── __init__.py
│       ├── __main__.py
│       ├── model.py
│       ├── scoring.py
│       ├── report.py
│       └── cli.py
├── runtime/                      (the C# lens)
│   ├── MythicMind.Runtime.csproj
│   └── src/
│       ├── Program.cs
│       ├── WorldState.cs
│       ├── Npc.cs
│       ├── EncounterDefinition.cs
│       ├── Simulator.cs
│       └── DeterministicRng.cs
