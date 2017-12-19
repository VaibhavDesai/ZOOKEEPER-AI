import time
import collections
import sys

sys.setrecursionlimit(1000000000)
orig_stdout = sys.stdout

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

def display(position_set):
    for i in range(size_of_nursery):
        a = ""
        for j in range(size_of_nursery):

            if (i,j) in trees_coordinates_set:
                a = a + "2"
            elif (i,j) in position_set:
                a = a + "1"
            else:
                a = a + "0"
        print(a)

def isRestOfColumnHasTrees(row,col):

    return all(select_row in trees_coordinates_hasttable[col] for select_row in [i for i in range(row,size_of_nursery)])


def solveNQUtilNew(lizards_position_set, row, col,ptr):


    if len(lizards_position_set) == no_of_lizards and col <= size_of_nursery:
        return True

    if col >= size_of_nursery or row > size_of_nursery:
        return False
    for i in range(row, size_of_nursery):

        display(lizards_position_set)
        #print "0----------------0"

        #print "row:",i , "col",col
        #raw_input()

        if isLizardSafe(lizards_position_set, i, col):

            lizards_position_set.add((i,col))

            if col in trees_coordinates_hasttable1 and len(trees_coordinates_hasttable1[col]) > ptr:

                trees_row_deque = trees_coordinates_hasttable1[col]
                first_tree_pos = trees_row_deque[ptr]
                ptr += 1

                if first_tree_pos+1 == size_of_nursery:
                    if solveNQUtilNew(lizards_position_set, 0 ,col+1,0) == True:
                        return True
                else:
                    if solveNQUtilNew(lizards_position_set, first_tree_pos+1 ,col,ptr) == True:
                        return True

            else:

                if solveNQUtilNew(lizards_position_set, 0 ,col+1,0) == True:
                    return True

            lizards_position_set.remove((i,col))

        else:

            if (i,col) in trees_coordinates_set:
                ptr += 1
                if isRestOfColumnHasTrees(i, col):
                    i = size_of_nursery-1
                    return solveNQUtilNew(lizards_position_set, 0, col+1,ptr)
        if i == size_of_nursery - 1:
            return solveNQUtilNew(lizards_position_set, 0, col + 1, 0)

    return False

def run(lizards_position_set):

    for col in range(size_of_nursery):
        if col in trees_coordinates_hasttable and len(trees_coordinates_hasttable[col]) == size_of_nursery:
            continue
        if solveNQUtilNew(lizards_position_set, 0, col,0):
            return True,lizards_position_set

    return False,set()


size = raw_input()
tstart = time.time()

file = open("input"+".txt","r")

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
            trees_coordinates_set.add((i, j))
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
#sys.stdout = orig_stdout
#file1.close()
#print (time.time())-tstart
#print count
