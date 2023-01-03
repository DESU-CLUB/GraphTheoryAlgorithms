'''
DFS: Search algorith to explore nodes and edges of graph
Time complexity O(V+E)
Usually used as building block for other algos

Usually modified to solve problems


Basic DFS goes depth first, until cannot go further, then backtracks and continue

Goes depth first
Once all child nodes visited, add to list of visited
backtrack
if dead end reach, mark as visited
backtrack

if visiting parent node via child node, back track all the way to parent node, add all to visited
'''
#Variables in global

g = {0:{1:False,2:False},1:{0:False},2:{0:False},3:{}}# adjacency list repr graph
n = len(g) #no of nodes in graph
visited =[False for i in range(n)]

def properDFS(start,g,visited,components): #Proper DFS
    if visited[start]: #So that if visited, it skips 
        return #Checks itself for visited
    else:
        components.append(start) #Append itself to its component: i.e. list recording nodes linked to each other
        visited[start] = True #Mark itself as true
    neighbours = g[start] #Finds its set of neighbours in adj list
    for i in neighbours: #this loops through all neighbours depth first
        properDFS(i,g,visited,components) #recurseively call on child nodes until dead end/visited before
    print(start)




visited =[False for i in range(n)]
#properDFS(1,g,visited)
        
#DFS can be used to id each component of disconnected graph
#Algo: DFS at every node unless visited, give each same connected same id
def findComponents(g,visited):
    count = 0
    components = {}
    for i in range(len(g)):
        if not visited[i]:
            count+=1
            components[count] = []# Video implemented as list where 
                                  #Index referred to each graph node, and
                                  #value is which component they belong to
            #I implemented it as a hashmap
            properDFS(i,g,visited,components[count])
    return components
        
    
visited =[False for i in range(n)]
print(findComponents(g,visited))


















'''
def DFS(start,g,visited,count): #What i implemented: WRONG
    visited[start] = True
    for i in g[start]:
        if not visited[i]: #Checks neighbours before applying DFS
                            #If neighbour is revisited as called from outside function
                            #Will still run depth first search instead of returning false
            DFS(i,g,visited,count)
    print(start,count)

    
def DFSconnected(start,g,visited):
    count = 0
    DFS(start,g,visited,count)
    for i in range(len(visited)):
        if not visited[i]:
            count+=1
            DFS(i,g,visited,count)

visited =[False for i in range(n)]
DFSconnected(0,g,visited)
'''