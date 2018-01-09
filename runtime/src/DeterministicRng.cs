using System;

namespace MythicMind.Runtime;

/// <summary>
/// A small, fully deterministic pseudo-random generator.
/// We deliberately avoid <see cref="System.Random"/> because its internal
/// algorithm is not guaranteed stable across runtimes, which would break
/// deterministic encounter replay. This is a SplitMix64 generator: tiny,
/// well-distributed, and byte-for-byte reproducible on every platform.
/// </summary>
public sealed class DeterministicRng
{
    private ulong _state;

    public DeterministicRng(ulong seed)
    {
        _state = seed;
    }
