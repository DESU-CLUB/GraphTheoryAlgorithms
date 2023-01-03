'''
Dijkstra's Shortest Path
-> Single Source Shortest Path
- for graphs with non -ve edge weights
Time Complexity: O(E*log(V))

Djikstra can tell you shortest distance from source node to all other nodes in graph


Constraint: Edges of graph need non -ve edge weight
-> once node visited, optimal distance cannot be improved
-> enables Dijkstra to act greedily

Lazy and Eager variants

Algorithm
-> DIst array where dist to every node is +ve inf
distance to start node is 0

Priority Queue of key-value pairs of (node,index,distance)pairs which tell you which node to visit next
based on sorted min value

1)Insert startnode, with dist of 0 into priority queue(PQ)
2)Pop out startnode, discover neighbouring nodes
3)If node already visited, skip
4)if distance of neighbouring nodes < current distance in array
update dist array with new distance
5) add neighbouring node to priority queue
6) Find most promising node (node with shortest distance)
7) Pop most promising node and discover neighbours
8) Mark its visited as true
8) Repeat 4-8

Until PQ is empty, shortest distance stored in dist array

### Concept of marking nodes visited
 --> How Dijkstra works is that it finds
     node with shortest distance, and expands on that node

--> If there are multiple paths leading to same node, Dijkstra will find 
    shortest path to node before marking node as visited
    (Because intuitively by following nodes with shortest distance all the way to node you're trying to find
     you will have distance to destination node with shortest distance)

Idea is: A to B has cost of 40
         A to C has cost of 10
         C to B has cost of 5

         Graph is 
            B
         A< |
            C

Discover neighbours of A, B and C
B and C with their distances are appended to priority queue

Since A to C has lowest cost
we expand out neighbours of C,
next, new distance of A to B is 10+5 = 15
as A->C->B offers distance of 15
so, next promising node is from C to B
so now B is marked as visited, distance is 15
A-> B is 40 is ignored
the visited array controls direction



'''
import sys 
from heapq import *

g = {0:{1:4,2:1},1:{3:1},2:{1:2,3:5},3:{4:3},4:{}}

n = len(g)


class Priority(): #Priority Queue implementation using Queue
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def insert(self,item):
        self.queue.append(item)

    def pop(self): #Pops element based on priority
        if self.queue:
            min_idx = -1
            min_val = float('inf')
            for idx in range(len(self.queue)):
                if self.queue[idx][1]<min_val:
                    min_val = self.queue[idx][1]
                    min_idx = idx
            return self.queue.pop(min_idx)



    def size(self):
        return len(self.queue)

    
class Heap(): #Priority Queue implementation using Heap
    def __init__(self):
        self.heap = []

    def parent(self,i):
        return (i)//2

    def l_child(self,i):
        if 2*i+1 <len(self.heap):
            return 2*i+1
        else:
            return False
    
    def r_child(self,i):
        if 2*i+2 < len(self.heap):
            return 2*i+2
        else:
            return False

    
    def getMin(self):
        return self.heap[0]

    def isLeaf(self,pos): #check if its a leaf node
        return pos**2 > len(self.heap)
    
    
    def pop(self): #O(Log(n))
        #removes minimum element
        popped = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.minHeapify(0)
       
        return popped


    def minHeapify(self,i):
        #If node is non leaf node
        #and greater than all children
        if not self.isLeaf(i):
            l = self.l_child(i)
            r = self.r_child(i)
            if l and r:
                if self.heap[i][1] > self.heap[l][1]:
                    self.heap[i],self.heap[l] = self.heap[l],self.heap[i]
                    self.minHeapify(l)
                elif self.heap[i][1] > self.heap[r][1]:
                    self.heap[i],self.heap[r] = self.heap[r],self.heap[i]
                    self.minHeapify(r)
            elif l:
                if self.heap[i][1] > self.heap[l][1]:
                    self.heap[i],self.heap[l] = self.heap[l],self.heap[i]
                    self.minHeapify(l)
            elif r:
                if self.heap[i][1] > self.heap[r][1]:
                    self.heap[i],self.heap[r] = self.heap[r],self.heap[i]
                    self.minHeapify(r)

    def size(self):
        return len(self.heap)

                

        

    def insert(self,val):
        self.heap.append(val)
        idx = len(self.heap) -1
        
        while self.heap[idx][1] < self.heap[self.parent(idx)][1]: #for djikstra, we look at dist, which is 2nd element
            self.heap[idx],self.heap[self.parent(idx)] = self.heap[self.parent(idx)],self.heap[idx]
            idx = self.parent(idx)
            

