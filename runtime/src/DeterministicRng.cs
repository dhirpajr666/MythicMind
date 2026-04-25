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

    /// <summary>Derive a child generator from a string label (stable hashing).</summary>
    public static DeterministicRng FromLabel(ulong baseSeed, string label)
    {
        ulong h = baseSeed ^ 0x9E3779B97F4A7C15UL;
        foreach (char c in label)
        {
            h ^= c;
            h *= 0x100000001B3UL;
        }
        return new DeterministicRng(h);
    }

    public ulong NextUInt64()
    {
        _state += 0x9E3779B97F4A7C15UL;
        ulong z = _state;
        z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9UL;
        z = (z ^ (z >> 27)) * 0x94D049BB133111EBUL;
        return z ^ (z >> 31);
    }

    /// <summary>Uniform integer in [0, maxExclusive).</summary>
    public int NextInt(int maxExclusive)
    {
        if (maxExclusive <= 0) throw new ArgumentOutOfRangeException(nameof(maxExclusive));
        return (int)(NextUInt64() % (ulong)maxExclusive);
    }

    /// <summary>Uniform double in [0, 1).</summary>
    public double NextDouble()
    {
        // Use the top 53 bits for a clean double mantissa.
        return (NextUInt64() >> 11) * (1.0 / 9007199254740992.0);
    }
}
