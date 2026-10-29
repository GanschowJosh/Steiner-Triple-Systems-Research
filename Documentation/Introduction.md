# Research overview

## Steiner triple systems

A Steiner triple system of order `n`, or STS(n), consists of a set of `n`
points and a collection of three-element blocks such that every pair of points
appears in exactly one block. An STS(n) exists exactly when `n` is congruent to
1 or 3 modulo 6.

## Cycle structure

Given two distinct points `a` and `b`, remove the unique third point `c` for
which `{a, b, c}` is a block. Every block containing `a` or `b` then determines
an edge between its other two points. The resulting graph is a disjoint union
of even cycles on `n - 3` vertices and is called the cycle graph associated
with `a` and `b`.

The *circumference* of an STS is the length of the longest cycle appearing in
any of its cycle graphs. A perfect STS has one cycle of length `n - 3` in every
cycle graph. An antiperfect STS is at the opposite extreme: none of its cycle
graphs contains a cycle of length `n - 3`.

## Research goals and outcomes

This project began as a computational investigation of systems with small
circumference. It developed tools for:

- generating random systems with the revised Stinson algorithm;
- validating Steiner triple systems;
- constructing cycle graphs and measuring their circumference;
- detecting Pasch configurations and experimenting with Pasch trades; and
- processing large catalogs of order-21 systems in parallel.

The resulting work contributed to the classification and construction results
reported in “Small antiperfect Steiner triple systems,” including existence for
all admissible orders at least 15 and computational results for small orders.

Large catalogs and generated output are not stored in this repository. The
repository instead retains the algorithms, documentation, and small examples
needed to understand and exercise the computational approach.