class OptimHeap(): #Heap using heapq

    def __init__(self):
        self.heap =[]




def djikstra(g,n,s):
    visited = [False]*n #List of visited nodes
    dist = [float('inf')]*n #Distance array
    dist[s] = 0
    pq = Heap()
    pq.insert([s,0]) #Insert start
    while pq.size() !=0:
        index, minvalue = pq.pop() #Unpacks most promising node into index and distance
        #print(pq.heap,[index,minvalue])
        visited[index] = True #Once unpacked, mark as visited
        for neighbour in g[index]: #For every neighnour of most promising node
            if visited[neighbour]: #check if visited
                continue
            newdist = dist[index]+g[index][neighbour] #new distance of neighbouring node is current node's distance from s + weight
            if newdist < dist[neighbour]: #if newdist is better than current neighbour
                dist[neighbour] = newdist #update dist array with new dist
                pq.insert([neighbour,newdist]) #insert neighbour and its distance from s into pq
                #If not smaller than current distance, we dont bother adding it to priority queue as it will be ignored
    return dist

dist = djikstra(g,n,0)
print(dist)



def djikstra2(adj,len_nodes,start):
    visited = [False]*len_nodes
    dist = [float('inf') for i in range(len_nodes)]
    dist[start] = 0
    pq = []
    heappush(pq,[0,start])
    while len(pq) >0:
        minval,idx = heappop(pq) #Since cannot specify along which axis to compare for heapq, we invert storage
            #So stored in (cost,which node) instead
        visited[idx] = True
        if dist[idx] <minval: #to optimise further,skipping stale indices
            continue #while neighbours are skipped if visited, nodes already in priority queue 
                    #still go through even if node is visited
        for neighbour in adj[idx]: 
            if visited[neighbour]:
                continue
            newdist = dist[idx]+adj[idx][neighbour]
            if newdist < dist[neighbour]:
                dist[neighbour] = newdist
                heappush(pq,[newdist,neighbour])
    return dist


print(djikstra2(g,n,0))

'''
We're adding duplicate node indices with different costs
instead of updating the current node index because
adding takes O(log(n)) while searching for key takes O(n)

'''



def djikstra3(g,n,s,e):
    dist = [float('inf')]*n
    visited = [False]*n
    prev = ["null"]*n #For finding shortest path

    dist[s] = 0
    pq = []
    heappush(pq,[0,s])

    while pq:
        val, idx = heappop(pq)
        visited[idx] = True
        if idx == e:
            return (dist,prev) #we stop early because once visited, it means shortest distance already acquired for node
            #so can just return now
        if dist[idx] < val:
            continue
        for neighbor in g[idx]:
            newdist = dist[idx]+g[idx][neighbor]
            if dist[neighbor] > newdist:
                dist[neighbor] = newdist
                heappush(pq,[newdist,neighbor])
                prev[neighbor] = idx
    

def findShortestPath(dist,prev,s,e):
    path = []
    cur = e
    while cur != 'null':
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    if path[0] == s:
        print(f'Path from {s} to {e}:',path)
        print('Total cost is',dist[e])
    return[]
dist,prev = djikstra3(g,n,0,4)
findShortestPath(dist,prev,0,4)


