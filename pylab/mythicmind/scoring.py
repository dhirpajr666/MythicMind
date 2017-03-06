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
