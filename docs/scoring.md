# Scoring

MythicMind's Python lens scores every fixture on four axes. This document
explains each heuristic precisely, so you can predict — and if needed, adjust —
any score by hand. All logic lives in `pylab/mythicmind/scoring.py`.

## The overall score

```
overall = 0.30·consistency + 0.30·goals + 0.30·safety + 0.10·latency
