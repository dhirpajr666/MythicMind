# Architecture

MythicMind is two independent programs that share a philosophy and a data
directory. This document describes how each is built and where the seams are.

## Overview

```
          PRODUCES behaviour                 JUDGES behaviour
        ┌────────────────────┐            ┌────────────────────┐
        │   C# .NET 9 lens    │  JSON      │    Python lens      │
        │   runtime/          │  transcript│    pylab/           │
        │                     │───────────▶│                     │
        │  World → Goals →    │            │  Fixtures → Axes →  │
        │  Memory → Replay    │            │  Reasons → Report   │
        └────────────────────┘            └────────────────────┘
                  ▲                                   ▲
