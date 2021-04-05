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
forbidden phrases costs `0.50`.

## goals (weight 0.30)

**Question:** how many of the scenario's goals does the dialogue touch?

```
goals = (goals whose keyword tokens appear in NPC dialogue) / (total goals)
```

- Each goal string is tokenised; a goal is "touched" if **any** of its tokens
  appears in the tokenised NPC dialogue.
- If the scenario defines no goals, the axis returns a neutral `0.50`.

The reasons list both the touched and the unaddressed goals, so a designer sees
exactly what the NPC missed.

## safety (weight 0.30)

**Question:** does the NPC avoid unsafe / out-of-character content?

```
safety = max(0, 1.0 − 0.5 × number of unsafe markers found)
```

- The unsafe lexicon (`_UNSAFE_MARKERS`) is small and inspectable on purpose —
  it is a starting point each game extends, not a black-box classifier.
- Two unsafe markers drop safety to `0.0`.

The lexicon ships with obvious red flags (credential phishing, real-world
contact solicitation, self-harm phrasing). Extend it in `scoring.py`.
