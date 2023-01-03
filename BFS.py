'''
Breadth First Search
explores nodes and edges breadth first
runs with time complexity O(V+E)

BFS useful for finding shortest path on unweighted graph

Algo:
Starts at arbitrary node
explores neighbour nodes first before moving to next level neighbours
i.e. it explores around it before travelling to next node

maintains q of which node it should visit next
so adds all of neighbours to queue first

if node already in queue, skip adding it into queue again
'''

#My implementation of BFS
queue = [] #queue to check what nodes are supposed to be visited after cur node

g = {0:{1:False,2:False},1:{0:False, 2:False,3:False},2:{0:False,1:'False'},3:{}}
path = [None]*len(g) #This path puts parent node at index of child node
visited = [False for i in range(len(g))] 
def BFS(start,g,queue,visited,path): #Need to use visited, in case we add nodes that are already visited yet connected to unvisited node
    if visited[start]: #If visited before, skip
        return
    visited[start] = True #Else mark 
    neighbours = g[start] #Find itself in adj list
    for neighbour in neighbours: #For each neighbour
        if neighbour not in queue and not visited[neighbour]: #if neighbiur not visited/in queue
            queue.append(neighbour) #Add neighbour to queue
            path[neighbour] = start #For reconstructing pth later, 
        #so when backtracking, path[e] leads to parent node

        #This adding of parent node done when enqueing
        #Because if done at dequeuing,
        #Will cause child node to identify parent node wrongly,or will not
        #identify first parent node that enqueued it correctly
    print ('Current Node: %d'%start)
    if queue:#If queue still has any more nodes, traverse
        next_node = queue.pop(0) #next_node is first node in queue, FIFO
        BFS(next_node,g,queue,visited,path)  #This ensures number is kicked out of queue once traversed

def MakePath(s,e,path):
    shortest_path = [] #list for recording shortest path 
    cur = e #start from end
    while cur != None: #While its not None (means either end not in same component as start)
    #while statement also is for handling when start is reached from end, then terminate
        shortest_path.append(cur) #append index (current node)
        cur = path[cur] #backtrack to parent node in shortest path until start is reached
    shortest_path = list(reversed(shortest_path)) #Flip this because we started from end
    if shortest_path[0] == s: #In case graph is disjoint, cannot reach node s
        print(shortest_path)
    else:
        print([]) #No possible path
BFS(0,g,queue,visited,path)
MakePath(0,3,path)
#Implementing for shortest path

