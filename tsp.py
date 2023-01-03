'''
TSP problem is NP complete
Difficult to find optimal solution

2 methods:
Use Brute force with permutations
Time complexity O(n!)
Use Dynamic Programming
O(n^2*2^n)
makes 23 nodes TSP feasible

Dynamic Programming  Algo
Find solution for subpath, use subpath to find optimal path for n+1 

1) Select starting node, 0<S<=N
2) Compute and store optimal value from S to each node X
    TSP of path 2 now solved
3) To compute the optimal solution of path length 3,
`a) Record set of visited nodes in subpath
 b) Index of last visited node in path
Since N possible nodes we could have visited last, and 2^N subsets
Space complexity is O(N*2^n)

This is stored in binary state (i.e. a 32 bit integer)
to save space, allow for easy caching

4) Take solved subpaths from n-1, as another edge extending to unvisited node
5) Complete TSP tour, connect tour back to S
Loop over end states in memo table for every possible end position
Miniminze Lookup value + cost of going back to S

Use adj matrix to solve



'''



import itertools

#---------------Brute Force Method------------------
g = [[0,4,1,9],
     [3,0,6,11],
     [4,1,0,2],
     [6,5,-4,0]  ]
nodes = [0,1,2,3]
permute = list(itertools.permutations(nodes))


minCost = float('inf')
minPath = []
for path in permute:
    cost = 0
    for node in range(1,len(path)):
        parent = node-1
        cost+=g[path[parent]][path[node]]
    cost+=g[path[node]][path[0]]
    if cost < minCost:
        minCost = cost
        minPath = list(path)
minPath.append(minPath[0])
print('________________Travelling Salesman Problem: Brute Force______________')
print(minPath,minCost)


#----------------Dynamic Programming Method-------------------------

g = [[0,4,1,9],
     [3,0,6,11],
     [4,1,0,2],
     [6,5,-4,0]  ]

def tsp(g,S): #graph and starting node
    N = len(g)

    #initialise memo table
    #Fill table with null values or +inf

    memo = [[float('inf') for i in range(2**N)] for j in range(N)]
    #memo is 2d table of size N by 2^N
    setup(g,memo,S,N)
    solve(g,memo,S,N)
    minCost = findMinCost(g,memo,S,N) #Our memo contains all solutions for all possible endstates (eg cost if graph ended at node 2, graph if cost ended at node 3)
    tour = findOptimalTour(g,memo,S,N)
    return (minCost,tour)

def setup(m,memo,S,N):
    for i in range(N):
        if i == S: #Skip if i is starting node, 
            continue #as we are calculating optimal path
        #Store optimal value from S to each node i
        #(given as input in the adj matrix)
        memo[i][1<<S|1<<i] = m[S][i]
    #Above snippet of binary manipulation
    #Just resolves to give binary state that represents
    #S and i has been visited
    #Additionally, we store this in m[i] as this is the
    # Optimal node to go to node i from S 

def combinations(r,N):  #Basically permutates all bitmaps, and returns a list of their integer form
    base = '1'*r+'0'*(N-r)
    return set(map(lambda x: int(''.join(x),2),itertools.permutations(base)))


def notIn(node,subset):
        return ((1<<node) & subset) == 0
        #Returns whether subset contains flipped bit representing node's position

def solve(m,memo,S,N):
    for r in range(3,N+1):#N+1 here because cannot miss out combinations(N,N), where all bits flipped to 1
        for subset in combinations(r,N):
            if notIn(S,subset): #If S not visited in subset, skip
                continue
            for next in range(N): #we iterate for next node, if subset has >2 nodes flipped
                                 # other than start, any one of the flipped nodes can be next node to go to, and the rest will be a subpath
                if next == S or notIn(next,subset):
                    continue
                #So skip if next node is start or next node is not visited in subset
                #Eg for 1011, if next is 1, we skip it as it is not visited in the graph
                #Then we only generate visiting the 2nd node or 3rd node next,
                #Using the states 1001 (0th and 3rd node visited)
                #or state 1010 (0th and 2nd node already visited)

                #Next, we want to find the subset state excluding next node
                #So that we can get result from our memoization
                #we do this by XOR the bit shift from next
                state = subset ^ (1<<next)
                minDist = float('inf')

                #e is end node
                for e in range(N): #We iterate through n so as to solve multiple subpaths in one loop
                    #because for same subset without next bit, 
                    #if more than 2 bits switched on, last node could be any one of the nodes that is not the start
                    #Also find which end node best optimizes the partial tour
                    if e == S or e == next or notIn(e,subset):
                        continue
                    #We skip if end node is start node or next node, or if e is not in subset
                    newDistance = memo[e][state] + m[e][next]
                    #memo[e][state] denotes from current optimal distance from previously ended node
                    #+m[e][next] adds distance from end node to next node to visit, using graph 
                    #So get subpath from memo, get new distance between last node to next node from graph

                    if (newDistance<minDist):
                        minDist = newDistance #See if current distance is less than previous minimum distance for current subset
                # then we take the minimum distance across same subset with diff end nodes to next node
                memo[next][subset] = minDist #records optimal distance of current state, given memo[next node][flipped state]
                    #So if nodes 0,1,2 visited, 2 was last node to visit,
                    #memo[2][0111]

