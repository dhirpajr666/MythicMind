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
        var rng = new DeterministicRng(def.Seed);
        var dialogue = new List<TranscriptLine>();

        for (int t = 0; t < def.Ticks; t++)
        {
            world.Tick = t;

            // NPCs act in a stable id order so replay is deterministic.
            foreach (var npc in world.Npcs.Values.OrderBy(n => n.Id, StringComparer.Ordinal))
            {
                var goal = npc.SelectGoal(world);
                if (goal is null)
                {
                    dialogue.Add(new TranscriptLine(t, npc.Id, "(none)", "*waits*", Math.Round(npc.Mood, 4)));
                    continue;
                }

                // Apply goal effects to the shared world.
                foreach (var kv in goal.SetsFlags)
                    world.SetFlag(kv.Key, kv.Value);

                // Mood drifts slightly toward warmth when a goal succeeds; a
                // small deterministic jitter keeps personalities from feeling
                // robotic without breaking reproducibility.
                var npcRng = DeterministicRng.FromLabel(def.Seed, $"{npc.Id}:{t}");
                double jitter = (npcRng.NextDouble() - 0.5) * 0.05;
                npc.Mood = Math.Clamp(npc.Mood + 0.03 + jitter, -1.0, 1.0);

                npc.Remember(new MemoryTrace(t, "acted", goal.Name, goal.Priority));

                dialogue.Add(new TranscriptLine(
                    t, npc.Id, goal.Name, goal.Line, Math.Round(npc.Mood, 4)));
            }
        }

        return new EncounterTranscript(def.Name, def.Seed, def.Ticks, dialogue, world.Snapshot());
    }
}

<!-- draft note 1444 -->
