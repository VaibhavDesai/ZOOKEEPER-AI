import copy
import time
import collections

def isLizardSafe(all_possible_lizards_positions, row_no, column_no):

    if (row_no,column_no) in trees_coordinates_set:
        return False

    row_move = [0, 1, -1]
    column_move = [-1, -1, -1]
    for i in range(3):
        row_inc = row_move[i];
        column_inc = column_move[i];

        row_position = row_no + row_inc;
        column_position = column_no + column_inc;

        while (row_position >= 0 and row_position < size_of_nursery and column_position >= 0 and column_position < size_of_nursery and not ((row_position,column_position) in trees_coordinates_set)):
            if (row_position,column_position) in all_possible_lizards_positions:
                return False
            row_position += row_inc
            column_position += column_inc

    return True

def isLizardSafeOld(all_possible_lizards_positions, row_no, column_no):

    if (row_no,column_no) in trees_coordinates_set:
        return False

    row_move = [0, 1, 1, 1, 0, -1, -1, -1]
    column_move = [-1, -1, 0, 1, 1,  1,  0, -1]
    for i in range(8):
        row_inc = row_move[i];
        column_inc = column_move[i];

        row_position = row_no + row_inc;
        column_position = column_no + column_inc;

        while (row_position >= 0 and row_position < size_of_nursery and column_position >= 0 and column_position < size_of_nursery and not ((row_position,column_position) in trees_coordinates_set)):
            if (row_position,column_position) in all_possible_lizards_positions:
                return False
            row_position += row_inc
            column_position += column_inc

    return True

def display(position_set):
    for i in range(size_of_nursery):
        for j in range(size_of_nursery):
            if (i,j) in trees_coordinates_set:
                print "2",
            elif (i,j) in position_set:
                print "1",
            else:
                print "0",
        print "\n",

def isRestOfColumnHasTrees(row,col):

    print trees_coordinates_hasttable[col]
    print [i for i in range(row,size_of_nursery)]
    print all(select_row in trees_coordinates_hasttable[col] for select_row in [i for i in range(row,size_of_nursery)])
    return all(select_row in trees_coordinates_hasttable[col] for select_row in [i for i in range(row,size_of_nursery)])
    '''
    print "came here"
    print trees_coordinates_hasttable1[col]
    print "cal",(size_of_nursery - (row))
    if size_of_nursery - (row) == len(trees_coordinates_hasttable1[col]):
        return True
    else:
        return False
        '''
    '''if col in trees_coordinates_hasttable and trees_coordinates_hasttable[col] != []:
        print trees_coordinates_hasttable[col]
        print [i for i in range(row,size_of_nursery)]
        print all(select_row in trees_coordinates_hasttable[col] for select_row in [i for i in range(row,size_of_nursery)])
        return all(select_row in trees_coordinates_hasttable[col] for select_row in [i for i in range(row,size_of_nursery)])
        '''


def solveNQUtil(lizards_position_set, row, col):
    #print lizards_position_set , "col",col
    if len(lizards_position_set) == no_of_lizards and col <= size_of_nursery:
        return True

    if col >= size_of_nursery or row > size_of_nursery:
        return False

    for i in range(row, size_of_nursery):
        leftIndex = 0
        display(lizards_position_set)
        print "row:",i , "col",col
        raw_input()

        if isLizardSafe(lizards_position_set, i, col):
        #if isLizardSafe(lizards_position_set, row, col):

            lizards_position_set.add((i,col))
            #lizards_position_set.add((row,col))
            #print trees_coordinates_hasttable1
            if col in trees_coordinates_hasttable1 and len(trees_coordinates_hasttable1[col]) != 0:

                trees_row_deque = trees_coordinates_hasttable1[col]
                print "In if",trees_row_deque
                first_tree_pos = trees_row_deque2[leftIndex]
                #i = first_tree_pos+1
                leftIndex += 1
                '''first_tree_pos = trees_row_deque.popleft()
                i = first_tree_pos+1
                '''
                if solveNQUtil(lizards_position_set, first_tree_pos+1 ,col) == True:
                    return True
                print "in here"
                #trees_row_deque.appendleft(first_tree_pos)
            else:
                if solveNQUtil(lizards_position_set, 0 ,col+1) == True:
                    return True
            print "here"

            lizards_position_set.remove((i,col))
            #lizards_position_set.remove((row,col))

        else:
            if (i,col) in trees_coordinates_set:
            #if (row,col) in trees_coordinates_set:
                if isRestOfColumnHasTrees(i,col):
                #if isRestOfColumnHasTrees(row,col):
                    i = size_of_nursery-1
                    return solveNQUtil(lizards_position_set, 0, col+1)
                else:
                    trees_row_deque2 = trees_coordinates_hasttable1[col]
                    print "In else",trees_row_deque2
                    first_tree_pos1 = trees_row_deque2[leftIndex]
                    #i = first_tree_pos1
                    leftIndex += 1
                    '''if solveNQUtil(lizards_position_set, first_tree_pos1+1 ,col) == True:
                        return True
                    print "was here"
                    trees_row_deque2.appendleft(first_tree_pos1)'''

        '''if col+1 < no_of_lizards:
        if solveNQUtil(lizards_position_set, 0 ,col+1) == True:
            return True
    # if queen can not be place in any row in
    # this colum col  then return false'''
    return False