def findMinCost(m,memo,S,N):
    END_STATE = (1<<N)-1 #End state is bit mask with N bits set to 1
    #2^N -1
    # This is basically 11111....1 N times, as 1<<N will give 1 with N 0s behind as binary repr
    #So represents travelled through all states
    minTourCost = float('inf')
    for e in range(N):
        if e == S:
            continue
        tourCost = memo[e][END_STATE] +m[e][S] #Finds final cost for all end nodes
        #We add back from endstate to start as premise of qn is that saesman goes to all nodes and BACK TO STARTING NODE
        minTourCost = min(tourCost,minTourCost) #Checks for optimal cost
    return minTourCost

def findOptimalTour(m,memo,S,N):
    lastIndex = S #We are gonna travel backwards
    state = (1<<N)-1 #End state
    tour = [S]
    for i in range(N-1,0,-1):# Because the 0th index is S, so we only run through from before it reached start node again to after it traversed start node for the first time 
        index = -1 #N-1 to 1 as we only have N-1 states
        for j in range(N):#While travelling backwards, we are 
            if j == S or notIn(j,state):
                continue
            if index == -1:
                index = j
            prevDist = memo[index][state] + m[index][lastIndex] #Calculates distance from index with current lowest cost, variable storing this is index
            #prevDist calculates last known min cost distance
            newDist = memo[j][state] + m[j][lastIndex] #Calculates distance from jth node to last index in our path
            if newDist < prevDist:
                index = j
        tour.append(index) #append best index
        state = state ^ (1<< index) #update state to take out current best index, for next iteration
        lastIndex = index #Since we are going back, optimal index is now last known, we find best path to this index until the node after start ndoe
    tour.append(S)
    tour.reverse()
    return tour


# Optimised backtracking function for combination       

def OptimisedCombinations(r,N):
    subsets = []
    combiutils(0,0,r,N,subsets)
    return subsets
def combiutils(subset,at,r,n,subsets):
    if r == 0:
        subsets.append(subset)
    else:
        for i in range(at,n):
            subset = (1<<i) | subset #switch bit to 1
            combiutils(subset,i+1,r-1,n,subsets) #for flipping all others bits to 1, with current bit as 1
            subset = subset & ~(1<<i) #backtrack and switch bit back to 0


print('________________Travelling Salesman Problem: DP______________')
print(tsp(g,0))


#---------------------TSP without going back to start node---------

g = [[0,4,1,9],
     [3,0,6,11],
     [4,1,0,2],
     [6,5,-4,0]  ]

def tsp2(g,S): #graph and starting node
    N = len(g)

    #initialise memo table
    #Fill table with null values or +inf

    memo = [[float('inf') for i in range(2**N)] for j in range(N)]
    #memo is 2d table of size N by 2^N
    setup(g,memo,S,N)
    solve(g,memo,S,N)
    minCost,minIndex = findMinCost2(g,memo,S,N) #Our memo contains all solutions for all possible endstates (eg cost if graph ended at node 2, graph if cost ended at node 3)
    tour = findMinTour2(g,memo,S,N,minIndex)
    return (minCost,tour)

def findMinCost2(m,memo,S,N):#SOlves TSP without going back to start
    minCost = float('inf')
    state = (1<<N) -1
    for i in range(N):
        if i == S:
            continue
        cost = memo[i][state]    
        if cost < minCost:
            minCost = cost
            minIndex = i
    return minCost,minIndex

def findMinTour2(m,memo,S,N,minIndex):
    state = (1<<N)-1
    lastIndex = minIndex
    tour = []
    for i in range(N-1,0,-1):
        index = -1
        for j in range(N):
            if j == S or notIn(j,state):
                continue
            if index == -1:
                index = j
            prevdist = memo[index][state] + m[index][lastIndex]
            newdist = memo[j][state] +m[j][lastIndex]
            if prevdist > newdist:
                index = j
        state = state ^ (1<<index)
        lastIndex = index
        tour.append(index)
    tour.append(S)
    tour.reverse()
    return tour
print('_____________Travelling Salesman Problem: W/O Returning__________')
print(tsp2(g,0))