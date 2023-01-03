'''
Capacity scaling

IDea: priortise edges with larger capacities first

adjust size of each edge based on capacity value

Let U be value of largest edge capacity
Let delta be largest power of 2 <= U
Heuristic
Only take edges whose remaining capacity is >= delta in order to achieve better runtime

Repeatedly find augmenting paths with remaining capacity >=delta
until no more paths

decrease value of delta by half
while delta >0

Works very well in practice

capacity scaling is O(E**2log(U)) if DFS used
O(EVlog(U)) if BFS used
'''
import math

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
    graph[parent].append(e1)
    graph[child].append(e2)

n = 8
g = [[]for i in range(n)]
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

def highestPowerof2(n): #Finds highest power of 2 that is closest to current largest remaining capacity
    return 2**int(math.log2(n))


def capacityScalingDFS(g,s,t): #DFS version of capacity scaling
    maxCapacity = 0
    flow = float('inf')
    vtoken = 1
    v = [0]*len(g)
    maxflow = 0
    for i in g: 
        for j in i: #Finds largest capacity within entire graph
            if j.capacity>0 and highestPowerof2(j.capacity)  > maxCapacity:
                maxCapacity = highestPowerof2(j.capacity) 
    delta = maxCapacity
    while delta >0:#this part is the capacity scaling logic, where we keep dividing by 2 until delta is 0 (no more augmenting paths found)
        while True:
            f = scalingDFS(g,v,s,t,flow,vtoken,delta)#keep on finding augmenting paths which have remaining capacity>=delta
            if f == None: #break if no more augmenting paths
                break
            maxflow+=f
            vtoken+=1
        delta //=2 #halve delta, now anything >=delta is considered in next iteration of DFS
    return maxflow

def scalingDFS(g,v,s,t,flow,vtoken,delta): #DFS helper for capacity scaling (DFS)
    if s == t:#terminate and backtrack once sink found
        return flow
    v[s] = vtoken
    for edge in g[s]: #similar to ford-fulkerson, find edges that meet requirement, and then traverse to those child nodes
        if v[edge.child] != vtoken and edge.remain()>=delta: 
            #capacity scaling puts a limit on how much remaining capacity edge should have to be selected
            bottleneck = scalingDFS(g,v,edge.child,t,min(flow,edge.remain()),vtoken,delta) #traverse to child, here we compare values of flow with remaining capacity
            #this will help us get the bottleneck value: smallest remaining capacity in path from source to sink
            if bottleneck != None:
                edge.augment(bottleneck) #do augmentation for nodes inpath
                return bottleneck

print(capacityScalingDFS(g,0,7))
        


def capacityScalingBFS(g,s,t):
    '''
    Everything is similar to DFS version, does backtracking and augmenting outside of helper function
    '''
    maxCapacity = 0
    flow = float('inf')
    vtoken = 1
    v = [0]*len(g)
    maxflow = 0
    for i in g: #find max capacity
        for j in i:
            if j.capacity>0 and highestPowerof2(j.capacity)  > maxCapacity:
                maxCapacity = highestPowerof2(j.capacity) 
    delta = maxCapacity
    while delta >0:#logic of capacity scaling
        while True: #repeat until no more augmenting path
            queue = []
            prev = [-1]*len(g)
            f = scalingBFS(g,v,s,t,queue,prev,flow,vtoken,delta)
            if f == None:
                break
            maxflow+=f
            vtoken+=1
            node = t
            while prev[node]!=-1: #backtrack to augment paths
                prev[node].augment(f)
                node = prev[node].parent
        delta //=2
    return maxflow

def scalingBFS(g,v,s,t,queue,prev,flow,vtoken,delta):
    if s == t:
        return flow
    
    for edge in g[s]: #add child to queue if it meets requirements
        if edge.remain()>delta and v[edge.child]!=vtoken and v[edge.child] not in queue:
            queue.append([edge.child,edge])
    if queue:
        node,edge = queue.pop(0)
        prev[node] = edge
        v[node] = vtoken
        bottleneck = scalingBFS(g,v,node,t,queue,prev,min(flow,edge.remain()),vtoken,delta)
        #traverse to child, here we compare values of flow with remaining capacity
        #this will help us get the bottleneck value: smallest remaining capacity in path from source to sink
        return bottleneck
    
       

n = 8
g = [[]for i in range(n)]
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
print(capacityScalingBFS(g,0,7))