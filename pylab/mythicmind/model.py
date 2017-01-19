"""Fixture data model.

Fixtures are plain JSON on disk. These dataclasses give them structure and a
single, validated place to load them from. Everything here is stdlib-only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Persona:
    """The NPC's stated identity: who it is and what it must never do."""

    npc_id: str
    name: str
    traits: list[str] = field(default_factory=list)
    # Phrases the persona is expected to lean on (voice consistency).
    voice_markers: list[str] = field(default_factory=list)
    # Words/phrases that are out of character for this persona.
    forbidden: list[str] = field(default_factory=list)

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "Persona":
        return Persona(
            npc_id=str(d["npc_id"]),
            name=str(d.get("name", d["npc_id"])),
            traits=[str(x) for x in d.get("traits", [])],
            voice_markers=[str(x).lower() for x in d.get("voice_markers", [])],
            forbidden=[str(x).lower() for x in d.get("forbidden", [])],
        )


@dataclass(frozen=True)
class Scenario:
    """The situation the NPC is placed in and the goals it should pursue."""

    scenario_id: str
    summary: str
    goals: list[str] = field(default_factory=list)
    # Latency budget in milliseconds for a single NPC response.
    latency_budget_ms: float = 800.0

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "Scenario":
        return Scenario(
            scenario_id=str(d["scenario_id"]),
            summary=str(d.get("summary", "")),
            goals=[str(x).lower() for x in d.get("goals", [])],
            latency_budget_ms=float(d.get("latency_budget_ms", 800.0)),
        )
