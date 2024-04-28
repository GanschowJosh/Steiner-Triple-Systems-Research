from collections import defaultdict


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
    num_nodes = max(graph.keys())+1
    visited = [False] * num_nodes

    for node in graph:
        if not visited[node]:
            dfs(node, visited, [])

    return cycles

def cycleFromPair(a, b, system):
    edgesFromPair = []
    #alphabet = "abcdefghijklmnopqrstuvwxyz"
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
    
    #for cycle in allCycles:
        #cyDict[len(cycle)] += 1
    #print(cycleLengthDict)
    return max(len(cycle) for cycle in allCycles)

def paschPair(a, b, system):
    edgesFromPair = []
    #alphabet = "abcdefghijklmnopqrstuvwxyz"
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
    
    #for cycle in allCycles:
        #cyDict[len(cycle)] += 1
    #print(cycleLengthDict)
    cyclesOfLength4 = [cycle for cycle in allCycles if len(cycle) == 4]
    #print(cyclesOfLength4)
    return cyclesOfLength4

def swapPoints(system, a, b, cycle):
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

    # Identify adjacent nodes in the cycle
    for i in range(len(cycle)):
        current_node = cycle[i]
        next_node = cycle[(i + 1) % len(cycle)]
        # Swap edges corresponding to adjacent nodes in the cycle
        graph[current_node].remove(next_node)
        graph[next_node].remove(current_node)
        graph[current_node].append(cycle[(i + 2) % len(cycle)])
        graph[cycle[(i + 2) % len(cycle)]].append(current_node)

    return graph

def cyclesReduced(beforeGraph, afterGraph):
    cyclesBefore = find_cycles(beforeGraph)
    cyclesAfter = find_cycles(afterGraph)
    return max(len(cycle) for cycle in cyclesAfter) < max(len(cycle) for cycle in cyclesBefore)

pairs=[]
paschPairs = {}
cycleDict = {}
g = [{1, 2, 21}, {1, 3, 7}, {8, 1, 4}, {1, 19, 5}, {1, 6, 15}, {1, 11, 9}, {1, 10, 23}, {16, 1, 12}, {1, 20, 13}, {1, 14, 25}, {1, 18, 17}, {24, 1, 22}, {2, 3, 23}, {24, 2, 4}, {17, 2, 5}, {2, 11, 6}, {2, 22, 7}, {8, 25, 2}, {9, 2, 12}, {2, 10, 13}, {16, 2, 14}, {2, 18, 15}, {2, 19, 20}, {25, 3, 4}, {3, 5, 14}, {17, 3, 6}, {8, 3, 20}, {9, 3, 13}, {10, 3, 12}, {11, 3, 21}, {3, 22, 15}, {16, 18, 3}, {19, 24, 3}, {13, 4, 5}, {18, 4, 6}, {4, 14, 7}, {9, 4, 21}, {10, 11, 4}, {4, 12, 23}, {4, 20, 15}, {16, 4, 22}, {17, 19, 4}, {21, 5, 6}, {20, 5, 7}, {8, 12, 5}, {9, 5, 15}, {10, 18, 5}, {16, 11, 5}, {25, 5, 22}, {24, 5, 23}, {8, 6, 7}, {9, 20, 6}, {24, 10, 6}, {12, 6, 14}, {13, 6, 22}, {16, 25, 6}, {19, 6, 23}, {9, 19, 7}, {25, 10, 7}, {11, 15, 7}, {12, 21, 7}, {18, 13, 7}, {16, 23, 7}, {24, 17, 7}, {8, 9, 18}, {8, 10, 15}, {8, 17, 11}, {8, 24, 13}, {8, 19, 14}, {8, 16, 21}, {8, 22, 23}, {9, 10, 22}, {24, 9, 14}, {16, 9, 17}, {9, 25, 23}, {17, 10, 14}, {16, 10, 20}, {10, 19, 21}, {11, 12, 20}, {11, 13, 23}, {18, 11, 14}, {19, 11, 22}, {24, 25, 11}, {25, 12, 13}, {19, 12, 15}, {17, 12, 22}, {24, 18, 12}, {13, 14, 15}, {16, 19, 13}, {17, 21, 13}, {20, 14, 23}, {21, 14, 22}, {16, 24, 15}, {17, 23, 15}, {25, 21, 15}, {17, 20, 25}, {25, 18, 19}, {18, 20, 22}, {18, 21, 23}, {24, 20, 21}]
#cycleLengthDict = defaultdict(int) #length: num 
for a in range(25, 0, -1):
    for b in range(1, 26):
        if a!=b:
            pairs.append((a, b))
    #print(pairs)
    for pair in pairs:
        #print(pair)
        a, b = pair
        ret = paschPair(a, b, g)
        #cycleDict[(a, b)] = ret 
        if len(ret) > 0:
            paschPairs[(a,b)] = ret
        #paschPairs.append(ret)
#print(paschPairs)
#print(cycleDict)
#print(cycleLengthDict)
#print(paschPairs.items())

def isSteinerTripleSystem(points, triples):
    print(triples)
    # Create a set of all triples
    triples_set = set(map(frozenset, triples))

    # Check if every pair of points appears in exactly one triple
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            pair = frozenset([points[i], points[j]])
            count = sum(1 for triple in triples_set if pair <= triple)
            if count != 1:
                return False

    # Check if the order of the system is congruent to 1 or 3 modulo 6
    order = len(points)
    if order % 6 not in [1, 3]:
        return False

    # Return True if all checks passed
    return True
for pair, pasch_configurations in paschPairs.items():
    a, b = pair
    for pasch_configuration in pasch_configurations:
        print("Before swapping:", pasch_configuration)
        # Perform the swap
        graph = swapPoints(g, a, b, pasch_configuration)
        if(isSteinerTripleSystem((i for i in range (1, 26)), graph)):
            # Recalculate cycles after swap
            cycles_before = find_cycles({i: list(graph[i]) for i in range(len(graph))})
            # Undo the swap
            swapPoints(g, a, b, pasch_configuration)
            # Perform the maximum cycle reduction check
            swapPoints(g, a, b, pasch_configuration)
            cycles_after = find_cycles({i: list(graph[i]) for i in range(len(graph))})
            swapPoints(g, a, b, pasch_configuration)
            if cyclesReduced(cycles_before, cycles_after):
                print("Swapping points", a, "and", b, "reduces the length of the maximum cycle.")
            else:
                print("Swapping points", a, "and", b, "does not reduce the length of the maximum cycle.")
        else:
            continue 
