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

