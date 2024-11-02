import networkx as nx
from collections import defaultdict
import math
from itertools import combinations

def find_max_cycle(graph):
    g = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            g.add_edge(node, neighbor)
    
    max_length = 0
    for cycle in nx.cycle_basis(g):
        max_length = max(max_length, len(cycle))
    
    return max_length

def cycleFromPair(a, b, system):
    edgesFromPair = []
    for triple in system:
        x, y, z = triple
        if x == a or x == b:
            edgesFromPair.append((y, z))
        elif y == a or y == b:
            edgesFromPair.append((x, z))
        elif z == a or z == b:
            edgesFromPair.append((x, y))
    
    graph_dict = defaultdict(list)
    for edge in edgesFromPair:
        graph_dict[edge[0]].append(edge[1])
        graph_dict[edge[1]].append(edge[0])
    
    return find_max_cycle(graph_dict)

def processSystem(system):
    #cute usage of the quadratic formula, but not needed
    #numNodes = int((1+math.sqrt(1+24*(len(system))))/2)
    numNodes = max(max(triple) for triple in system)
    pairs = combinations(list(i+1 for i in range(numNodes)), 2)
    cycleMax = 0
    for a, b in pairs:
        currCycle = cycleFromPair(a, b, system)
        if currCycle > cycleMax:
            cycleMax = currCycle
        if cycleMax > numNodes-3: #cutting off at n-3, don't even need to look at the rest of the system
            return cycleMax
    
    return cycleMax
