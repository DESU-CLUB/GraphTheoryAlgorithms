'''
Floyd Warshal Algorithm

All pairs shortest path:
    Find shortest path between all pairs of nodes

    Time Complexity:  O(V**3)
    Ideal for graphs with less than couple 100 nodes

    Optimal way to represent graph is adj mat
    for FW
    m[i][j] represens edge of i to j.

    Distance from node to itself is 0
    So diagonal all zeroes.

    if no edge from i to j set edge val as +inf

    If lang does not support const for +inf
    avoid using int max
    use a large constant like 10^^7 instead

    FW builds up all intermediate routes between nodes i and j
    finds optimal path

    given
        b
   a<     \
       ->   c

    if m[a][b]+m[b][c]< m[a][c],
    route through b to c instead

    Use memoisation

    Let 'dp' be a 3d matrix of size n*n*n
    that acts as a memo table

    dp[k][i][j] = shortest path from i to j routing k nodes
    for nodes {0,1,....,k-1,k}

    Gradually builds optimal solutions for nodes 0 and 1
    then nodes 0 and 2
    until n-1 which stores APSP solution

    dp[n-1] is solution we're after

    How to populate DP table
      -> dp[k][i][j] = m[i][j] if k = 0
      so dp[k][i][j] is distance between nodes i and j

    otherwise,
    dp[k][i][j] is minimum of dp[k-1][i][j] and
    dp[k-1][i][k] + dp[k-1][k][j]

    so to explain the equation, it is trying to find whether
    direct path from i to j, is better than intermediate path from
    i to k, and k to j.

    Explanation:
    dp[k-1][i][j]
    Reuse best distance from i to j with values routing through nodes {0,1...,k}

    Right side says go from i to k, then k to j

    To elaborate more on population
        Firstly, if k = 1,if i = 0 and j = 2
         LHS: it checks whether 0 can connect to 2, calculate distance
         RHS: now, using 1 as an intermediate route, it checks if
         distance from 0 to 1, 
         
         then compare whether distance from 0 to 1 to 2 is smaller
         than direct route from 0 to 2
         
         store min distance


        so lets, say in the case 0 is connected to 2 which is connected to 3
        and 0 is also connected to 3, but 0-3 has a longer distance

        LHS will find distance from 0 to 3
        RHS will find distance from 0 to 2:
                it looks back at k-1[i][k]
                which takes optimal distance from 0 to 2

                during previous iteration, we have established 0
                to 1, then 1 to 2 is the shortest distance

                so [k-1][0][2] will store min distance which is 0 to 1 to 2

                so in a sense, it uses previous result to compute current result
               
                furthermore, by doing this, we can express routes with many intermediate nodes
                we can get dist 0-1-2 by using result 1,0,2 in dp
                so if 4 is connected to 3, in dp[3][0][4], it will take 0-1-2-3-4's distance
                you can see that it has 2 intermediate nodes hre

       then stores min distance from i to j using k as a intermediary


       if intermediate route not connected to i or j, it will be +inf,
       thus direct route if any will be better


       if lets say we found out 0 to 9 to 3 has a better route

       we will recompute 0 to 3 when k =9
        check if current optimal route is better than intermediate route 0-9 then 9-3
       
       and 9[0][3] will have best result as of k=9 

    thus, [k-1][i][j] will store best solution for i to j distance


Optimisation of space
    O(V**3) memory as our memo table has 3 dimensions
    To optimise, can compute k in place

    saving us memory and reducing space complexity to
    O(V**2)

    so

    dp[i][j] = m[i][j] if k = 0

    otherwise,
    dp[i][j] = min(dp[i][j], dp[i][k]+dp[k][j])
'''

m = [ [0,1,float('inf'),float('inf')],
      [float('inf'),0,6,2],
      [float('inf'),float('inf'),0,float('inf')],
      [float('inf'),float('inf'),2,0]
                                                ]

def propagateNegative(m,dp):
    #checks for -ve cycles
    for k in range(len(m)):
        for i in range(len(m)):
            for j in range(len(m)):
                if dp[i][k]+dp[k][j]<dp[i][j]:
                    dp[i][j] = -float('inf') #-ve cycle, so -inf is solution
                    next[i][j] = -1 #means shortest path compromise
                                




def fm1(m): #Unoptimised version
    dp = [[[m[i][j] if k == 0 else float('inf') for j in range(len(m))] for i in range(len(m))] for k in range(len(m))]
    for k in range(1,len(m)):
        for i in range(len(m)):
            for j in range(len(m)):
                dp[k][i][j] = min(dp[k-1][i][j],dp[k-1][i][k]+dp[k- 1][k][j])
    return dp[-1] #prints final solution
 #Note this implementation didnt check for -ve cycles
print(fm1(m))

#We can optimise this by looping k times
#but replace the valur of ij whenever its better


def fm2(m): #Optimised version
    dp = [[m[i][j] for j in range(len(m))] for i in range(len(m))]
    next = [[j if m[i][j] != float('inf') else float('inf') for j in range(len(m))] for i in range(len(m))]
    #next[i][j] represents prev node leading to m[i][j]

    for k in range(1,len(m)):
        for i in range(len(m)):
            for j in range(len(m)):
                if dp[i][j]>dp[i][k]+dp[k][j]:
                    dp[i][j] = dp[i][k]+dp[k][j]
                    next[i][j] = k #instead of j, going to k has shorter cost
                   
    propagateNegative(m,dp)
    return (dp,next) #prints final solution


def reconstruct(dp,next,start,end):
    path = []
    cur = end
    path.append(cur)
    if dp[start][cur] == float('inf'):
        return([],float('inf')) #means no connection in first place
    
    while next[start][cur] != cur: #checks if start is reached, as path[start][start] = start 
        cur = next[start][cur]
        if cur == -1:
            print('No path as negative cycle encountered')
            return
        path.append(cur)
        
    path.append(start)
    path.reverse()
    return path,dp[start][end]

dp,next = fm2(m)
print(dp)
print('FW next',next)
path,cost = reconstruct(dp,next,1,0)
print('Path:',path)
print('Cost:',cost) #Cost is distance

'''
What is a negstive cycle

nodes directly involved in -ve cycle

nodes not in -ve cycle but connected to nodes in -ve cycle

if optimal path goes through -ve cycle, path is compromised
'''
