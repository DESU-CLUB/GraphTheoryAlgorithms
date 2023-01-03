'''
Eulerian Path is a path of edges that visits all edges exactly once

Not every path has an eulerian path
Some graphs only have eulerian path on specific nodes

Condition for eulerian path:
Undirected graphs: Either every vertex has even degree or
                   exactly two vertices have odd degree

Directed graph: At most 1 vertex has (outdegree) - (indegree) = 1 
                and at most one vertex has (indegree) - (outdegree)= 1
                All other vertices have equal in and out degrees

Eulerian circuits
 -> Path which starts and ends on same vertex
 You can start anywhere for graphs with eulerian circuits


Eulerian circuit  conditions:
 Undirected graph: Every vertex has an even degree
 Directed Graph: Every vertex has equal indegree and outdegree

Undirected graphs:
Node degree is how many edges connected to it

Directed graphs:
Outdegree: edges going out
indegree: edges going in

Finding eulerian path
1) Check if eulerian path exists
2) At most one vertex has outdegree - indegree = 1 and one vertex has indegree - outdegree = 1

Need to force DFS to visit all edges of graph
When no more unvisited outgoing edges, we backtrck and add current node to solution

Time complexity is O(E)

'''

g = {
    0:{},
    1:{2:1,3:3},
    2:{2:2,4:[1,3]},
    3:{1:2,2:1,5:4},
    4:{3:2,6:1},
    5:{6:1},
    6:{3:2}
}

def pathchecker(g):
    inout = {i:{'in':0,'out':0} for i in g}
    #first element of dict in number of ins, second element of list is number of outs
    for node in g:
        for child in g[node]:
            if type(g[node][child]) == int:
                val = len([g[node][child]])
            else:
                val = len(g[node][child])
            
            inout[node]['out']+=val
            inout[child]['in']+=val
    print(inout)
    
    outvertex = []
    invertex = []
    for node in inout:
        if inout[node]['out']- inout[node]['in'] == 0:
            continue
        elif inout[node]['out']- inout[node]['in'] == 1: #More outdegree than in
            outvertex.append(node)
        elif inout[node]['out']- inout[node]['in'] == -1: #More indegrees
            invertex.append(node)
        else:
            return False
    if not( (len(invertex) == 0 and len(outvertex) == 0) or (len(invertex) == 1 and len(outvertex) == 1)):
        return False
    outv = False if not outvertex else outvertex[0]
    inv = False if not invertex else invertex[0]
    return (True,outv,inv)
    
def setup(v):
   for i in g:
    v[i] = {}
    for j in g[i]:
        if type(g[i][j]) == int:
            v[i][j] = False
        else:
            v[i][j] = [False for i in g[i][j]]


def DFSPath(g,v,s,path):
    for child in g[s]:
        if v[s][child] == False:
            v[s][child] = True
            DFSPath(g,v,child,path)
        elif type(v[s][child]) == list:
            for i in range(len(v[s][child])):
                if v[s][child][i] == False:
                    v[s][child][i] = True
                    DFSPath(g,v,child,path)
                    break

    path.insert(0,s)

        
        
sg= {0:{1:1},
    1:{2:1,3:1},
    2:{1:1},
    3:{4:2},
    4:{}
    }

def findStart(g):
    for i in g:
        if len(g[i])>0:
            return i


def edgecount(g):
    edges = 0
    for node in g:
        for child in g[node]:
            edges += len(g[node][child]) if type(g[node][child]) == list else 1
    return edges

def eulerpath(g):
    if edgecount(g) == 0:
        print('No path')
        return
    exists,start,end = pathchecker(g)
    if start == False:
        start = findStart(g) #Since pathfinder checks for unique starting node
        #We just need to find non singleton here

    path = []
    v = {}
    setup(v)
    if exists:
        DFSPath(g,v,start,path)
        if len(path) == edgecount(g)+1: #In case of disconnected graphs
            print(path) #Number of edges+1 is because our path is no of vertices, which is no of edges +1
    else:
        print("No Path")


eulerpath(g)

