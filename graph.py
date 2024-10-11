from collections import defaultdict
from itertools import cycle, combinations
import math

# global variables
cyclesOfLength4 = []

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
    
    #print(graph)
    allCycles = find_cycles(graph)
    #print("All Cycles = ", allCycles)
    for cycle in allCycles:
        if len(cycle) == 4:
            cyclesOfLength4.append(cycle)
    #print(len(cycle) for cycle in allCycles)
    #return cyclesOfLength4[::4]
    
    #for cycle in allCycles:
        #cyDict[len(cycle)] += 1
    #print(cycleLengthDict)
    #print([cycle for cycle in allCycles if len(cycle) < 18])
    return max(len(cycle) for cycle in allCycles)
"""a = [{1, 2, 25}, {1, 3, 17}, {1, 4, 21}, {1, 20, 5}, {1, 18, 6}, {1, 10, 7}, {8, 1, 22}, {1, 11, 9}, {1, 12, 23}, {16, 1, 13}, {1, 14, 15}, {24, 1, 19}, {2, 3, 7}, {2, 19, 4}, {2, 21, 5}, {16, 2, 6}, {8, 2, 15}, {9, 2, 18}, {2, 10, 14}, {24, 2, 11}, {17, 2, 12}, {2, 13, 23}, {2, 20, 22}, {3, 4, 12}, {11, 3, 5}, {24, 3, 6}, {8, 9, 3}, {10, 3, 21}, {25, 3, 13}, {3, 14, 22}, {3, 20, 15}, {16, 19, 3}, {18, 3, 23}, {13, 4, 5}, {4, 6, 23}, {4, 20, 7}, {8, 4, 14}, {24, 9, 4}, {25, 10, 4}, {17, 11, 4}, {18, 4, 15}, {16, 4, 22}, {8, 5, 6}, {24, 5, 7}, {9, 5, 14}, {10, 18, 5}, {19, 12, 5}, {17, 5, 15}, {16, 25, 5}, {5, 22, 23}, {22, 6, 7}, {9, 12, 6}, {10, 11, 6}, {13, 6, 15}, {25, 6, 14}, {17, 20, 6}, {19, 21, 6}, {8, 16, 7}, {9, 17, 7}, {11, 23, 7}, {18, 12, 7}, {13, 14, 7}, {15, 21, 7}, {25, 19, 7}, {8, 10, 23}, {8, 19, 11}, {8, 12, 13}, {8, 17, 18}, {8, 20, 21}, {8, 24, 25}, {9, 10, 13}, {9, 19, 15}, {16, 9, 20}, {9, 21, 23}, {9, 22, 25}, {10, 12, 22}, {24, 10, 15}, {16, 17, 10}, {10, 19, 20}, {16, 11, 12}, {21, 11, 13}, {18, 11, 14}, {11, 22, 15}, {25, 11, 20}, {12, 20, 14}, {25, 12, 15}, {24, 12, 21}, {17, 19, 13}, {18, 20, 13}, {24, 13, 22}, {16, 21, 14}, {24, 17, 14}, {19, 14, 23}, {16, 23, 15}, {16, 24, 18}, {17, 21, 22}, {17, 25, 23}, {18, 19, 22}, {25, 18, 21}, {24, 20, 23}]
print(cycleFromPair(11, 19, a))"""

def processSystem(system):
    numNodes = int((1+math.sqrt(1+24*(len(system))))/2)
    pairs = combinations(list(i+1 for i in range(numNodes)), 2)
    cycleMax = 0
    for a, b in pairs:
        currCycle = cycleFromPair(a, b, system)
        if currCycle > cycleMax:
            cycleMax = currCycle
        if cycleMax > 15: #cutting off at 15, don't even need to look at the rest of the system
            return cycleMax
    
    return cycleMax