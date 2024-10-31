"""
old version of graph module with no networkx
"""
from collections import defaultdict
from itertools import cycle, combinations
import math

def paschtrade(system, a, b): #returns list of lists
    newsystem = []
    for triple in system:
        x, y, z = triple
        if x == a: newtriple = [b, y, z]
        if x == b: newtriple = [a, y, z]
        if y == a: newtriple = [x, b, z]
        if y == b: newtriple = [x, a, z]
        if z == a: newtriple = [x, y, b]
        if z == b: newtriple = [x, y, a]
        else: newtriple = [x, y, z]
        newsystem.append(newtriple)
    return newsystem

def find_cycles(graph):
    def dfs(node, visited, current_path):
        visited[node] = True
        current_path.append(node)

        for neighbor in graph[node]:
            if neighbor not in current_path:
                if not visited[neighbor]:
                    dfs(neighbor, visited, current_path)
            else: 
                # Found a cycle
                cycle_start = current_path.index(neighbor)
                cycle = current_path[cycle_start:]
                cycles.append(cycle)

        current_path.pop()
        visited[node] = False

    cycles = []
    num_nodes = max(graph.keys()) + 1
    visited = [False] * num_nodes

    for node in graph:
        if not visited[node]:
            dfs(node, visited, [])

    return cycles

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

    graph = {i: [] for i in range(max(max(pair) for pair in edgesFromPair) + 1)}
    for edge in edgesFromPair:
        graph[edge[0]].append(edge[1])
        graph[edge[1]].append(edge[0])
    
    
    allCycles = find_cycles(graph)
    
    # cycles_of_length_4 = [cycle for cycle in allCycles if len(cycle) == 4]
    # print(cycles_of_length_4)

    return max(len(cycle) for cycle in allCycles)

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
    testSystem1 = [{1, 4, 5}, {1, 6, 7}, {8, 1, 9}, {1, 10, 11}, {1, 12, 13}, {1, 14, 15}, {16, 1, 17}, {1, 18, 20}, {1, 19, 21}, {1, 2, 3}, {2, 4, 6}, {2, 5, 7}, {8, 2, 10}, {9, 2, 11}, {2, 12, 14}, {2, 13, 15}, {19, 2, 18}, {16, 2, 20}, {17, 2, 21}, {3, 4, 7}, {3, 5, 6}, {8, 11, 3}, {9, 10, 3}, {3, 12, 15}, {3, 13, 14}, {3, 20, 21}, {16, 19, 3}, {17, 18, 3}, {8, 4, 12}, {9, 13, 5}, {9, 18, 4}, {8, 19, 5}, {16, 4, 13}, {17, 12, 5}, {4, 21, 15}, {20, 5, 14}, {17, 10, 4}, {16, 11, 5}, {19, 4, 14}, {18, 5, 15}, {11, 4, 20}, {10, 21, 5}, {10, 6, 14}, {11, 15, 7}, {10, 19, 15}, {18, 11, 14}, {10, 20, 13}, {11, 12, 21}, {19, 11, 6}, {10, 18, 7}, {16, 10, 12}, {17, 11, 13}, {18, 12, 6}, {19, 13, 7}, {21, 13, 6}, {12, 20, 7}, {8, 18, 13}, {9, 19, 12}, {16, 18, 21}, {17, 19, 20}, {8, 20, 15}, {9, 21, 14}, {9, 20, 6}, {8, 21, 7}, {8, 16, 6}, {9, 17, 7}, {17, 6, 15}, {16, 14, 7}, {8, 17, 14}, {16, 9, 15}]
    testSystem2 = [{1, 4, 5}, {1, 6, 7}, {8, 1, 9}, {1, 10, 11}, {1, 12, 13}, {1, 14, 15}, {16, 1, 17}, {1, 18, 20}, {1, 19, 21}, {1, 2, 3}, {2, 4, 6}, {2, 5, 7}, {8, 2, 10}, {9, 2, 11}, {2, 12, 14}, {2, 13, 15}, {19, 2, 18}, {16, 2, 20}, {17, 2, 21}, {3, 4, 7}, {3, 5, 6}, {8, 11, 3}, {9, 10, 3}, {3, 12, 15}, {3, 13, 14}, {3, 20, 21}, {16, 19, 3}, {17, 18, 3}, {8, 4, 12}, {9, 13, 5}, {9, 18, 4}, {8, 19, 5}, {16, 4, 13}, {17, 12, 5}, {4, 21, 15}, {20, 5, 14}, {17, 10, 4}, {16, 11, 5}, {19, 4, 14}, {18, 5, 15}, {11, 4, 20}, {10, 21, 5}, {10, 6, 14}, {11, 15, 7}, {10, 19, 15}, {18, 11, 14}, {10, 20, 13}, {11, 12, 21}, {19, 11, 6}, {10, 18, 7}, {16, 10, 12}, {17, 11, 13}, {18, 12, 6}, {19, 13, 7}, {21, 13, 6}, {12, 20, 7}, {8, 18, 13}, {9, 19, 12}, {16, 18, 21}, {17, 19, 20}, {8, 20, 15}, {9, 21, 14}, {9, 20, 6}, {8, 21, 7}, {8, 16, 6}, {9, 17, 7}, {17, 6, 15}, {16, 14, 7}, {8, 17, 14}, {16, 9, 15}]

    print(processSystem(testSystem1))
    print(processSystem(testSystem2))