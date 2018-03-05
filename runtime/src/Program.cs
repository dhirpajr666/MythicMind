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
