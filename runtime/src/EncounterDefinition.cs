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
