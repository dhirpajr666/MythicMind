"""mythicmind — rapid AI NPC behaviour evaluation lab (Python side).

The Python package provides an explainable, stdlib-only evaluation harness. It
ingests persona / scenario / dialogue fixtures (JSON), scores each transcript
along four axes — consistency, goals, safety and latency — using transparent
heuristics whose contributions are always reported, and rolls the per-fixture
results up into batch reports.

There is intentionally no machine-learning dependency: every score is a small,
inspectable arithmetic combination so a designer can see *why* an NPC scored
the way it did.
"""

__version__ = "1.0.0"

from .model import Persona, Scenario, DialogueTurn, Fixture  # noqa: F401
from .scoring import evaluate_fixture, EvaluationResult  # noqa: F401
