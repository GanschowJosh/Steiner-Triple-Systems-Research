# Implemented algorithms

## Revised Stinson generation

`Scripts/STSGenerator.py` implements the revised Stinson hill-climbing
algorithm for constructing an STS(n).

The generator maintains, for every point, a compact collection of *live pairs*
that have not yet been covered by a block. A switching step selects a live
point and two of its live neighbors. If their pair is also uncovered, the
three points form a new block. Otherwise, the conflicting block is exchanged
and its displaced pairs become live again. Switching continues until the
system contains

```text
n(n - 1) / 6
```

blocks. The implementation is effective in practice, although the randomized
hill-climbing procedure does not provide a theoretical termination guarantee.

## Validation

`isSteinerTripleSystem` verifies that:

1. the order is congruent to 1 or 3 modulo 6; and
2. every unordered pair of points occurs in exactly one block.

This direct validator favors clarity over asymptotic efficiency and is useful
for generated examples and smoke tests.

## Cycle graphs and circumference

`Scripts/graph.py` constructs the cycle graph associated with each unordered
pair of points. For a valid STS, each such graph is 2-regular, so its connected
components are cycles. NetworkX is used to obtain a cycle basis, and the
largest observed cycle length is returned as the system's circumference.

An STS(n) is antiperfect precisely when the returned circumference is less
than `n - 3`.

## Pasch detection and trades

A Pasch configuration consists of four blocks on six points in which each
point occurs twice. `Scripts/Pasch_checker.py` indexes blocks by point and
searches compatible block combinations to determine whether a system contains
such a configuration.

The experimental programs in `Scripts/Process` also explore Pasch trades,
which replace one Pasch configuration with its complementary four blocks.
These trades move between STS configurations while preserving the defining
pair-incidence property.

## Large-catalog processing

`Scripts/Multiprocessing_bits.py` processes a compressed representation of
62,336,617 order-21 systems with prescribed automorphism groups. It rebuilds
systems from orbit data, validates them, computes their circumference, and
writes qualifying systems incrementally. A bounded process pool permits the
catalog to be analyzed without retaining every reconstructed system in memory.

The catalog itself is external research data and is intentionally excluded
from this repository.

## Cycle vectors

`Scripts/STS21_vectorization.py` summarizes the cycle structure of order-21
systems as vectors. These vectors support grouping and comparison without
retaining every individual cycle graph.
