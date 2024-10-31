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
    numNodes = int((1+math.sqrt(1+24*(len(system))))/2)
    pairs = combinations(list(i+1 for i in range(numNodes)), 2)
    cycleMax = 0
    for a, b in pairs:
        currCycle = cycleFromPair(a, b, system)
        if currCycle > cycleMax:
            cycleMax = currCycle
        if cycleMax > numNodes-3: #cutting off at n-3, don't even need to look at the rest of the system
            return cycleMax
    
    return cycleMax

if __name__ == "__main__":
    # testing
    testSystem1 = [{1, 4, 5}, {1, 6, 7}, {8, 1, 9}, {1, 10, 11}, {1, 12, 13}, {1, 14, 15}, {16, 1, 17}, {1, 18, 20}, {1, 19, 21}, {1, 2, 3}, {2, 4, 6}, {2, 5, 7}, {8, 2, 10}, {9, 2, 11}, {2, 12, 14}, {2, 13, 15}, {19, 2, 18}, {16, 2, 20}, {17, 2, 21}, {3, 4, 7}, {3, 5, 6}, {8, 11, 3}, {9, 10, 3}, {3, 12, 15}, {3, 13, 14}, {3, 20, 21}, {16, 19, 3}, {17, 18, 3}, {8, 4, 12}, {9, 13, 5}, {9, 18, 4}, {8, 19, 5}, {16, 4, 13}, {17, 12, 5}, {4, 21, 15}, {20, 5, 14}, {17, 10, 4}, {16, 11, 5}, {19, 4, 14}, {18, 5, 15}, {11, 4, 20}, {10, 21, 5}, {10, 6, 14}, {11, 15, 7}, {10, 19, 15}, {18, 11, 14}, {10, 20, 13}, {11, 12, 21}, {19, 11, 6}, {10, 18, 7}, {16, 10, 12}, {17, 11, 13}, {18, 12, 6}, {19, 13, 7}, {21, 13, 6}, {12, 20, 7}, {8, 18, 13}, {9, 19, 12}, {16, 18, 21}, {17, 19, 20}, {8, 20, 15}, {9, 21, 14}, {9, 20, 6}, {8, 21, 7}, {8, 16, 6}, {9, 17, 7}, {17, 6, 15}, {16, 14, 7}, {8, 17, 14}, {16, 9, 15}]
    print(processSystem(testSystem1))
    testSystem2 = [{1, 2, 19}, {1, 10, 3}, {16, 1, 4}, {1, 11, 5}, {1, 6, 9}, {1, 17, 7}, {8, 1, 13}, {1, 12, 15}, {1, 14, 22}, {1, 18, 20}, {1, 21, 25}, {24, 1, 23}, {2, 3, 20}, {2, 4, 21}, {2, 5, 23}, {17, 2, 6}, {2, 12, 7}, {8, 2, 22}, {9, 2, 18}, {2, 10, 14}, {24, 2, 11}, {2, 13, 15}, {16, 25, 2}, {9, 3, 4}, {3, 5, 7}, {3, 12, 6}, {8, 17, 3}, {11, 3, 13}, {16, 3, 14}, {25, 3, 15}, {18, 3, 23}, {19, 3, 21}, {24, 3, 22}, {12, 4, 5}, {11, 4, 6}, {4, 13, 7}, {8, 18, 4}, {10, 19, 4}, {17, 4, 14}, {4, 20, 15}, {4, 22, 23}, {24, 25, 4}, {5, 6, 22}, {8, 10, 5}, {24, 9, 5}, {13, 20, 5}, {25, 5, 14}, {16, 5, 15}, {17, 19, 5}, {18, 21, 5}, {24, 6, 7}, {8, 16, 6}, {10, 6, 23}, {21, 13, 6}, {20, 6, 14}, {19, 6, 15}, {25, 18, 6}, {8, 25, 7}, {9, 14, 7}, {10, 20, 7}, {19, 11, 7}, {18, 15, 7}, {16, 23, 7}, {21, 22, 7}, {8, 9, 20}, {8, 11, 21}, {8, 24, 12}, {8, 19, 14}, {8, 23, 15}, {9, 10, 25}, {9, 11, 23}, {9, 12, 21}, {9, 13, 22}, {9, 17, 15}, {16, 9, 19}, {17, 10, 11}, {10, 12, 22}, {10, 18, 13}, {24, 10, 15}, {16, 10, 21}, {11, 12, 14}, {11, 22, 15}, {16, 18, 11}, {25, 11, 20}, {16, 12, 13}, {17, 12, 20}, {18, 19, 12}, {25, 12, 23}, {13, 14, 23}, {17, 13, 25}, {24, 19, 13}, {21, 14, 15}, {24, 18, 14}, {16, 17, 24}, {16, 20, 22}, {17, 18, 22}, {17, 21, 23}, {19, 20, 23}, {25, 19, 22}, {24, 20, 21}]
    print(processSystem(testSystem2))