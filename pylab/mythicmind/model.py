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


@dataclass(frozen=True)
class DialogueTurn:
    """A single NPC utterance plus the measured latency that produced it."""

    speaker: str
    text: str
    latency_ms: float = 0.0

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "DialogueTurn":
        return DialogueTurn(
            speaker=str(d.get("speaker", "npc")),
            text=str(d.get("text", "")),
            latency_ms=float(d.get("latency_ms", 0.0)),
        )


@dataclass(frozen=True)
class Fixture:
    """A complete evaluation unit: persona + scenario + a dialogue trace."""

    fixture_id: str
    persona: Persona
    scenario: Scenario
    dialogue: list[DialogueTurn]

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "Fixture":
        return Fixture(
            fixture_id=str(d["fixture_id"]),
            persona=Persona.from_dict(d["persona"]),
            scenario=Scenario.from_dict(d["scenario"]),
            dialogue=[DialogueTurn.from_dict(t) for t in d.get("dialogue", [])],
        )

    @staticmethod
    def load(path: str | Path) -> "Fixture":
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        return Fixture.from_dict(raw)

    def npc_turns(self) -> list[DialogueTurn]:
        """Only the NPC's own utterances (the thing under evaluation)."""
