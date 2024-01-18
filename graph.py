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
    alphabet = "abcdefghijklmnopqrstuvwxyz"
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
    return max(len(cycle) for cycle in allCycles)

#b = [ {0, 1, 2}, {0, 3, 4}, {0, 5, 6}, {0, 7, 8}, {0, 9, 10}, {0, 11, 12}, {0, 13, 14},
#{3, 8, 10}, {1, 8, 11}, {1, 7, 9}, {1, 4, 6}, {1, 12, 14}, {1, 10, 13}, {1, 3, 5},
#{4, 9, 13}, {2, 9, 12}, {2, 8, 14}, {2, 11, 13}, {2, 4, 5}, {2, 3, 6}, {2, 7, 10},
#{5, 11, 14}, {5, 7, 13}, {3, 12, 13}, {3, 9, 14}, {3, 7, 11}, {4, 7, 14}, {4, 8, 12},
#{6, 7, 12}, {6, 10, 14}, {4, 10, 11}, {5, 10, 12}, {6, 8, 13}, {5, 8, 9}, {6, 9, 11} ]
#cycleFromPair(6, 14, b)
#print(max((1,2)))