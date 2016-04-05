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

