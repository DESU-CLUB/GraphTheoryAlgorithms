'''
Tarjan Algorithm for SCC

strongly connected components (SCC)

-> self contained cycles where every vertex in a cycle can reach all verrtices in same cycle
-> unique within a direced graph
Low link value: Smallest node id reachable from node when doing DFS

Using Low Link value for SCC depends on where DFS starts

Might not end up with correct ids, as other SCCs interfere with each others low link value

Tarjan uses stack invariant: a set of valid nodes to update lowlink values from
Nodes added to stack as theyre explored first time
removed from set each time SCC completed

Low link update condition
 -> to update node u's low link value to node v (if v lowlink < u lowlink)
    1) need path of edged
    2) v must be on stack invariant

Tarjan complexity: O(V+E)
Update and find low link values on the fly to get linear complexity

1) Mark all nodes as unvisited
2) Start DFS, assign node id and lowlink val
3)Mark node as visited, add to seen stack
4) On DFS callback, if previous node on stack
    THEN MIN CUR NODE AND PREV NODE LOW LINK VALS*
5) After all neighbours visited, if current node started a connected component
6)pop nodes until current node is reached

*allows low link values to propagate through cycles without interfering
**node started connected component if id = low link value


'''
from collections import defaultdict
class SetStack():
    def __init__(self):
        self.stack = []
    
    def push(self,item):
        if item not in self.stack:
            self.stack.append(item)
    
    def pop(self):
        return self.stack.pop()

    def __contains__(self,item):
        if item in self.stack:
            return True
        return False

    def __str__(self):
        return str(self.stack)

seen = SetStack()
g = {0:{1:0},1:{2:1},2:{0:1,3:0},3:{4:0},4:{5:0},5:{3:0},6:{6:0}}
nodeids = [-1]*len(g)
lowlinks = [-1]*len(g)
v = [False]*len(g)

def DFS(g,v,node,seen,nodeids,lowlink,parent):
    v[node] = True
    nodeid = max(nodeids)+1
    nodeids[node] = nodeid
    lowlinks[node] = nodeid
    seen.push(node) #Push node to seen stack, only update lowlink of parent if child in seen
    for child in g[node]:
        if parent == child: #Skip if parent = child for undirected graphs
            continue
        if v[child] == False: #if child not visited
            DFS(g,v,child,seen,nodeids,lowlink,node) #visit it
            if child in seen: #on callback, if child in same scc, propagate lowlink value
                lowlinks[node] = min(lowlinks[child],lowlinks[node])
        else:
            if child in seen: #if child is smaller than parent, update lowlink if child in seen
                lowlinks[node] = min(nodeids[child],lowlinks[node])
    if lowlinks[node] == nodeids[node]: #If lowlink value of node == node id (base of SCC)  
        data = seen.pop()  #pop every node in that SCC out
        print(seen,node,data)
        while data != node:
            data = seen.pop()


    



def optimDFS(g,v,node,seen,nodeids,lowlink,parent):
    v[node] = True
    nodeid = max(nodeids)+1
    nodeids[node] = nodeid
    lowlinks[node] = nodeid
    seen.push(node)
    for child in g[node]:
        if parent == child:
            continue
        if v[child] == False:
            optimDFS(g,v,child,seen,nodeids,lowlink,node)
        if child in seen:
            lowlinks[node] = min(lowlinks[node],lowlinks[child])
    if lowlinks[node] == nodeids[node]: #If lowlink value of node == node id (base of SCC)  
        data = seen.pop()  #pop every node in that SCC out
        while data != node:
            data = seen.pop()


def tarjan(g,v,node,seen,nodeids,lowlink):
    for node in g:
        if v[node] == False:
            optimDFS(g,v,node,seen,nodeids,lowlink,-1)

tarjan(g,v,0,seen,nodeids,lowlinks)
scc = defaultdict(list)
for idx,root in enumerate(lowlinks):
    scc[root].append(idx)
print(scc)