using System;
using System.Collections.Generic;
using System.Linq;

namespace MythicMind.Runtime;

/// <summary>
/// The mutable state of a simulated encounter world. Everything an NPC can
/// observe or affect lives here. State mutation is intentionally centralised
/// so that a full snapshot can be emitted per tick for the transcript.
/// </summary>
public sealed class WorldState
{
    /// <summary>Named world facts, e.g. "gate.open" -> "false".</summary>
    public Dictionary<string, string> Flags { get; } = new(StringComparer.Ordinal);

    /// <summary>Named numeric resources, e.g. "party.gold" -> 40.</summary>
    public Dictionary<string, double> Resources { get; } = new(StringComparer.Ordinal);

