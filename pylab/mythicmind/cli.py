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


def _cmd_batch(args: argparse.Namespace) -> int:
    files = _collect_fixtures(args.paths)
    if not files:
        print("error: no fixtures found", file=sys.stderr)
        return 1
    results = [evaluate_fixture(Fixture.load(f)) for f in files]
    report = BatchReport(results)
    if args.json:
        print(json.dumps(report.as_dict(), indent=2))
    else:
        print(report.to_text(threshold=args.threshold))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mythicmind",
        description="Explainable AI NPC behaviour evaluation lab (stdlib only).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_eval = sub.add_parser("eval", help="score a single fixture")
    p_eval.add_argument("fixture", help="path to a fixture JSON file")
    p_eval.add_argument("--json", action="store_true", help="emit JSON")
    p_eval.set_defaults(func=_cmd_eval)

    p_explain = sub.add_parser("explain", help="show all axis reasons for a fixture")
    p_explain.add_argument("fixture", help="path to a fixture JSON file")
    p_explain.set_defaults(func=_cmd_explain)

    p_batch = sub.add_parser("batch", help="score many fixtures and aggregate")
    p_batch.add_argument("paths", nargs="+", help="fixture files or directories")
    p_batch.add_argument("--json", action="store_true", help="emit JSON")
    p_batch.add_argument("--threshold", type=float, default=0.6,
                         help="review threshold for flagging (default 0.6)")
    p_batch.set_defaults(func=_cmd_batch)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

# draft note 1429
