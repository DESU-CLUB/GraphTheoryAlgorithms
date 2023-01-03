'''
Topological Sort

Many real world situation can be modelled as 
graphs with directed edges where some events must occur before others

eg school class prerequisites, program dependencies
event scheduling
assembly instructions

Eg to take classH, must take class A and D , or class E, or class B and D

A topological ordering is where for each directed edge from A to B, A appears before B in the ordering

topsort can find top order in O(V+E)

top orderings are not unique

Not all direced graphs have ordering

must be acyclic

How to verify if graph does not contain direcred cycle
    --> use Tarjan's strongly connected component algo

All trees have topsort

topsort algo
-> Pick unvisited node
-> Begin DFS on selected node, exploring only unvisited nodes
-> On recursive callback of DFS, add node to top order in reverse order

Why add only after callback
 -> To ensure that node is only added once all of its child nodes have been added
'''

def toposort(g,v,s,topolist):
    if v[s]: #if visited,skip
        return
    v[s] = True #mark as visited
    neighbours = g[s] #get neighbouring nodes from adj list
    for node in neighbours:
        toposort(g,v,node,topolist) #recursively recall
    topolist = topolist.insert(0,s)
    #add element to front of list once all children added

    

g = {0:{1:5,2:3},1:{3:3,4:1},2:{3:3,4:2},3:{},4:{}}

def solve(g):
    visited = [False]*len(g) #init visited
    topolst = [] #list for toposort
    for i in range(len(visited)):
        if visited[i] != True: #keep on visiting until all nodes visited
            toposort(g,visited,i,topolst)

    return topolst


def altsolve(g,start):
    visited = [False]*len(g) #init visited
    topolst = [] #list for toposort
    toposort(g,visited,start,topolst)


    return topolst
 

print(altsolve(g,1))
print(solve(g))

