'''
Directed Acyclic graphs
    -> graph with directed edges and no cycles

Single Source ShortestPath on DAG can be solved in O(V+E)
-> does not care abt -ve edge unlike djikstra
use topsort and process sequentially

How does it work

it travels through every edge and vertex in top order
--> if value < dist[i],update else ignore
--> this allows it to find smallest cost
'''
g = {0:{1:5,2:3},1:{3:3,4:1},2:{3:3,4:2},3:{},4:{}}

def topsort(g):
    v= [False]*len(g)
    toplist = []
    for i in range(len(v)):
        if v[i] != True:
            dfs(g,v,i,toplist)
    return toplist

def dfs(g,v,s,toplist):
    if v[s]:
        return
    v[s] = True
    for neighbour in g[s]:
        dfs(g,v,neighbour,toplist)
    toplist.insert(0,s)

print(topsort(g))

def sp(g,toplist): #find shortest path
    dist = [float('inf')]*len(g) #init distance
    dist[0] = 0 #start node dist = 0
    for i in toplist: #for all vertices in topsort
        for j in g[i]: #for all edges
            ndist = dist[i]+g[i][j] #find new dist
            if ndist < dist[j]: #if new dist is shorter than current, update
                dist[j] = ndist
    return dist#print distance array

sp(g,topsort(g))

'''
DAG Longest Path

multiply all edge values by -1, find shortest path
then multiply all edge values by -1 again

'''

alt_g = {i:{k:-v  for k,v in g[i].items()} for i in g }

print(g[0].items())

print(alt_g)
d = sp(alt_g,topsort(g))
print('longest path is :',list(map(lambda x: x*-1,d)))