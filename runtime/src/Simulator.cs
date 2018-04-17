using System;
using System.Collections.Generic;
using System.Linq;

namespace MythicMind.Runtime;

/// <summary>One recorded exchange during a tick.</summary>
public sealed record TranscriptLine(
    int Tick,
    string NpcId,
    string Goal,
    string Utterance,
    double Mood);

/// <summary>The full, replayable record of a simulated encounter.</summary>
public sealed record EncounterTranscript(
    string Encounter,
    ulong Seed,
    int Ticks,
    List<TranscriptLine> Dialogue,
    WorldSnapshot FinalWorld);

/// <summary>
/// The deterministic encounter simulator. Given an <see cref="EncounterDefinition"/>
/// it advances the world tick by tick, letting each NPC select and act on its
/// highest-priority satisfiable goal, and records every utterance. Running the
/// same definition twice yields byte-identical transcripts.
/// </summary>
public static class Simulator
{
    public static EncounterTranscript Run(EncounterDefinition def)
    {
        var world = def.ToWorld();
