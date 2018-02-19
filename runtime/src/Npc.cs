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
