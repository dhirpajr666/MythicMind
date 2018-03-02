using System;
using System.Collections.Generic;
using System.Linq;

namespace MythicMind.Runtime;

/// <summary>
/// A single goal an NPC pursues. Goals carry a base priority and a set of
/// preconditions expressed against world flags. The highest-priority goal
/// whose preconditions are met becomes the NPC's active intent for a tick.
/// </summary>
public sealed class Goal
{
    public required string Name { get; init; }
    public double Priority { get; init; } = 1.0;

    /// <summary>Flag conditions of the form key => expectedValue.</summary>
    public Dictionary<string, string> Requires { get; init; } = new(StringComparer.Ordinal);

    /// <summary>Utterance template the NPC speaks when this goal is active.</summary>
    public string Line { get; init; } = "...";

    /// <summary>World effects applied when this goal drives a tick.</summary>
    public Dictionary<string, string> SetsFlags { get; init; } = new(StringComparer.Ordinal);

    public bool IsSatisfiable(WorldState world) =>
        Requires.All(r => string.Equals(world.GetFlag(r.Key), r.Value, StringComparison.Ordinal));
}

/// <summary>A bounded, decaying memory entry an NPC holds about the world.</summary>
public sealed record MemoryTrace(int Tick, string Kind, string Detail, double Salience);

/// <summary>
/// A non-player character with a persona, a prioritised goal stack and a
/// bounded working memory. Memory is a ring buffer capped at
/// <see cref="MemoryCapacity"/> so long encounters stay deterministic and
/// bounded in size.
/// </summary>
public sealed class Npc
{
    public const int MemoryCapacity = 16;

    public required string Id { get; init; }
    public required string Persona { get; init; }
    public double Mood { get; set; } = 0.0; // -1 hostile .. +1 warm
    public List<Goal> Goals { get; init; } = new();

