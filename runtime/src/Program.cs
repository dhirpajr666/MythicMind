using System;
using System.IO;
using System.Text.Json;
using MythicMind.Runtime;

// -----------------------------------------------------------------------------
// mythicmind runtime — deterministic NPC encounter simulator (.NET 9)
//
// Usage:
//   mythicmind run <encounter.json> [--out transcript.json] [--pretty]
//   mythicmind replay-check <encounter.json>
//
// The "run" verb simulates an encounter and emits a JSON transcript to stdout
// or a file. "replay-check" runs the same encounter twice and confirms the two
// transcripts are byte-identical, proving determinism.
// -----------------------------------------------------------------------------

var jsonOptions = new JsonSerializerOptions
{
    WriteIndented = false,
    DefaultIgnoreCondition = System.Text.Json.Serialization.JsonIgnoreCondition.Never,
};

try
{
    if (args.Length == 0)
    {
        PrintUsage();
        return 2;
    }

    switch (args[0])
    {
        case "run":
            return CmdRun(args);
        case "replay-check":
            return CmdReplayCheck(args);
        case "-h":
        case "--help":
        case "help":
            PrintUsage();
            return 0;
        default:
            Console.Error.WriteLine($"error: unknown command '{args[0]}'");
            PrintUsage();
            return 2;
    }
}
catch (FileNotFoundException ex)
{
    Console.Error.WriteLine($"error: file not found: {ex.FileName ?? ex.Message}");
    return 1;
}
catch (Exception ex)
{
    Console.Error.WriteLine($"error: {ex.Message}");
    return 1;
}

int CmdRun(string[] args)
{
    if (args.Length < 2)
    {
        Console.Error.WriteLine("error: 'run' requires an encounter file");
        return 2;
    }

    string encounterPath = args[1];
    string? outPath = null;
    bool pretty = false;

    for (int i = 2; i < args.Length; i++)
    {
        switch (args[i])
        {
            case "--out":
                if (i + 1 >= args.Length) { Console.Error.WriteLine("error: --out needs a path"); return 2; }
                outPath = args[++i];
                break;
            case "--pretty":
                pretty = true;
                break;
            default:
                Console.Error.WriteLine($"error: unknown flag '{args[i]}'");
                return 2;
        }
    }

    var def = EncounterDefinition.Load(encounterPath);
