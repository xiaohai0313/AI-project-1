import queue
f = open("input.txt","r")
All_line = f.readlines()
Task = []
for line in All_line:
    temp = line.strip('\n')
    temp = line.split('\t')
    temp = line.strip('\n')
    Task.append(temp)


Decrptype = Task[0]
RCnumber = [int(n) for n in Task[1].split()]
max_col , max_row = RCnumber[0] , RCnumber[1]


Initial_position = [int(n) for n in Task[2].split()]
#Initial_position[0] , Initial_position[1] = Initial_position[1] , Initial_position[0]

Max_deep = int(Task[3])
Target_number = int(Task[4])

Target = []
for i in range(0,Target_number,1):
    Target.append([int(n) for n in Task[5+i].split()])

grid = []

for i in range(0,max_row,1):
    grid.append([int(n) for n in Task[5+Target_number+i].split()])

white = 0
gray = 1
black = 2



class Node:
    def __init__(self,x):
        self.color = white
        self.value = 0
        self.elevation = x
        self.path = []
        self.row = 0
        self.col = 0
        self.Avalue = 0
   #     self.parent = [0,0]

def BFS(nrow,ncol,initial,mdeep,targetnumber,target,grid , result):
    grid[initial[1]][initial[0]].color = gray
    grid[initial[1]][initial[0]].row = initial[1]
    grid[initial[1]][initial[0]].col = initial[0]
    grid[initial[1]][initial[0]].path = [[initial[0],initial[1]]]
    Que = queue.Queue()
    Que.put(grid[initial[1]][initial[0]])
    while Que.qsize() != 0:
        current = Que.get()
        if [current.col , current.row] in target:
            result[target.index([current.col , current.row])] = current.path
            targetnumber -= 1
        if targetnumber == 0:
            return result
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                if current.row + i >= nrow or current.col + j >= ncol or grid[current.row + i][current.col + j].color != white or abs(current.elevation - grid[current.row + i][current.col + j].elevation) > mdeep or current.row + i < 0 or current.col + j < 0:#> 0
                    continue


                grid[current.row + i][current.col + j].row = current.row + i
                grid[current.row + i][current.col + j].col = current.col + j
                grid[current.row + i][current.col + j].color = gray
                grid[current.row + i][current.col + j].path = current.path + [[current.col + j , current.row + i]]
                Que.put(grid[current.row + i][current.col + j])

        current.color = black




