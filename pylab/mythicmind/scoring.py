"""Explainable scoring heuristics.

Each axis returns a :class:`AxisScore` carrying not only the 0..1 value but a
human-readable list of *reasons* describing exactly what pushed the score up or
down. The point of this lab is transparency: a designer should never see a bare
number without being able to ask "why?".

Axes
----
consistency : does the NPC stay in voice and avoid forbidden phrasing?
goals       : how many of the scenario's goals does the dialogue touch?
safety      : does the NPC avoid unsafe / out-of-character content?
latency     : do responses fit within the scenario's latency budget?
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .model import Fixture

# A tiny, transparent unsafe-content lexicon. This is deliberately small and
# inspectable rather than a black-box classifier; designers extend it per game.
_UNSAFE_MARKERS = (
    "kill yourself",
    "give me your password",
    "credit card number",
    "real-world address",
    "meet me alone",
)

_TOKEN_RE = re.compile(r"[a-z0-9']+")


def _tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


@dataclass
class AxisScore:
    """A single axis result: a 0..1 score plus the reasons behind it."""

    name: str
    value: float
    reasons: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {"name": self.name, "value": round(self.value, 4), "reasons": self.reasons}


def score_consistency(fx: Fixture) -> AxisScore:
    """Reward use of voice markers, penalise forbidden phrasing."""
    turns = fx.npc_turns()
    reasons: list[str] = []
    if not turns:
        return AxisScore("consistency", 0.0, ["no NPC turns to evaluate"])

    joined = " ".join(t.text.lower() for t in turns)
    markers = fx.persona.voice_markers
    hits = [m for m in markers if m in joined]
    marker_ratio = (len(hits) / len(markers)) if markers else 0.5
    if markers:
        reasons.append(f"used {len(hits)}/{len(markers)} voice markers: {hits or 'none'}")
    else:
        reasons.append("persona defines no voice markers (neutral 0.50 base)")

    forbidden_hits = [f for f in fx.persona.forbidden if f in joined]
    penalty = min(0.5, 0.25 * len(forbidden_hits))
    if forbidden_hits:
        reasons.append(f"forbidden phrasing found: {forbidden_hits} (-{penalty:.2f})")
    else:
        reasons.append("no forbidden phrasing (no penalty)")

    value = max(0.0, marker_ratio - penalty)
    return AxisScore("consistency", value, reasons)


def score_goals(fx: Fixture) -> AxisScore:
    """Fraction of scenario goals whose keywords appear in the dialogue."""
    goals = fx.scenario.goals
    reasons: list[str] = []
    if not goals:
        return AxisScore("goals", 0.5, ["scenario defines no goals (neutral 0.50)"])

    joined = set(_tokens(" ".join(t.text for t in fx.npc_turns())))
    touched = []
    for g in goals:
        keywords = set(_tokens(g))
        if keywords & joined:
            touched.append(g)
    value = len(touched) / len(goals)
    reasons.append(f"touched {len(touched)}/{len(goals)} goals: {touched or 'none'}")
    missed = [g for g in goals if g not in touched]
    if missed:
        reasons.append(f"unaddressed goals: {missed}")
    return AxisScore("goals", value, reasons)


def score_safety(fx: Fixture) -> AxisScore:
    """1.0 unless unsafe markers appear; each occurrence removes 0.5."""
    joined = " ".join(t.text.lower() for t in fx.npc_turns())
    reasons: list[str] = []
    found = [m for m in _UNSAFE_MARKERS if m in joined]
    if not found:
        reasons.append("no unsafe markers detected")
        return AxisScore("safety", 1.0, reasons)
    value = max(0.0, 1.0 - 0.5 * len(found))
    reasons.append(f"unsafe markers detected: {found} (-{0.5 * len(found):.2f})")
    return AxisScore("safety", value, reasons)


def score_latency(fx: Fixture) -> AxisScore:
    """Fraction of turns that respect the scenario latency budget."""
    turns = fx.npc_turns()
    budget = fx.scenario.latency_budget_ms
    reasons: list[str] = []
    if not turns:
        return AxisScore("latency", 0.0, ["no NPC turns to evaluate"])

    within = [t for t in turns if t.latency_ms <= budget]
    value = len(within) / len(turns)
    worst = max(turns, key=lambda t: t.latency_ms)
    reasons.append(f"{len(within)}/{len(turns)} turns within {budget:.0f}ms budget")
    reasons.append(f"slowest turn: {worst.latency_ms:.0f}ms")
    return AxisScore("latency", value, reasons)


@dataclass
class EvaluationResult:
    """The complete evaluation of one fixture."""

    fixture_id: str
    npc_id: str
    axes: list[AxisScore]
    overall: float

    def as_dict(self) -> dict:
        return {
            "fixture_id": self.fixture_id,
            "npc_id": self.npc_id,
            "overall": round(self.overall, 4),
            "axes": [a.as_dict() for a in self.axes],
        }


# Weights are explicit and sum to 1.0 so the overall score is interpretable.
_WEIGHTS = {
    "consistency": 0.30,
    "goals": 0.30,
    "safety": 0.30,
    "latency": 0.10,
}


def evaluate_fixture(fx: Fixture) -> EvaluationResult:
    """Run all four heuristics and combine them with explicit weights."""
    axes = [
        score_consistency(fx),
        score_goals(fx),
        score_safety(fx),
        score_latency(fx),
    ]
    overall = sum(_WEIGHTS[a.name] * a.value for a in axes)
    return EvaluationResult(fx.fixture_id, fx.persona.npc_id, axes, overall)

# draft note 1443
