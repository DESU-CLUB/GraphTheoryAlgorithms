grid = [
    ['.','.','.'],
    ['.','#','#'],
    ['.','.','E']
]
x_q = []
y_q = []

start_x = 0
start_y = 0
visited = [[False for i in range(len(grid))] for i in range(len(grid[0]))]

def solve(grid,start_x,start_y,visited):
    move = 0
    cur = 1 #how many nodes in current BFS layer i.e. no of neighbours around current node
    next =0
    x_q.append(start_x)
    y_q.append(start_y)
    len(x_q) 
    visited[start_x][start_y] = True
    while x_q:
        x = x_q.pop(0)
        y = y_q.pop(0)
        if grid[x][y] == 'E':
            grid[x][y] = [prev_x,prev_y]
            return (move,x,y)
        next +=BFS(grid,x,y,x_q,y_q,visited) #records how many nodes in next layer
        cur-=1
        if cur == 0:
            cur = next
            next = 0 #since all of current nodes searched,next layer becomes current layer 
            move+=1 #after all current nodes searched, move up by 1
        prev_x = x
        prev_y = y
        
    return False


def BFS(grid,x,y,xq,yq,visited):
    dr = [1,-1,0,0]
    dc = [0,0,1,-1]
    next = 0
    for i in range(4):
        nx = x+dr[i]
        ny = y+dc[i]
        if nx<0 or ny<0 or nx>=len(grid) or ny>=len(grid[0]):
            continue
        elif grid[nx][ny] == '#':
            continue
        elif visited[nx][ny] == True:
            continue
        else:
            
                
            grid[nx][ny] = [x,y] if grid[nx][ny] != 'E' else 'E'
            visited[nx][ny] = True
            xq.append(nx)
            yq.append(ny)

            next+=1 #how many nodes queued in next BFS layer
    return next #return how many valid nodes discovered by current node
            
            

def path(grid,ex,ey,start_x,start_y):
    x,y = ex,ey
    path = [[ex,ey]]
    while grid[x][y] not in ['#','.']:
        x,y = grid[x][y]
        path.append([x,y])
    path.reverse()
    if path and path[0] == [start_x,start_y] :
        return path
    return []
    

move, ex,ey =solve(grid,start_x,start_y,visited)
print(f'Moves from {start_x},{start_y} to {ex},{ey} is {move}')
print('Path is:')
print(path(grid,ex,ey,start_x,start_y))
#print(grid)
    
