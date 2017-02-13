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
