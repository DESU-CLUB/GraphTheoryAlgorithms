'''
Bellman-Ford

shortest path

SSSP algoirithm

find shortest path from one node to other node

not ideal for most SSSP as time complexity of O(EV)

Time complexity of Bellman Ford
- O(V*E)

beter to use Djikstra: O(log(E+V))

use BF if Djiksta fails, if thereis negative edge weight+cycle

E: edges
V: vertices
S: id
D: array of size V

set D elements to + inf

D[S] = 0
relax each edge v-1 time
because you are not interested in start node

Nodes dont need to be process in any order

Why iterate v-1 times?: 
Cycles may not be detected on first run, so need multiple runs

n-1  is the maximal length of a shortest path in the graph. 
After k iterations of the Bellman-Ford algorithm, you know the 
minimum distance between any two vertices, when restricted to paths of length at most k
'''
g = {0:{1:5,2:3},1:{3:3,4:1},2:{3:3,4:2},3:{},4:{}}

def BF(g,s):
    dist = [float('inf')]*len(g)
    dist[s] = 0
    negcycle = []
    for j in range(len(g)-1): #iterate v-1 times
        for i in range(len(g)):
            for neigh in g[i]:
                newdist = dist[i]+g[i][neigh] #
                if newdist < dist[neigh]:
                    dist[neigh] = newdist

    #Repeat to find neg cycle, as above finds shortest path already
    for j in range(len(g)-1):
        for i in range(len(g)):
            for neigh in g[i]:
                newdist = dist[i]+g[i][neigh]
                if g[i][neigh] <0 and [i,neigh] not in negcycle:
                    negcycle.append([i,neigh]) #Finds directly involved nodes in neg cycle

                if newdist < dist[neigh]:
                    dist[neigh] = -float('inf') #Update neg cycles to -inf
                    #Take note that nodes not directlyinvolved but along the path of the -ve cycle are also -inf
    return (dist,negcycle)
print(BF(g,0))

g = {0:{1:4,2:1},1:{3:1},2:{1:2,3:5},3:{4:3},4:{}}

print(BF(g,0))
 
 #Adding neg cycles
g =  {0:{1:4,2:1},1:{1:-1},2:{1:2,3:5},3:{4:3},4:{}}
print(BF(g,0))
    