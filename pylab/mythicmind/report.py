"""Batch report generation.

Given a set of :class:`EvaluationResult` objects, produce both a machine
readable summary (dict / JSON) and a compact human-readable text report.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

from .scoring import EvaluationResult

_AXES = ("consistency", "goals", "safety", "latency")


@dataclass
class BatchReport:
    results: list[EvaluationResult]

    def axis_means(self) -> dict[str, float]:
        out: dict[str, float] = {}
        for axis in _AXES:
            vals = [
                a.value
                for r in self.results
                for a in r.axes
                if a.name == axis
            ]
            out[axis] = mean(vals) if vals else 0.0
        return out

    def overall_mean(self) -> float:
        return mean([r.overall for r in self.results]) if self.results else 0.0

    def flagged(self, threshold: float = 0.6) -> list[EvaluationResult]:
        """Fixtures whose overall score falls below a review threshold."""
        return [r for r in self.results if r.overall < threshold]

    def as_dict(self) -> dict:
        return {
            "count": len(self.results),
            "overall_mean": round(self.overall_mean(), 4),
            "axis_means": {k: round(v, 4) for k, v in self.axis_means().items()},
            "results": [r.as_dict() for r in self.results],
        }

    def to_text(self, threshold: float = 0.6) -> str:
        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("  MYTHICMIND - NPC BEHAVIOUR EVALUATION REPORT")
        lines.append("=" * 60)
        lines.append(f"fixtures evaluated : {len(self.results)}")
        lines.append(f"overall mean score : {self.overall_mean():.3f}")
        lines.append("")
        lines.append("axis means:")
        for k, v in self.axis_means().items():
            bar = "#" * int(round(v * 20))
            lines.append(f"  {k:<12} {v:5.3f}  {bar}")
        lines.append("")
        lines.append("per-fixture:")
        for r in sorted(self.results, key=lambda x: x.overall):
            mark = "!!" if r.overall < threshold else "ok"
            lines.append(f"  [{mark}] {r.fixture_id:<24} {r.overall:5.3f}  ({r.npc_id})")
        flagged = self.flagged(threshold)
        if flagged:
            lines.append("")
            lines.append(f"flagged for review (< {threshold:.2f}):")
            for r in flagged:
                lines.append(f"  - {r.fixture_id}")
                for a in r.axes:
                    if a.value < threshold:
                        lines.append(f"      {a.name}: {a.value:.3f} - {a.reasons[0] if a.reasons else ''}")