def solveNQUtilNew(lizards_position_set, row, col):
    #print lizards_position_set , "col",col
    if len(lizards_position_set) == no_of_lizards and col <= size_of_nursery:
        return True

    if col >= size_of_nursery or row > size_of_nursery:
        return False

    leftIndex = 0
    for i in range(row, size_of_nursery):

        #print "left",leftIndex
        display(lizards_position_set)
        print "row:",i , "col",col
        raw_input()

        if isLizardSafe(lizards_position_set, i, col):

            lizards_position_set.add((i,col))

            if col in trees_coordinates_hasttable1 and len(trees_coordinates_hasttable1[col]) != 0:

                trees_row_deque = trees_coordinates_hasttable1[col]
                print "In if",trees_row_deque
                first_tree_pos = trees_row_deque.popleft()
                print "here"

                if solveNQUtilNew(lizards_position_set, first_tree_pos+1 ,col) == True:
                    return True
                trees_row_deque.appendleft(first_tree_pos)
            else:
                if solveNQUtilNew(lizards_position_set, 0 ,col+1) == True:
                    return True

            lizards_position_set.remove((i,col))

        else:
            if (i,col) in trees_coordinates_set:
                print "abc"
                if isRestOfColumnHasTrees(i,col):
                    i = size_of_nursery-1
                    return solveNQUtilNew(lizards_position_set, 0, col+1)
                else:
                    trees_row_deque1 = trees_coordinates_hasttable1[col]
                    first_tree_pos1 = trees_row_deque1.popleft()
                    i = first_tree_pos1
                    print "here here"
                    if solveNQUtilNew(lizards_position_set, first_tree_pos1+1 ,col) == True:
                        return True
                    trees_row_deque1.appendleft(first_tree_pos1)
    return False

def run(lizards_position_set):
    queue = []
    no_solution = False
    for col in range(size_of_nursery):
        if col in trees_coordinates_hasttable and len(trees_coordinates_hasttable[col]) == size_of_nursery:
            continue
        if solveNQUtilNew(lizards_position_set, 0, col):
            return True,lizards_position_set

    return False,set()


size = raw_input()
tstart = time.time()

file = open("input_"+str(size)+".txt","r")
algorithm_type = file.readline()
size_of_nursery = int(file.readline())
no_of_lizards = int(file.readline())


trees_coordinates_hasttable = {}
trees_coordinates_hasttable1 = {}
trees_coordinates_set = set()

count = 0

for i in range(size_of_nursery):
    row = file.readline()
    for j in range(len(row)-1):
        if row[j] == '2':
            trees_coordinates_set.add((i,j))
            if j in trees_coordinates_hasttable:
                trees_coordinates_hasttable[j].append(i)
                trees_coordinates_hasttable1[j].append(i)
            else:
                trees_coordinates_hasttable[j] = [i]
                trees_coordinates_hasttable1[j] = collections.deque()
                trees_coordinates_hasttable1[j].append(i)

solution,lizards_position_set = run(set())
if solution:
    print "OK"
    display(lizards_position_set)
else:
    print "Fail"
print (time.time())-tstart
print count
