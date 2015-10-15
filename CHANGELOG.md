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
