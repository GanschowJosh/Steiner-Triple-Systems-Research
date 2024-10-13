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
    
    
    allCycles = find_cycles(graph)
    
    for cycle in allCycles:
        if len(cycle) == 4:
            cyclesOfLength4.append(cycle)

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