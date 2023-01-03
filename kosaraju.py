'''
Kosaraju Algorithm
> Finds SCCs in O(V+E)
'''
from collections import defaultdict
class Stack():
    def __init__(self):
        self.stack = []

    def push(self,item):
        self.stack.append(item)
    
    def pop(self):
        return self.stack.pop()

    def show(self):
        return self.stack

    def isEmpty(self):
        return False if self.stack else True


g = {0:{1:0},1:{2:0},2:{3:0,0:1},3:{4:2},4:{5:0},5:{3:0}}
v = [False]*len(g)



def DFSUtil(g,v,node,stack):
    if v[node] == True:
        return
    v[node] = True
    for child in g[node]:
        DFSUtil(g,v,child,stack)
    stack.push(node)

def transpose(graph):
    ng = defaultdict(dict)
    for i in graph:
        for j in graph[i]:
            ng[j].update({i:graph[i][j]})
    return ng

def kosaraju(g,v):
    stack = Stack()
    for i in g:
        if v[i] == False:
            DFSUtil(g,v,i,stack)

    v = [False]*len(g)
    g_t = transpose(g)
    scc = []
    print(stack.show())
    while not stack.isEmpty():
        nstack = Stack()
        data = stack.pop()
        if v[data] == False:
            DFSUtil(g_t,v,data,nstack)
            scc.append(nstack.show())
        else:
            continue
    
    return scc

            

print(kosaraju(g,v))


    

