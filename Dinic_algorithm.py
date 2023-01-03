'''
Dinic's Algorithm
'''
from collections import defaultdict
class FlowEdge():
    def __init__(self,parent,child,capacity):
        self.flow = 0
        self.parent = parent
        self.child = child
        self.capacity = capacity
        self.residual = 0
    def augment(self,bottleneck):
        self.flow+=bottleneck
        self.residual.flow-=bottleneck
    def remain(self):
        return self.capacity - self.flow

def addEdge(graph,parent,child,capacity):
    e1 = FlowEdge(parent,child,capacity)
    e2 = FlowEdge(child,parent,0)
    e1.residual = e2
    e2.residual = e1
    graph[parent][child] = e1
    graph[child][parent] = e2

n = 8
g = [[0]*n for i in range(n)]
addEdge(g,0,1,5)
addEdge(g,0,2,7)
addEdge(g,0,3,9)
addEdge(g,1,4,12)
addEdge(g,2,5,20)
addEdge(g,2,6,15)
addEdge(g,3,6,30)
addEdge(g,4,7,15)
addEdge(g,5,7,12)
addEdge(g,6,7,12)

def BFS(g,s,t,level,queue): #Creates level graph
    queue.append(s)
    while queue:
        node = queue.pop(0)
        for edge in g[node]:
            if edge ==0:
                continue
            if edge.remain()>0 and edge.child not in queue and level[edge.child] == -1: #level records level graph amd acts as visited
                queue.append(edge.child)
                level[edge.child] = level[node]+1 #So that child node always 1 layer after parent node
    return level[t] != -1

def DFS(g,v,s,t,level,next,vtoken,flow): #Finds flow paths
    if s == t:
        return flow
    v[s] = vtoken
    while next[s]<len(next): #value of next[s] cannot be more than total no of nodes
        edge =g[s][next[s]] #points to next edge from s
        if  edge ==0 :#if edge is 0, we continue as no existing edge
            next[s]+=1
            continue 
        else:#we check if we should traverse to next node
            #should always advance in level graph, and not visited
            #capacity also >0
            if v[edge.child] !=vtoken and edge.remain()>0 and level[edge.child] > level[edge.parent]:
                bottleneck = DFS(g,v,edge.child,t,level,next,vtoken,min(flow,edge.remain()))
                if bottleneck != None:
                    edge.augment(bottleneck)#augment to update flow of edge and to update residual edges
                    return bottleneck #return so that all nodes can update
            next[s]+=1 #if it doesn't return, means dead end, so find another edge
            



def Dinic(g,s,t):
    '''
    Sequence
    BFS for level graph
    reset queue (dont reset level as needed by DFS)
    DFS through level graph until stopping flow is found
    repeat until no more level graph to sink
    
    '''
    level = [-1]*len(g)
    maxflow = 0
    queue = []
    vtoken = 1
    v = [0]*len(g)
    while BFS(g,s,t,level,queue): #BFS constructs level graph until no more found
        queue = [] 
        next = [0]*len(g) #next shows next node to go to for all vertices
        flow = float('inf') #this is the flow for DFS
        while True:
            f = DFS(g,v,s,t,level,next,vtoken,flow) #Once no more flow for level graph, redo level graph and repeat until no more graphs can be made
            if f == None:
                break
            maxflow+=f #accumulate flow, as max flow is sum of all bottlenecks
        level = [-1]*len(g)
    return maxflow

                
print(Dinic(g,0,7))
