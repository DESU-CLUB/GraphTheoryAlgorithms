'''
Max Flow Ford Fulkerson Algorithm

For network flow

Max flow issue: With infinte input source, how much "flow" can we push through network
given that each edge has certain capacity?

Give a source and sink.

Edges have flow value: How many units of flow passing through edge
Edges also have capacity
2 special nodes: Source and Sink: S and T respectively

Can be used where edges are roads, pipes etc
It is the bottleneck value for flow that can pass through network from source to sink
under all constraints.

Max flow is sum of flows entering sink node

Flow graph: Directed fraph that has certain capacity
Can receive certain amount of flow

Flow running through must be less than equal to capacity

Each edge in flow graph has certain flow and capacity specified by fraction adjacent to each edge
Flow through each edge is 0 (at start), capacity is a non negative value

To find maximum flow (and min-cut),

Ford Fulkerson method repeatedly finds augmenting paths through residual graph
and augments flow until no more augmenting paths found


Augmenting path is path of edges in residual graph with unused capacity greater than zero from source s to sink t

Every augmenting path will have bottleneck (smallest edge in graph)
Bottleneck is smallest remaining capacity: ie capacity - current flow
Use bottleneck value to augment flow along path

Augmenting flow -> Updating flow values along augmenting path

for forward edges, we increase the flow by the bottleneck value
For backward edges, need to decrease the flow along each residual edge by bottleneck value

These edges exist to "undo" bad augmenting paths which do not lead to max flow

Think of every original edge having a residual edge that is not shown
residual graph is the graph that contains residual edges

Remaining capacity of edge is its capacity - flow

Sum of bottlenecks found in each augmenting path = max flow

Time complexity depends on how we find augmenting paths
 -> DFS method: O(f*E), f is maxflow

 If middle edge is 1 and DFS uses middle edge, we iterate 200 times as 1 is always bottleneck value

Faster max flow methods:
    Edmonds-Karp: O(E**2*V)
    Capacity Scalig O(E**2*log(u))
    Dinic's algorithm: O(V**2*E)
    Push relabel: O(V**2*E) or O(V**2*sqrt(E))

To add residual edges: Each residual edge is the reverse of edge with capacity of 0
'''

graph = [[0,10,10,0,0,0],
         [0,0,0,25,0,0],
         [0,0,0,0,15,0],
         [0,0,0,0,0,10],
         [0,0,0,0,0,10],
         [0,0,0,0,0,0]]
#Graph shows remaining capacity in each path
#Thus when residual paths are made, we add bottleneck to indicate paths that are open for flow to redirect
#When paths are filled, we reduce by the flow (bottleneck) to indicate remaining capacity has reduced
#We add and reduce by flow (found by doing DFS first to find smallest capacity/remaining capacity)
#as any redirection or adding of flow is limited by smallest capacity
#Since remaining capacity maintained in graph, even if we run same path,
#bottleneck will be different and thus flow will also change


def ford_fulkerson(g,s,t):
    max_flow = 0
    v = [0]*len(g)
    visited_token = 1 
    while True:
        f = dfs(g,v,s,t,float('inf'),visited_token)#Keep running to search for paths 
        if f == None: #check if function returned nth: i.e. no paths
            break
        max_flow+=f#Max flow is sum of all paths bottleneck
        visited_token+=1 #we change vtoken so that we dont reinitiailise entire list
    return max_flow 

def dfs(g,v,s,t,flow,vtoken):
    if s == t:
        return flow
    v[s] = vtoken #basically insteadof re_init the list to False every time, we just change 1 number
    for child,capacity in enumerate(g[s]):
        if  capacity>0 and v[child] != vtoken:
            bottleneck = dfs(g,v,child,t,min(flow,g[s][child]),vtoken)
            #Basically compare current remaining capacity and last known smallest capacity, update flow if needed
            if bottleneck !=None: #Backtrack and propagate values: Basically once smallest remaining capacity found
                g[s][child]-=bottleneck #Reduce capacity of forward edges by bottleneck
                g[child][s]+=bottleneck #Increase capacity of backward edges by bottleneck
                #Rationale of backward edges: So as to allow for rerouting of current flow to other nodes to augment path again
                return bottleneck

print(ford_fulkerson(graph,0,5))
m = [[0,5,7,9,0,0,0,0],
    [0,0,0,0,12,0,0,0],
    [0,0,0,0,0,20,15,0],
    [0,0,0,0,0,0,30,0],
    [0,0,0,0,0,0,0,15],
    [0,0,0,0,0,0,0,12],
    [0,0,0,0,0,0,0,12],
    [0,0,0,0,0,0,0,0]]

print(ford_fulkerson(m,0,7))