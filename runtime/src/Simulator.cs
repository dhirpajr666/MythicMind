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
