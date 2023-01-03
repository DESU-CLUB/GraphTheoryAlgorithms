'''
Edmond Karp algorithm

Ford Fulkerson with BFS

Time complexityO(VE**2)

Does not depend on capcity value of edge
Strongly polynomial

repeatedly finds shortest augmenting path
 - impt as DFS uses long windy paths, 
    -longer the path, smaller bottleneck value
    -longer runtime

DO BFS from source to sink

maxx flow = sum of bottleneck values
'''

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

def BFSUtil(g,v,s,t,flow,vtoken,queue,prev): #Edmond Karp => Ford Fulkerson algorithm with BFS
    if s == t:
        return flow

    for edge in g[s]: #adds  children to queue if they satisfy req: still have capacity left for more flow, not visited already
        if edge.remain()>0 and v[edge.child] != vtoken and edge.child not in queue:          
            queue.append([edge.child,edge])
    if queue:#If more thingsin queue, pop and recursively do BFS
        node,edge = queue.pop(0)
        v[node] = vtoken#mark as visited
        prev[node] = edge#this is to record all previous nodes for augmenting
        '''
        why not use recursive backtrack, instead of prev?
            -> when backtracking, no way to get previous edge that led to current edge
            --> eg node 4 has children nodes 5 and 6, both are valid
            --> 4 leads to 5, 
            --> 5 leads to 8
            --> In node 8, next node is popped, which is 6
            --> 6 leads to sink
            --> 6 correctly augments
            --> But if u backtrack recursively, you're now in node 8, not part of the augmenting path
        
        '''
        bottleneck = BFSUtil(g,v,node,t,min(flow,edge.remain()),vtoken,queue,prev)
        '''
        Undoc this snippet of code for an example of recursive backtracking unable to handle the augmenting
        if bottleneck != None:
            print(edge.parent,edge.child)
        '''
        return bottleneck
            
def BFSIterative(g,v,s,t,vtoken,queue,prev): #This is the iterative version of above
    v[s] = vtoken
    queue.append(s)
    while queue: #continue to pop while queue has item 
        node = queue.pop(0)
        if node == t: #break off if item is sink
            break
        for edge in g[node]: #run requirements and add edges that satisfy to queue
            if edge.remain()>0 and v[edge.child] !=vtoken and edge.child not in queue:
                v[edge.child] = vtoken#mark as visited
                prev[edge.child] = edge#record edge as the prev edge for its child, this will help us backtrack for augmentation later
                queue.append(edge.child) #append child to queue
    if prev[t] == -1: #if path to sink not found, return 
        return None
    bottleneck = float('inf') #we start off with infinity, and we compare values of nodes in augmenting path to find smallest remaining capacity
    node = t
    while prev[node] !=-1: #find bottleneck
        bottleneck = min(bottleneck,prev[node].remain())
        node = prev[node].parent
        
    node = t
    while prev[node] !=-1:#augment by bottleneck
        prev[node].augment(bottleneck)
        node = prev[node].parent
    return bottleneck



def Edmond_Karp(g,s,t):
    vtoken = 1
    v = [0]*len(g)
    flow = float('inf')
    maxflow = 0
    while True:#For edmond karp, keep on finding augmenting paths until no more found
        queue = []
        prev=  [-1]*len(g)
        f = BFSUtil(g,v,s,t,flow,vtoken,queue,prev)
        if f == None:#this signifies no more paths to sink found
            break
        maxflow+=f#add flow to max flow
        vtoken+=1
        node = t
        while prev[node] != -1:#start from end to start of path, augmenting all flows and residuals
            prev[node].augment(f)
            node = prev[node].parent
    return maxflow

print(Edmond_Karp(g,0,7))

def Edmond_Karp_I(g,s,t):
    vtoken = 1
    v = [0]*len(g)
    maxflow = 0
    while True: #repeat until no more augmenting paths
        queue = []
        prev = [-1]*len(g)
        f = BFSIterative(g,v,s,t,vtoken,queue,prev)
        if f == None:
            break
        maxflow+=f
        vtoken+=1
    return maxflow


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





print(Edmond_Karp_I(g,0,7))
        




    