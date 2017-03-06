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
