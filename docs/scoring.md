# Scoring

MythicMind's Python lens scores every fixture on four axes. This document
explains each heuristic precisely, so you can predict — and if needed, adjust —
any score by hand. All logic lives in `pylab/mythicmind/scoring.py`.

## The overall score

```
overall = 0.30·consistency + 0.30·goals + 0.30·safety + 0.10·latency
```

Weights are explicit constants (`_WEIGHTS`) and sum to `1.0`, so `overall` is a
plain weighted mean in `[0, 1]`.

## consistency (weight 0.30)

**Question:** does the NPC stay in voice and avoid forbidden phrasing?

```
marker_ratio = (voice markers found in dialogue) / (voice markers defined)
penalty      = min(0.5, 0.25 × number of distinct forbidden phrases used)
consistency  = max(0, marker_ratio − penalty)
```

- If the persona defines **no** voice markers, `marker_ratio` defaults to `0.50`
  (a neutral base) and a reason states this.
- Matching is case-insensitive substring matching against the joined NPC turns.

**Example:** 3/3 markers used, no forbidden phrasing → `1.00`. Using two
