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

    /// <summary>All NPCs currently present in the encounter, keyed by id.</summary>
    public Dictionary<string, Npc> Npcs { get; } = new(StringComparer.Ordinal);

    /// <summary>Current simulation tick (0-based).</summary>
    public int Tick { get; set; }

    public string GetFlag(string key, string fallback = "") =>
        Flags.TryGetValue(key, out var v) ? v : fallback;

    public bool GetBoolFlag(string key) =>
        Flags.TryGetValue(key, out var v) && string.Equals(v, "true", StringComparison.OrdinalIgnoreCase);

    public double GetResource(string key, double fallback = 0) =>
        Resources.TryGetValue(key, out var v) ? v : fallback;

    public void SetFlag(string key, string value) => Flags[key] = value;

    public void AddResource(string key, double delta) =>