'''
Eager Djikstra's using Indexed Priority Queue

Lazy Djikstra uses duplicate key-value pairs

inefficient for dense graph as we end up with several stale 
outdated key value pairs

eager ver avoids dupes, support efficient value updates in O(log(n))
using indexed priority queue


D-ary heap optimisation

When ex edjikstra, on dense graph, alot of ops

D-ary heap  has d children,so we can update faster but at the cost of removals
can update key in O(1)

TO remove, swap root with last element
then find smallest child from root and swap until done

But optimized as there are less removals than updates

For optimal D-ary heap degree,
D = E/V is the best degree to use to balance removals against decreasekey ops
-> improving complexity to O(E*log of base e/v (V))
much better for dense graphs

State of the Art for Djikstra: Fibonacci Heap
Time complexity of O(E+Vlog(V))
--> Cons
    Difficult to implement
    Large constant amortized overhead
--> Only use if very large graph

'''
##TO DO TMR
#Implement Eager +IPQ
#Use D-ary Heap
'''
Indexed Priority Queue is a PQ that supports quick updates
and deletions of key value graphs

very impt to dynamically update priority

assign index values to all keys, form bidirectional mapping
create mapping using (0,N)

To access value for any key k, find key index
do lookup in vals array maintained by IPQ

We need 4 arrays
key
vals
position map: maps key index to node
inverse map: maps node index to key-> gives info which key value associated with node

to insert, we update position map and inverse map along with val arr
then fix heap invariant

to delete,
we swap bottom right child with val, then delete val at bottom right pos
update pm im during swap and delete
fix heap invariant


To update value of key
-> update then swim and sink
'''
class IndexedMinPQ:
    def __init__(self,N):
        #Use indices as key
        self.pm = [None]*N #maps node to key in heap
        self.im = [None]*N#maps node index to val
        self.val = [None]*N #heap itself, contains values
        self.size = 0
        self.maxsize = N
        #to find value of node from key: vals[7]
        # to find value from node index val[key[im[0]]]
        #find node index from key: pm[3] will give node index
    
    def parent(self,i):
        return i//2


    def insert(self,ki,value):
        '''
        Inserts value into min indexed binary heap
            - Key value must not be in heap already
            - value cannot be null
        ki: keyvalue from 0 to N
        value: value
        '''
        if self.val[ki] != None:
            print('key already exists')
            return
            #size is cur sz of map
        if self.size >= self.maxsize:
            print('Max size reached')
            return

        self.val[ki] = value
         
         #since node index is self.vals index, can do following:
        self.pm[ki]= self.size #puts value at the back of pm array first

        self.im[self.size] = ki
        self.swim(self.size) #swim takes current node's index and swap with parent if node <parent

        self.size +=1


    def swim(self,node):
        '''
        swim takes node and checks if parent can swap with node


        i.e child <parent
        '''
        def swap(node,p):
            #swap position map first
            #as it takes reference from im
            self.pm[self.im[node]],self.pm[self.im[p]] = self.pm[self.im[p]],self.pm[self.im[node]]

            self.im[p],self.im[node] = self.im[node],self.im[p]

        def less(node,p):
            #checks if current node < parent
            if self.val[self.im[p]] > self.val[self.im[node]]:
                return True

        parent = self.parent(node)

        while node>0 and less(node,parent):
            #swap pm and im positions
            swap(node,parent)
            #update pointer of node:now it is the parent
            node = parent
            #update parent again
            parent = self.parent(node)

    def delete(self,ki):
        if self.size == 0:
            print('No values to delete')
            return 
        if self.val[ki] == 'None':
            print('Node has no value')
            return 

        # Swap pm and im pos
        node = self.pm[ki]

        self.size -=1#BEcause self.size will also be +1 of index of last element

        self.pm[self.im[node]],self.pm[self.im[self.size]] = self.pm[self.im[self.size]],self.pm[self.im[node]]

        self.im[node],self.im[self.size] = self.im[self.size],self.im[node]

       
        #since values of pm has been swapped

        rt_val = self.val[ki]
        self.val[ki] = None 
        self.pm[ki] = None 
        self.im[self.size] = None

        #set to none first so swim and sink doesnt include deleted node

       
        self.sink(node)
        self.swim(node)
        

        

        
        
        return rt_val
       
        

        

    def sink(self,node):
        while True:
            l = node*2+1
            r = node*2+2
            smallest = l
            print(l>self.size,l,self.size)
            if l>=self.size or self.val[self.im[l]] > self.val[self.im[node]]:
                return 
                
            if r <self.size and self.val[self.im[l]] > self.val[self.im[r]]:
                smallest = r

            self.pm[self.im[node]],self.pm[self.im[smallest]] = self.pm[self.im[smallest]],self.pm[self.im[node]]

            self.im[smallest],self.im[node] = self.im[node],self.im[smallest]


    def decrease_key(self,ki,value):
        if value < self.val[ki]:
            self.val[ki] = value
            self.swim(self.pm[ki])

    def peek(self):
        key = self.im[0]
        return key

    def pop(self): #delete min value in IPQ
        return self.delete(self.peek())

    def keyExists(self,ki):
        if self.val[ki] != None:
            return True



    def __len__(self):
        return self.size

