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
