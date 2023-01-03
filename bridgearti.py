'''
Bridges and articulations
    - Bridge/cut edge: edge whose removal disocnnect graph
    - Articultion point/cut vertex: Node ingraph whose removal increases no
    of connected components

    Impt as they hint at weak points



Bridges algo:
DFS
label nodes with increasing id
keep track of id and smallest low link
bridges are found where id of node edge coming from <
low link value of node edge is going to

low link val: smallest id reachable from that node


why if low link val of next node > current node id, means bridge?
-> Because if low link val of next node > cur id,
means that next node does not have a cycle back to cur id

Original algo
one DFS to label all nodes

V more DFS to find all low link values

O(V(V+E))

One pass version is
O(V+E)

'''
g = {0:{1:3,4:0},1:{0:1,2:1,3:0},2:{3:0},3:{1:0},4:{0:0}}

v = [False]*len(g)
lowlink = {}
bridges = []
nodeids = [-1]*len(g)
#one pass method
#only works if root is origin node, else it finds for subgraph
def find_bridge(g,v,s,nodeids,bridges,lowlink,parent,nodeid = 0):
    v[s] = True #mark as visited
    nodeid = max(nodeids)+1 #if neighbour not visited means not recorded yet, so can assign node
    if s not in nodeids: #assign node an id if not given 1 yet
        nodeids[s] = nodeid 

    lowlink[s] = nodeid #initial lowlink val is its node id

    for neigh in g[s]: #check all neighbours
        if neigh == parent: #skip if parent is connected edge, as for undirected edges we treat as singular edge, so taking it out negates both to and fro
            continue #this will affect result as it will think its connected to id < lowlink value and update
        if not v[neigh]: #if neighbour doesnt have id, give it one
            parent = s
            neighid = nodeid


            find_bridge(g,v,neigh,nodeids,bridges,lowlink,parent,nodeid) #do children nodes first
            #this propagates low link values in cycle
            neighlink = lowlink[neigh] #for current child node, get its lowlink val

            if lowlink[s]  > neighlink: #if lowlink val is > neighbours
                lowlink[s] = neighlink #means in a cycle as neighbour should have increasing lowlink val if not in cycle

            if nodeids[s] < neighlink: #if lets say not in cycle, and id < lowlink, means it continues on and is a bridge
                bridges.append([s,neigh])

        #this is as all children is checked already, if lowlink still bigger, means its a bridge as no cycle for all children node

        else: 
            neighid = nodeids[neigh] #else give it its own id
            if neighid < lowlink[s]: #if neighbour id < lowlink val at s
                lowlink[s] = neighid #means in cycle, so lowlink updated to smallest val
            #if neighbour visited, then you want to check if neighbours id is less than lowlink val
            #if neigh was visited before, it is connected to another node somewhere
            #cannot be bridge so can just focus on checking if can update lowlink
        
        
def find_bridges(g,v,nodeids,bridges,lowlink):
    for i,j in enumerate(v):
        if not j:
            find_bridge(g,v,i,nodeids,bridges,lowlink,-1)
    print(nodeids,lowlink)

            

find_bridges(g,v,nodeids,bridges,lowlink)

print(bridges)

'''
Find articulation points

On connected component with >=3 v

if u,v is bridge, either u or v is articulation point

but thee are more conditions

can have arti point but no bridge

has to do with cycles
presence of cycle means original node is arti point

so lowlink can find arti point

exception is if node chosen has 0 or 1 outgoing directed edge
then it is not articulation point

if >2 outgoing edge, cycle becomes articulation point
'''
g = {0:{1:1,2:0},1:{0:0,2:1},2:{1:1,0:0}}

v = [False]*len(g)
lowlink = {}
artipoint = []
nodeids = [-1]*len(g)
def arti_point(g,v,s,lowlink,artipoint,nodeids,parent,root,out,nodeid = 0):
    if parent == root: #only if parent == root then add to outgoing edges
        out+=1 
        '''
        even if more than 2 edges outgoing in adj list, 
        if edge has been visited before it was visited by root
        it will not be considered an outgoing edge as the undirected edge was "transformed"
        into an edge ingoing to root

        eg 0 and 1, 0 and 3 undirected edge, 1 inevitably leads to 3
        so 3 to 0 is now considered ingoing, we do not consider 0-3
        hard to update adj list, so instead the code below marks 3 as visited, 
        so that when root visits child,instead of dfs which will increase outgoing,
        will just check the lowlink values

        Furthermore, 3 will not visit 0 as 0 is visited already

        Also, this outgoing edges also works as a condition for checking if connected component
        <3 vertices, then not articulaton point if bridge, as if  only 2 vertices, outgoing will alwasy be less than 2
        '''
    v[s] = True
    nodeid = max(nodeids)+1
    nodeids[s] = nodeid
    lowlink[s] = nodeid
    for child in g[s]:
        if child == parent:
            continue
        if not v[child]:
            parent = s
            neighid = nodeid
            out = arti_point(g,v,child,lowlink,artipoint,nodeids,parent,root,out,neighid)
            if lowlink[s] > lowlink[child]:
                lowlink[s] = lowlink[child]
            if nodeids[s] == lowlink[child] and s not in artipoint: #check if current node id is same as lowlink  
                artipoint.append(s)#then add to arti point: why? because this means that this is the start of the cycle
            if nodeids[s] < lowlink[child] and s not in artipoint:
                artipoint.append(s) 
        else:
            lowlink[s] = min(lowlink[s],nodeids[child])
    return out
   

def arti_points(g,v,lowlink,artipoint,nodeids):
    for i,j in enumerate(v):
        if not j:
            out = arti_point(g,v,i,lowlink,artipoint,nodeids,-1,i,0,0)
            if i in artipoint and out<2:
                artipoint.remove(i) #check for exception which is root
arti_points(g,v,lowlink,artipoint,nodeids)
print(artipoint)