def eagerDjikstra(g,n,s,e):
    visited = [False]*n
    dist = [float('inf')]*n
    dist[s] = 0
    pq = IndexedMinPQ(n)
    pq.insert(0,0)
    
    while len(pq)!=0:
       
        key = pq.peek()
        visited[key] = True
        val= pq.pop()
        print('Removing',pq.im,pq.pm,pq.val)
        if dist[key] <val:
            continue

        if key == e:
            return dist

        for neighbour in g[key]:
            if visited[neighbour]:
                continue
            newdist = dist[key]+ g[key][neighbour]
            
            if newdist < dist[neighbour]:
                dist[neighbour] = newdist

                if pq.keyExists(neighbour):
                    pq.decrease_key(neighbour,newdist)
                    print('Updating',pq.im,pq.pm,pq.val)
                else:
                    pq.insert(neighbour,newdist)
                    print('Inserting',pq.im,pq.pm,pq.val)
    return -1

            
            
print(eagerDjikstra(g,n,0,4))


'''

K-ary heap

generalisation of binary heap
each node have K children
Properties:
    Nearly complete binary tree, all levels have max nodes except last

        Can have max k-ary / min k-ary heap


        Aloows faster decreasekey ops at expense of removal ops

        Better memcache behabiour

        Parent = (i-1)/k

        Children = (k*1)+k

        last non leaf at (n-2)//k

        where k is degree
'''

class k_Heap():
    def __init__(self,k):
        '''
        K represents degree of k-ary heap
        '''
        self.k = k
        self.arr = []

    def parent(self,i):
        return (i-1)//self.k

    def first_child(self,i):
        return (self.k*i)+1 if self.k*i+1 <len(self.arr) else -1


    def fin_non_leaf(self):
        print('yo',(len(self.arr)-2)//self.k)
        return (len(self.arr)-2)//self.k

    def insert(self,value):
        self.arr.insert(0,value)

        if len(self.arr) == 1:
            return
        self.restoreUp(self.fin_non_leaf())

    def restoreUp(self,i):
        print('hello',i)
        if self.first_child(i) == -1:
            return
        child = self.first_child(i)
        min_child = float('inf')
        min_child_idx = -1
        for j in range(self.k):
            nchild = child+j
            if nchild >= len(self.arr):
                break
            if min_child > self.arr[nchild]:
                min_child = self.arr[nchild]
                min_child_idx = nchild

        if min_child < self.arr[i]:
            self.arr[i],self.arr[min_child_idx] = self.arr[min_child_idx],self.arr[i]
        else:
            return
        parent = self.parent(i)
        if parent>=0:
            self.restoreUp(parent)


    def restoreDown(self,i):
        '''
        Fix heap invariant from root to leaf
        '''
        if self.first_child(i) == -1:
            return
        child = self.first_child(i)
        min_child = -1
        min_child_idx = -1
        for j in range(self.k):
            nchild = child+j
            if nchild >= len(self.arr):
                break
            if min_child > self.arr[nchild]:
                min_child = self.arr[nchild]
                min_child_idx = nchild
        if min_child < self.arr[i]:
            self.arr[i],self.arr[min_child_idx] = self.arr[min_child_idx],self.arr[i]
        else:
            return
        if self.parent(i) >=0:
            self.restoreDown(min_child_idx)




    def deleteMin(self):
        val = self.arr[0] 
        self.arr[0] = self.arr.pop()
        self.restoreDown(0)
        return val

    def __str__(self):
        return' '.join([str(i) for i in self.arr])
            


        



a = k_Heap(3)
a.insert(1)
a.insert(3)
a.insert(0)
print(a)
c=  a.deleteMin()
print(a)
print(c)
        
        

