"""Command-line interface for the mythicmind evaluation lab.

    python -m mythicmind eval <fixture.json> [--json]
    python -m mythicmind batch <dir-or-files...> [--json] [--threshold 0.6]
    python -m mythicmind explain <fixture.json>

`eval`    scores a single fixture.
`batch`   scores many fixtures and prints an aggregate report.
`explain` prints every axis reason for a single fixture (full transparency).

Stdlib only — no third-party dependencies.
