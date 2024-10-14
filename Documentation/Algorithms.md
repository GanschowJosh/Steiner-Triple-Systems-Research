# Algorithms in the Steiner Triple Systems Project
## Overview
This document outlines the primary algorithms implemented in the project.
## 1. Revised Stinson's Algorithm
### Purpose
Revised Stinson's Algorithm is utilized for generating valid Steiner Triple Systems based on a specific order (v)
### Description
#### Key Properties

- **Block and Point Distribution**: In an STS(v), each point appears in exactly 
  $r = \frac{v-1}{2}$ 
  blocks, where $( |B| = \frac{v(v-1)}{6} )$ represents the total number of blocks. For an STS to exist, \( v \) must satisfy $v \equiv 1$ or $3 \mod 6$.

- **Exponential Growth**: The number of non-isomorphic STS(v) on a specific set grows exponentially, making efficient construction methods valuable.

#### Problem Formulation

The task of constructing an STS(v) can be framed as a combinatorial optimization problem:

- **Instance**:
  - A positive integer $v \equiv 1$ or $3 \mod 6$.
  - A finite set $V$ such that $|V| = v$.

- **Objective**: Maximize the number of blocks ($|B|$) such that $(V, B)$ forms a Partial Steiner Triple System (PSTS).

#### Heuristic Approach

The algorithm employs a heuristic named `SWITCH` to iteratively refine the PSTS. This heuristic identifies live points and pairs, facilitating the addition of new blocks while maintaining or increasing the overall size of the system.

The `SWITCH` process involves selecting live points and exploring possible pair combinations. If a new block can be formed, it is added to the system; otherwise, existing blocks may be exchanged to maintain the structure.

#### Algorithm Overview

1. **Initialization**: Begin with an empty block set and initialize necessary data structures to track live points and pairs.
   
2. **Iterative Improvement**: Apply the `SWITCH` heuristic repeatedly to enhance the current PSTS until the maximum size is reached, ensuring all criteria for a valid STS are satisfied.

3. **Output**: Upon completion, the algorithm outputs the constructed STS(v), represented as $(V, B)$.

This algorithm is efficient in practice, often successfully generating a valid STS(v) quickly, even though there is no theoretical guarantee of termination.

## 2. Graph Cycle Analysis
### Purpose
This algorithm analyzes the graph representation of a Steiner Triple System to identify cycles, specifically targeting the longest cycle (circumference)

### Description
The cycle analysis is performed using depth-first search (DFS) to explore the graph created from the triples. The algorithm identifies all cycles and records those of length 4, which is of particular interest as this forms a Pasch configuration.

### Key functions
- `find_cycles(graph)`: Performs DFS to discover all cycles within the given graph.
- `cycleFromPair(a, b, system)`: Generates the graph from pairs and finds cycles that include the specified pair of elements

## 3. Pasch Trade Algorithm
### Purpose
The Pasch Trade algorithm modifies existing Steiner Triple Systems by swapping elements within triples to explore new configurations.

### Description
The algorithm iterates through valid Pasch pairs of elements within the system, applying trades to create new triples. It checks whether the newly generated system is a valid STS and tracks if that new configuration has a smaller circumference.

### Key Functions
- `paschtrade(system, a, b)`: Generates a new system based on swapping elements in the triples
- `performPaschTrades(system, pairs)`: Iterates through pairs, applying the Pasch trade and recording results.
