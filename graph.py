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
    num_nodes = max(graph.keys()) + 1
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

g = [{1, 2, 20}, {24, 1, 3}, {1, 4, 6}, {1, 10, 5}, {1, 13, 7}, {8, 1, 23}, {16, 1, 9}, {1, 11, 12}, {1, 21, 14}, {1, 17, 15}, {1, 18, 25}, {1, 19, 22}, {2, 3, 6}, {17, 2, 4}, {2, 11, 5}, {2, 15, 7}, {8, 2, 12}, {9, 2, 19}, {2, 10, 22}, {2, 13, 23}, {16, 2, 14}, {24, 2, 18}, {25, 2, 21}, {16, 3, 4}, {13, 3, 5}, {3, 22, 7}, {8, 18, 3}, {9, 3, 15}, {25, 10, 3}, {11, 3, 21}, {3, 12, 14}, {19, 17, 3}, {3, 20, 23}, {4, 5, 22}, {24, 4, 7}, {8, 10, 4}, {9, 11, 4}, {18, 4, 12}, {25, 4, 13}, {4, 14, 23}, {4, 21, 15}, {19, 4, 20}, {19, 5, 6}, {12, 5, 7}, {8, 21, 5}, {24, 9, 5}, {17, 5, 14}, {18, 5, 15}, {16, 20, 5}, {25, 5, 23}, {20, 6, 7}, {8, 6, 14}, {9, 10, 6}, {18, 11, 6}, {12, 13, 6}, {16, 6, 15}, {17, 6, 25}, {21, 6, 22}, {24, 6, 23}, {8, 17, 7}, {9, 25, 7}, {10, 14, 7}, {19, 11, 7}, {16, 23, 7}, {18, 21, 7}, {8, 9, 22}, {8, 11, 15}, {8, 20, 13}, {8, 16, 25}, {8, 24, 19}, {9, 12, 23}, {9, 13, 17}, {9, 18, 14}, {9, 20, 21}, {10, 11, 23}, {17, 10, 12}, {10, 21, 13}, {10, 19, 15}, {16, 24, 10}, {10, 18, 20}, {16, 11, 13}, {24, 11, 14}, {17, 11, 22}, {25, 11, 20}, {12, 20, 15}, {16, 19, 12}, {24, 12, 21}, {25, 12, 22}, {13, 14, 15}, {18, 19, 13}, {24, 13, 22}, {25, 19, 14}, {20, 14, 22}, {23, 22, 15}, {24, 25, 15}, {16, 17, 21}, {16, 18, 22}, {17, 18, 23}, {24, 17, 20}, {19, 21, 23}]
pairs=[]
#cycleLengthDict = defaultdict(int) #length: num 
for a in range(25, 0, -1):
    for b in range(1, 26):
        if a!=b:
            pairs.append((a, b))
#print(pairs)
    for pair in pairs:
        a, b = pair
        ret = cycleFromPair(a, b, g)
#print(cycleLengthDict)