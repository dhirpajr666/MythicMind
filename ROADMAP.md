# MythicMind roadmap

Only implemented foundation work is checked.

## Completed foundation
- [x] **M1 — Two-lens architecture.** Independent Python evaluation lens and deterministic .NET runtime.
- [x] **M2 — Explainable scorer.** Consistency, goals, safety, and latency axes with readable reasons.
- [x] **M3 — Encounter runtime.** World state, NPC goals, bounded memory, seeded replay, and JSON transcripts.
- [x] **M4 — Examples and automation.** Fixtures, encounters, documentation, scripts, and dual-language CI.

## Planned
- [ ] Automated pytest and xUnit suites.
- [ ] Optional axis weights loaded from a `weights.json` beside a fixture set.
- [ ] Streaming evaluation for large transcript batches.
- [ ] Lore-grounding and turn-coherence axes.
- [ ] Automatic transcript-to-fixture conversion.
- [ ] Multi-step NPC goal planning.
- [ ] Unity adaptation guide (the current runtime is engine-agnostic, not a Unity package).
