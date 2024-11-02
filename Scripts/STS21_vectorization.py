"""
Script to take in a list of STS21s and convert them to a vector that shows the 
number of each type of cycle graph that appears in the STS21. Listed below are the types
T1: [4,4,4,6]
T2: [4,4,10]
T3: [4,6,8]
T4: [4,14]
T5: [6,6,6]
T6: [6,12]
T7: [8,10]
Vectors in form of [T1, T2, T3, T4, T5, T6, T7]

Since each cycle graph of a STS21 has 18 vertices and breaks down into cycles of even length,
we can obtain the above possible cycle graphs. Additionally, because the STS21 has 21 choose 2 = 210 pairs of vertices, 
the sum of the vector should be 210.
"""

import networkx as nx
from collections import defaultdict, Counter
import math
from itertools import combinations
import sys

# Define the cycle types
CYCLE_TYPES = {
    'T1': sorted([4, 4, 4, 6]),
    'T2': sorted([4, 4, 10]),
    'T3': sorted([4, 6, 8]),
    'T4': sorted([4, 14]),
    'T5': sorted([6, 6, 6]),
    'T6': sorted([6, 12]),
    'T7': sorted([8, 10]),
}

def read_sts21_file(filename):
    """
    Function to read in the STS21 systems from a file and return a list of systems.
    """
    with open(filename, 'r') as file:
        sts21_list = []
        for line in file:
            sts21_list.append(eval(line))
    return sts21_list

def find_cycle_structure(graph):
    """
    Finds all cycles in the graph and returns a sorted list of their lengths.
    Ensures that cycles are even-length as per STS21 properties.
    """
    cycles = nx.cycle_basis(graph)
    cycle_lengths = [len(cycle) for cycle in cycles]
    
    # Ensure all cycles are even-length
    if any(length % 2 != 0 for length in cycle_lengths):
        print("Warning: Found odd-length cycle.")
    
    return sorted(cycle_lengths)

def classify_cycle_structure(cycle_structure):
    """
    Classifies the given cycle structure into one of the predefined types.
    Returns the type key (e.g., 'T1') or None if no match is found.
    """
    for type_key, type_structure in CYCLE_TYPES.items():
        if cycle_structure == type_structure:
            return type_key
    return None

def graph_from_pair(a, b, system):
    """
    Constructs a graph based on the given pair (a, b) and the STS21 system.
    Returns a NetworkX graph.
    """
    edges_from_pair = []
    for triple in system:
        x, y, z = triple
        if x == a or x == b:
            edges_from_pair.append((y, z))
        elif y == a or y == b:
            edges_from_pair.append((x, z))
        elif z == a or z == b:
            edges_from_pair.append((x, y))
    
    graph = nx.Graph()
    graph.add_edges_from(edges_from_pair)
    
    return graph

def process_sts21(system):
    """
    Processes a single STS21 system and returns the cycle type vector.
    """
    num_nodes = int((1 + math.isqrt(1 + 24 * len(system))) / 2)
    if num_nodes != 21:
        raise ValueError(f"Expected STS21 with 21 nodes, got {num_nodes}")
    
    type_counts = Counter({'T1':0, 'T2':0, 'T3':0, 'T4':0, 'T5':0, 'T6':0, 'T7':0})
    
    vertices = list(range(1, num_nodes + 1))
    pairs = combinations(vertices, 2)
    
    for a, b in pairs:
        graph = graph_from_pair(a, b, system)
        if not graph.edges:
            # No cycles can be formed if there are no edges
            continue
        cycle_structure = find_cycle_structure(graph)
        cycle_type = classify_cycle_structure(cycle_structure)
        if cycle_type:
            type_counts[cycle_type] += 1
        else:
            # didn't find a cycle type match
            print(f"Unmatched cycle structure {cycle_structure} for pair ({a}, {b})")
    
    # Create the vector in the order [T1, T2, T3, T4, T5, T6, T7]
    vector = [
        type_counts['T1'],
        type_counts['T2'],
        type_counts['T3'],
        type_counts['T4'],
        type_counts['T5'],
        type_counts['T6'],
        type_counts['T7'],
    ]
    
    # Verify that the sum is 210 (C(21,2))
    total = sum(vector)
    if total != 210:
        print(f"Warning: Total cycle types count {total} does not equal 210.")
    
    return vector

def main(input_file, output_file):
    sts21_list = read_sts21_file(input_file)
    print(f"Found {len(sts21_list)} STS21 systems.")
    
    with open(output_file, 'w') as out:
        # Write header
        out.write("STS21_Index,T1,T2,T3,T4,T5,T6,T7\n")
        for idx, system in enumerate(sts21_list, 1):
            vector = process_sts21(system)
            vector_str = ",".join(map(str, vector))
            out.write(f"{idx},{vector_str}\n")
            print(f"Processed STS21 #{idx}: {vector}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python STS21_vectorization.py <input_file> <output_file>")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    
    main(input_filename, output_filename)
