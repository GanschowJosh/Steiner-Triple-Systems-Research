from collections import defaultdict


class Graph:
    def __init__(self, vertices):

        #number of vertices
        self.V = vertices

        #default dictionary to store graph
        self.graph = defaultdict(list)

    #function to add an edge
    def addEdge(self, v, w):
        #add w to v_s list
        self.graph[v].append(w)

        #add v to w_s list
        self.graph[w].append(v)
    

    #Recursive function that uses visited[] and parent to
    #detect cycle in subgraph reachable from vertex v.
    def isCyclicUtil(self, v, visited, parent):
        #mark the current node as visited
        visited[v] = True

        #recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            #if node is not visited then recurse on it
            if visited[i] == False:
                if(self.isCyclicUtil(i, visited, v)):
                    return True
            #if an adjacent vertex is visited and not parent
            #of current vortex, then there is a cycle
            elif parent != i:
                return True
        return False
    
    def isCyclic(self):
        #mark all the vertices as not visited
        visited = [False] * (self.V)

        #call the recursive helper
        #function to detect cycle in different DFS trees
        for i in range(self.V):
            #don't recur for u if it is already visited
            if visited[i] == False:
                if(self.isCyclicUtil(i, visited, -1)) == True:
                    return True
        return False
    

'''g = Graph(5)
g.addEdge(1, 0)
g.addEdge(1, 2)
g.addEdge(2, 0)
g.addEdge(0, 3)
g.addEdge(3, 4)

if g.isCyclic():
    print("Graph contains cycle")
else:
    print("Graph doesn't contain cycle")
g1 = Graph(3)
g1.addEdge(0, 1)
g1.addEdge(1, 2)
if g1.isCyclic():
    print("Graph contains cycle")
else:
    print("Graph doesn't contain cycle")
'''