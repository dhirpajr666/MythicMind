# Changelog

All notable changes to MythicMind are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/), and the project follows
semantic versioning since `1.0.0`.

## [Unreleased]

### Planned

- Streaming evaluation for large transcript batches (see ROADMAP).

## [1.0.0] — 2026-05-26

The first stable release. The two-lens contract is frozen: the Python CLI
verbs, the fixture schema, and the runtime transcript format are now treated
as stable interfaces.

### Added
- `replay-check` on both example encounters, wired into CI so every push
  proves byte-identical replay on a clean runner.
- Documentation pass: `docs/architecture.md` and `docs/scoring.md` brought in
  line with the frozen interfaces.

### Changed
- The runtime transcript format is documented and versioned alongside the
  fixture schema.

## [0.9.0] — 2025-06-17

### Added
- Example encounters (`examples/encounters/`) and fixtures
  (`examples/fixtures/`) covering a gate, a market and an oracle.
- `Makefile` and `scripts/run_all.{sh,ps1}` convenience targets for both
  lenses.

### Changed
- `Npc` memory was bounded to a 16-entry ring buffer so long encounters stay
  small and replayable.

## [0.8.0] — 2024-05-21

### Added
- `DeterministicRng` (SplitMix64) replacing `System.Random`, removing the
  last cross-runtime reproducibility risk.
- `run` and `replay-check` console verbs in the C# runtime.

### Changed
- Goal selection now breaks priority ties by goal name for stable replay.

## [0.7.0] — 2023-04-18

### Added
- The C# `Simulator`: a tick loop that selects goals, mutates world flags and
  records every utterance into an `EncounterTranscript`.
- `WorldState` snapshots with stable ordering for serialisation.

### Fixed
- Flag preconditions are evaluated against a frozen view of the world at the
  start of each tick, so goal order cannot leak state mid-tick.
