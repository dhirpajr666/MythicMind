"""Fixture data model.

Fixtures are plain JSON on disk. These dataclasses give them structure and a
single, validated place to load them from. Everything here is stdlib-only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
