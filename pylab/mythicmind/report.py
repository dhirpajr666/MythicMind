"""Batch report generation.

Given a set of :class:`EvaluationResult` objects, produce both a machine
readable summary (dict / JSON) and a compact human-readable text report.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

from .scoring import EvaluationResult

