using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace MythicMind.Runtime;

/// <summary>
/// The on-disk description of an encounter: the seed, initial world facts,
/// the roster of NPCs with their goals, and the number of ticks to run.
/// Loaded from JSON so encounters are data, not code, and fully replayable.
/// </summary>
public sealed class EncounterDefinition
{
    [JsonPropertyName("name")] public string Name { get; set; } = "unnamed";
    [JsonPropertyName("seed")] public ulong Seed { get; set; } = 1;
    [JsonPropertyName("ticks")] public int Ticks { get; set; } = 8;
    [JsonPropertyName("flags")] public Dictionary<string, string> Flags { get; set; } = new();
    [JsonPropertyName("resources")] public Dictionary<string, double> Resources { get; set; } = new();
    [JsonPropertyName("npcs")] public List<NpcDefinition> Npcs { get; set; } = new();

    private static readonly JsonSerializerOptions ReadOptions = new()
    {
        PropertyNameCaseInsensitive = true,
        ReadCommentHandling = JsonCommentHandling.Skip,
        AllowTrailingCommas = true,
    };

    public static EncounterDefinition Load(string path)
    {
        string json = File.ReadAllText(path);
        var def = JsonSerializer.Deserialize<EncounterDefinition>(json, ReadOptions)
                  ?? throw new InvalidDataException($"Could not parse encounter: {path}");
        if (def.Npcs.Count == 0)
            throw new InvalidDataException($"Encounter '{def.Name}' has no NPCs.");
        return def;
    }

    public WorldState ToWorld()
    {
        var world = new WorldState();
        foreach (var kv in Flags) world.SetFlag(kv.Key, kv.Value);
        foreach (var kv in Resources) world.Resources[kv.Key] = kv.Value;
        foreach (var nd in Npcs)
        {
            var npc = new Npc { Id = nd.Id, Persona = nd.Persona, Mood = nd.Mood };
            foreach (var gd in nd.Goals)
            {
