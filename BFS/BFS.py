import copy
import time

def isLizardSafe(all_possible_lizards_positions, row_no, column_no):

    if (row_no,column_no) in trees_coordinates:
        return False

    row_move = [0, 1, 1, 1, 0, -1, -1, -1]
    column_move = [-1, -1, 0, 1, 1,  1,  0, -1]
    for i in range(8):
        row_inc = row_move[i];
        column_inc = column_move[i];

        row_position = row_no + row_inc;
        column_position = column_no + column_inc;

        while (row_position >= 0 and row_position < size_of_nursery and column_position >= 0 and column_position < size_of_nursery and not ((row_position,column_position) in trees_coordinates)):
            if (row_position,column_position) in all_possible_lizards_positions:
                return False
            row_position += row_inc
            column_position += column_inc

    return True

def newSet(lizards_position_set, row_no, col_no):
    new_lizards_position_set = copy.deepcopy(lizards_position_set)
    new_lizards_position_set.add((row_no,col_no))
    return new_lizards_position_set


def possiblePlaces(lizards_position_set,row_no, column_no):
    global count
    queue = []
    for row in range(row_no+1,size_of_nursery):
        if isLizardSafe(lizards_position_set, row, column_no):
            count += 1
            #print count
            new_lizards_position_set = newSet(lizards_position_set, row, column_no)
            queue.append(new_lizards_position_set)
            #print display(new_lizards_position_set)
            #print queue
            #raw_input()
            queue += possiblePlaces(new_lizards_position_set, row, column_no)

    return queue


def run(lizards_position_set):

    queue = []
    no_solution = False
    for start_column in range(size_of_nursery):
        queue = possiblePlaces(lizards_position_set, -1, start_column)
        #print queue
        for position_set in queue:
            if len(position_set) == no_of_lizards:
                return True, position_set
        if len(queue) != 0:
            break

    for column in range(start_column+1, size_of_nursery):
        child_queue = []
        for lizards_position_set in queue:
            updated_lizards_position_queue = possiblePlaces(lizards_position_set, -1, column)
            #print updated_lizards_position_set
            for position_set in updated_lizards_position_queue:
                if len(position_set) == no_of_lizards:
                    return True,position_set
            child_queue += updated_lizards_position_queue
        queue = child_queue

    return no_solution,set()

def display(position_set):
    for i in range(size_of_nursery):
        for j in range(size_of_nursery):
            if (i,j) in trees_coordinates:
                print("2"),
            elif (i,j) in position_set:
                print("1"),
            else:
                print("0"),
        print("\n"),



tstart = time.time()

file = open("input.txt","r")
algorithm_type = file.readline()
size_of_nursery = int(file.readline())
no_of_lizards = int(file.readline())


trees_coordinates = set()

count = 0
for i in range(size_of_nursery):
    row = file.readline()
    for j in range(len(row)-1):
        if row[j] == '2':
            trees_coordinates.add((i,j))


solution, position_set = run(set())

if solution:
    print("OK")
    display(position_set)
else:
    print("Fail")

print (time.time())-tstart