def UCS(nrow,ncol,initial,mdeep,targetnumber,target,grid , result):
    grid[initial[1]][initial[0]].value = 0
    grid[initial[1]][initial[0]].row = initial[1]
    grid[initial[1]][initial[0]].col = initial[0]
    grid[initial[1]][initial[0]].color = white
    grid[initial[1]][initial[0]].path = [[initial[0], initial[1]]]

    open = []
    open.append((0, initial[0] , initial[1] , grid[initial[1]][initial[0]] ))      #col , row
    while open != []:
        current = open.pop(0)
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if current[2] + i >= nrow or current[1] + j >= ncol or abs(current[3].elevation - grid[current[3].row + i][current[3].col + j].elevation) > mdeep or current[3].row + i < 0 or current[3].col + j < 0 or (i==0 and j == 0):
                    continue

                in_open = False
                in_closed = False
                different = 0
                if abs(i) == abs(j) == 1:
                    different = 14
                else:
                    different = 10

                if grid[current[3].row + i][current[3].col + j].color == gray:
                    in_open = True

                elif grid[current[3].row + i][current[3].col + j].color == black:
                    in_closed = True

                if in_open == False and in_closed == False:
                    open.append((current[3].value + different , current[1] + j,current[2]+ i , grid[current[3].row + i][current[3].col + j]))
                    grid[current[2] + i][current[1] + j].row = current[2] + i
                    grid[current[2] + i][current[1] + j].col = current[1] + j
                    grid[current[2]+ i][current[1] + j].path = current[3].path + [[current[1] + j,current[2] + i]]
                    grid[current[2]+ i][current[1] + j].value = current[0] + different
                    grid[current[2]+ i][current[1] + j].color = gray

                elif in_open == True:
                    if current[0] + different < grid[current[2]+ i][current[1] + j].value:
                        open.remove((grid[current[2]+ i][current[1] + j].value, current[1] + j , current[2] + i , grid[current[2]+ i][current[1] + j]))
                        open.append((current[3].value + different, current[1] + j, current[2] + i,grid[current[3].row + i][current[3].col + j]))
                        grid[current[2] + i][current[1] + j].path = current[3].path + [[current[1] + j,current[2] + i]]
                        grid[current[2] + i][current[1] + j].value = current[0] + different
                        grid[current[2] + i][current[1] + j].color = gray
                        grid[current[2] + i][current[1] + j].row = current[2] + i
                        grid[current[2] + i][current[1] + j].col = current[1] + j

                elif in_closed == True:
                    if current[0] + different < grid[current[2]+ i][current[1] + j].value:
                        open.append((current[3].value + different, current[1] + j, current[2] + i,grid[current[3].row + i][current[3].col + j]))
                        grid[current[2] + i][current[1] + j].path = current[3].path + [[current[1] + j,current[2] + i]]
                        grid[current[2] + i][current[1] + j].value = current[0] + different
                        grid[current[2] + i][current[1] + j].color = gray
                        grid[current[2] + i][current[1] + j].row = current[2] + i
                        grid[current[2] + i][current[1] + j].col = current[1] + j
        current[3].color = black
        open.sort()
    #result[ii] = grid[target[1]][target[0]].path
    for index , x in enumerate(target):
        if x[1] >= 0 and  x[0] >= 0 and x[1] < nrow and x[0] < ncol:
            result[index] = grid[x[1]][x[0]].path


def htest(cur,goal,grid):
     #return (14 + abs(grid[cur[1]][cur[0]].elevation - grid[goal[1]][goal[0]].elevation)) if (abs(cur[0] - goal[0]) >= 1 and abs(cur[1] - goal[1]) >= 1) else (10 + abs(grid[cur[1]][cur[0]].elevation - grid[goal[1]][goal[0]].elevation))
     return ((abs(cur[0] - goal[0]) + abs(cur[1] - goal[1])) * 7) + abs(grid[cur[1]][cur[0]].elevation - grid[goal[1]][goal[0]].elevation)  # [col][row]




