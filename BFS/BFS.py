import copy
import time

def isSafe(grid, row, col):
    if [row,col] in tArray:
        return False
    for pair in grid:
        if row == pair[0]:
            is_blocking = False
            for tree in tArray:
                if pair[0] == tree[0] and pair[1] < tree[1] < col :
                    is_blocking = True
                    break
            if not is_blocking:
                return False

        if col == pair[1]:
            is_blocking = False
            if pair[0] > row:
                for tree in tArray:
                    if tree[1] == col and tree[0] in range(row+1,pair[0]):
                        is_blocking = True
                        break
            else:
                for tree in tArray:
                    if tree[1] == col and tree[0] in range(pair[0]+1,row):
                        is_blocking = True
                        break

            if not is_blocking:
                return False

    i = row+1
    j = col+1
    while i < n and j < n:
        if [i,j] in grid:
            return False
        i += 1
        j += 1

    i = row-1
    j = col+1
    while -1 < i < n and -1 < j < n:
        if [i,j] in tArray:
            break
        if [i,j] in grid:
            return False
        i -= 1
        j += 1

    i = row-1
    j = col-1
    while -1 < i < n and -1 < j < n:
        if [i,j] in tArray:
            break
        if [i,j] in grid:
            return False
        i -= 1
        j -= 1

    i = row+1
    j = col-1
    while -1 < i < n and -1 < j < n:
        if [i,j] in tArray:
            break
        if [i,j] in grid:
            return False
        i += 1
        j -= 1

    return True

def newGrid(grid, row, col):
    new_grid = copy.deepcopy(grid)
    new_grid.append([row,col])
    return new_grid


def possiblePlaces(grid, col, r):
    global count
    queue = []
    #print grid
    for row in range(r+1,n):
        #print "ROwL",row
        if isSafe(grid, row, col):
            #print "col:",col, "row:",row
            count += 1
            #print count
            new_grid = newGrid(grid, row, col)
            #print new_grid
            queue.append(new_grid)
            '''print queue
            print display(new_grid)
            raw_input()'''
            queue += possiblePlaces(new_grid,col,row)



    return queue


def run(grid):
    queue = []
    for c in range(n):
        queue = possiblePlaces(grid,c,-1)
        if len(queue) != 0:
            break

    for col in range(c+1 ,n):
        childQueue = []
        #print queue
        done = False
        for grid in queue:
            childQueue += possiblePlaces(grid, col,-1)
            if len(childQueue) != 0 and col == n-1:
                for childGrid in childQueue:
                    if len(childGrid) == l:
                        done = True
                        print display(childGrid)
                        break
            if done:
                break

        queue = childQueue

def display(grid):
    for i in range(n):
        for j in range(n):
            if [i,j] in tArray:
                print "2",
            elif [i,j] in grid:
                print "1",
            else:
                print "0",
        print "\n",

tstart = time.time()
n = raw_input()
file = open("input.txt","r")
n = int(file.readline())
l = int(file.readline())
tArray = []
count = 0
for i in range(n):
    row = [x for x in file.readline()]
    print row
    for index in range(len(row)-1):
        if row[index] == '2':
            tArray.append([i,index])
print tArray
print run([])
print (time.time())-tstart
print count
