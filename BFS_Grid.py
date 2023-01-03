'''
Many graph problems can be repr in grid

grids are implicit graph

can determine nodes neighbours based on location in grid

eg finding maze path

Common approach to solve graph theory prob on grid
is to convert grid to familiar format
-> eg adj list/matrix

IMPT: Assuming graph is unweighted and cells connect left,up,right,down

BFS on grid:
1) Convert grid to adj list
    a) Label grid cells with nums [0,n)
    where n = row x columns
    b)Construct adj list/matrix
    c)For matrix need to set up nxn matrix
    d)Nodes connect to top,down,right,left
    e) reflect thatin adj list
2) run algorithm

However, transformations between graph repr
can be usually avoided due to grid structure

Can use direction vectors
Define direction vectors for NSEW,
broken down into direction for row and column lists each
then loop for directions
and update direction with direction vector
if not out of bounds, rr,cc is neighboring cell of r,c

1) Add start node to queue
2) add adjacent nodes to queue
3) if cell is a rock,do not add to queue
4) if visited or alr in queue, do not add
'''
grid = [
    ['.','.','.'],
    ['.','#','#'],
    ['.','.','E']
]
prev= []
queue = []
start_x=1
start_y = 0
# Where # is rocks, E is escape
#start is grid[0][0]
#We will update grid with / for visited nodes
#get index of E:
for i in range(len(grid)):
    
    if 'E' in grid[i]:
        x_end = i
        y_end = grid[i].index('E')
grid[x_end][y_end] = '.'
def BFS_grid(grid,x_cur,y_cur,queue,x_start,y_start):
    dr = [1,-1,0,0] #NSEW effect on row
    dc =[0,0,1,-1]# NSEW effect on columns
    for i in range(4):
        nx = x_cur+dr[i]
        ny = y_cur+dc[i]
        if nx >=len(grid) or ny >=len(grid[0])or nx<0 or ny <0:
            continue
        elif grid[nx][ny] == '#' or grid[nx][ny] not in '.E':
            continue
        else:
            if [nx,ny] != [x_start,y_start]: #or grid of start
                queue.append([nx,ny])
                grid[nx][ny] = str(x_cur)+','+str(y_cur)
    if queue:
        node_x,node_y = queue.pop(0)
        BFS_grid(grid,node_x,node_y,queue,x_start,y_start)

def MakePath(sx,sy,ex,ey,grid):
    cur_x = ex
    cur_y = ey
    path = [[ex,ey]]
    while grid[cur_x][cur_y] != '.': 
        cur_x,cur_y = list(map(lambda x: int(x),grid[cur_x][cur_y].split(',')))
        path.append([cur_x,cur_y])
    path.reverse()
    if path and path[0] == [sx,sy]:
        return path
    else:
        return []

BFS_grid(grid,start_x,start_y,queue,start_x,start_y)
print(MakePath(start_x,start_y,x_end,y_end,grid))

            
    

'''

Alternative state representation

instead of storing as (x,y)
use one queue for each dimension

Need to enqueue/dequeue from all queues at the same time

'''
