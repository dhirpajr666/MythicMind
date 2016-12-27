"""Command-line interface for the mythicmind evaluation lab.

    python -m mythicmind eval <fixture.json> [--json]
    python -m mythicmind batch <dir-or-files...> [--json] [--threshold 0.6]
    python -m mythicmind explain <fixture.json>

`eval`    scores a single fixture.
`batch`   scores many fixtures and prints an aggregate report.
`explain` prints every axis reason for a single fixture (full transparency).

Stdlib only — no third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .model import Fixture
from .report import BatchReport
from .scoring import evaluate_fixture


def _collect_fixtures(paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            out.extend(sorted(path.glob("*.json")))
        elif path.is_file():
            out.append(path)
        else:
            print(f"warning: skipping missing path {p}", file=sys.stderr)
    return out


def _cmd_eval(args: argparse.Namespace) -> int:
    fx = Fixture.load(args.fixture)
    result = evaluate_fixture(fx)
    if args.json:
        print(json.dumps(result.as_dict(), indent=2))
    else:
        print(f"{fx.fixture_id}: overall {result.overall:.3f}")
        for a in result.axes:
            print(f"  {a.name:<12} {a.value:.3f}")
    return 0


def _cmd_explain(args: argparse.Namespace) -> int:
    fx = Fixture.load(args.fixture)
    result = evaluate_fixture(fx)
    print(f"fixture: {fx.fixture_id}  (npc={fx.persona.npc_id})")
    print(f"overall: {result.overall:.3f}")
    for a in result.axes:
        print(f"\n[{a.name}]  score = {a.value:.3f}")
        for reason in a.reasons:
            print(f"  - {reason}")
    return 0