def A_star(nrow,ncol,initial,mdeep,targetnumber,goal,grid , result,ii):
    grid[initial[1]][initial[0]].value = 0
    grid[initial[1]][initial[0]].row = initial[1]
    grid[initial[1]][initial[0]].col = initial[0]
    grid[initial[1]][initial[0]].path = [[initial[0], initial[1]]]
    grid[initial[1]][initial[0]].color = white

    open = []
    open.append((0, initial[0] , initial[1] , grid[initial[1]][initial[0]] ))
    while open != []:
        current = open.pop(0)
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if current[2] + i >= nrow or current[1] + j >= ncol or abs(current[3].elevation - grid[current[3].row + i][current[3].col + j].elevation) > mdeep or current[3].row + i < 0 or current[3].col + j < 0 or (i == 0 and j == 0):
                    continue

                in_open = False
                in_closed = False
                if grid[current[3].row + i][current[3].col + j].color == gray:
                    in_open = True

                if grid[current[3].row + i][current[3].col + j].color == black:
                    in_closed = True
                if abs(i) == abs(j) == 1:
                    different = 14 + abs(current[3].elevation - grid[current[3].row + i][current[3].col + j].elevation)
                else:
                    different = 10 + abs(current[3].elevation - grid[current[3].row + i][current[3].col + j].elevation)
                hvalue = htest((current[3].col + j , current[3].row + i), goal , grid)
                if in_open == False and in_closed == False:
                    open.append([current[3].value + different + hvalue,current[1] + j,current[2]+ i , grid[current[3].row + i][current[3].col + j]])
                    grid[current[2] + i][current[1] + j].row = current[2] + i
                    grid[current[2] + i][current[1] + j].col = current[1] + j
                    grid[current[2] + i][current[1] + j].path = current[3].path + [[current[1] + j, current[2] + i]]
                    grid[current[2] + i][current[1] + j].value = current[3].value + different
                    grid[current[2] + i][current[1] + j].color = gray
                    grid[current[2] + i][current[1] + j].Avalue = current[3].value + different + hvalue
                elif in_open == True:
                    if current[3].value + different < grid[current[2]+ i][current[1] + j].value:
                        open.remove([grid[current[2]+ i][current[1] + j].Avalue, current[1] + j,current[2]+ i , grid[current[3].row + i][current[3].col + j]])
                        open.append([current[3].value + different + hvalue,current[1] + j,current[2]+ i , grid[current[3].row + i][current[3].col + j]])
                        grid[current[2] + i][current[1] + j].path = current[3].path + [[current[1] + j, current[2] + i]]
                        grid[current[2] + i][current[1] + j].Avalue = current[3].value + different + hvalue
                        grid[current[2] + i][current[1] + j].value = current[3].value + different
                        grid[current[2] + i][current[1] + j].color = gray
                        grid[current[2] + i][current[1] + j].row = current[2] + i
                        grid[current[2] + i][current[1] + j].col = current[1] + j
                elif in_closed == True:
                    if current[3].value + different < grid[current[2]+ i][current[1] + j].value:
                        open.append([current[3].value + different + hvalue,current[1] + j,current[2]+ i , grid[current[3].row + i][current[3].col + j]])
                        #open.append((current[1] + different + htest([current[3][0] + j, current[3][1] + i] , goal), current[1] + different, htest([current[3][0] + j, current[3][1] + i] , goal) , [current[3][0] + j, current[3][1] + i] , [current[3][0], current[3][1]]))
                        grid[current[2] + i][current[1] + j].path = current[3].path + [[current[1] + j, current[2] + i]]
                        grid[current[2] + i][current[1] + j].value = current[3].value + different
                        grid[current[2] + i][current[1] + j].color = gray
                        grid[current[2] + i][current[1] + j].row = current[2] + i
                        grid[current[2] + i][current[1] + j].col = current[1] + j
                        grid[current[2] + i][current[1] + j].Avalue = current[3].value + different + hvalue
        open.sort()
        current[3].color = black
        if current[3].color == black and current[3].row == goal[1] and current[3].col == goal[0]:
            break
    result[ii] = grid[goal[1]][goal[0]].path



#def list_to_string(list,output):

if __name__=="__main__":
    for i in range(max_row):
        for j in range(max_col):
            grid[i][j] = (Node(grid[i][j]))
    result = [[] for n in range(Target_number)]
    output = ''
    if Decrptype == "BFS":
        BFS(max_row, max_col, Initial_position, Max_deep, Target_number, Target, grid, result)
    if Decrptype == 'UCS':
        UCS(max_row, max_col, Initial_position, Max_deep, Target_number, Target, grid, result)
    if Decrptype == 'A*':
        for ind, x in enumerate(Target):
            if x[0] >= max_col or x[1] >= max_row or x[0] < 0 or x[1] < 0 or Initial_position[0] >= max_col or Initial_position[1] >= max_row or Initial_position[0] < 0 or Initial_position[1] < 0:
                continue

            for i in range(max_row):
                for j in range(max_col):
                    grid[i][j] = Node(grid[i][j].elevation)
            A_star(max_row, max_col, Initial_position, Max_deep, 1, x, grid,result,ind)
    #print(result)
    rlength = 0
    for x in result:
        first = 0
        if x == []:
            output += 'FAIL'
        else:
            for y in x:
                if first == 0:
                    output += '{},{}'.format(y[0],y[1])
                    first+=1
                else:
                    output += ' {},{}'.format(y[0], y[1])
        if rlength < len(result) - 1:
            output += '\n'
            rlength+=1
    print(output)
    f = open("output.txt", "w")
    for x in output:
        f.write(x)


