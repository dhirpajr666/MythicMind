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
