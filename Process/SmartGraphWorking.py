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
        print(triple)
        x, y, z = triple
        if x == a or x == b:
            edgesFromPair.append((y, z))
        elif y == a or y == b:
            edgesFromPair.append((x, z))
        elif z == a or z == b:
            edgesFromPair.append((x, y))

    graph = {i: [] for i in range(max((max(pair) for pair in edgesFromPair), default=0) + 1)}
    for edge in edgesFromPair:
        graph[edge[0]].append(edge[1])
        graph[edge[1]].append(edge[0])
    
    #print(graph)
    allCycles = find_cycles(graph)
    #print("All Cycles = ", allCycles)
    
    #for cycle in allCycles:
        #cyDict[len(cycle)] += 1
    #print(cycleLengthDict)
    return max((len(cycle) for cycle in allCycles), default=0)


#pairs=[]
##cycleLengthDict = defaultdict(int) #length: num 
#for a in range(25, 0, -1):
#    for b in range(1, 26):
#        if a!=b:
#            pairs.append((a, b))
##print(pairs)
#    for pair in pairs:
#        a, b = pair
#        ret = cycleFromPair(a, b, g)
#print(cycleLengthDict)