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
