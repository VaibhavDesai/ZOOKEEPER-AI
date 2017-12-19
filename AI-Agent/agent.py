import random
import math
import collections
import copy
import sys


sys.setrecursionlimit(1000000000)
orig_stdout = sys.stdout

###########################SA#######################

class TimeoutError(Exception):
    pass

def signal_handler(signum, frame):
    raise TimeoutError()

class SA(object):

    size_of_nursery = 0
    number_of_lizards = 0
    trees_set = set()

    def __init__(self, size_of_nursery, number_of_lizards, trees_set):
        self.size_of_nursery = size_of_nursery
        self.number_of_lizards = number_of_lizards
        self.trees_set = trees_set
        current_energy = 1
        alpha = 1
        current_state = set()

        try:

            current_energy, current_state = self.run(alpha)

        except ZeroDivisionError:

            current_energy, current_state = self.run(alpha)

        finally:

            self.display(current_energy is 0, current_state)

    def run(self, alpha):

        iter_count = 2
        temp = 1000
        check_per_columns = False
        old_conflict_set = set()

        if len(trees_set) == 0:
            check_per_columns = True

        # place the initState randomly
        current_energy, conflict_set, current_state = self.generateRandomInitState(check_per_columns)
        old_conflict_set = conflict_set

        while True:

            if current_energy == 0 or temp < 0:
                break

            next_energy, conflict_set, next_state = self.generateNextRandomState(current_state, check_per_columns, old_conflict_set)
            delta_energy = next_energy - current_energy

            if delta_energy < 0:
                current_state = next_state
                current_energy = next_energy
                old_conflict_set = conflict_set

            else:

                if self.probabilityFunction(delta_energy, temp):
                    current_state = next_state
                    current_energy = next_energy
                    old_conflict_set = conflict_set

            temp = self.scheduleFuction(alpha, iter_count)
            iter_count += 1

            #print temp

        return current_energy, current_state

    def generateRandomInitState(self, check_per_column):

        inital_state = collections.deque()

        for i in range(self.number_of_lizards):
            if check_per_column:
                inital_state.append((random.randint(0, self.size_of_nursery - 1), i))
            else:
                inital_state.append(self.placeLizard(inital_state))

        energy,  conflict_set = self.getEnergy(inital_state)

        return energy, conflict_set, inital_state

    def generateNextRandomState(self, current_state, check_per_column, conflict_set):

        next_state = copy.deepcopy(current_state)
        (old_lizard_x, old_lizard_y) = random.sample(conflict_set, 1)[0]
        next_state.remove((old_lizard_x, old_lizard_y))

        #select_random_column = random.randint(0, len(next_state)-1)
        #(old_lizard_x, old_lizard_y) = next_state[select_random_column]

        next_lizard_x = random.randint(0, self.size_of_nursery - 1)
        next_lizard_y = random.randint(0, self.size_of_nursery - 1)

        if check_per_column:
            next_lizard_y = old_lizard_y

        while True:
            if (next_lizard_x, next_lizard_y) in current_state or (next_lizard_x, next_lizard_y) in self.trees_set:
                next_lizard_x = random.randint(0, self.size_of_nursery - 1)

                if not check_per_column:
                    next_lizard_y = random.randint(0, self.size_of_nursery - 1)

            else:
                break
        next_state.append((next_lizard_x, next_lizard_y))
        #next_state[select_random_column] = (next_lizard_x, next_lizard_y)

        energy, conflict_set = self.getEnergy(next_state)

        return energy, conflict_set, next_state

    def placeLizard(self, current_state):

        while True:
            col = random.randint(0, self.size_of_nursery - 1)
            row = random.randint(0, self.size_of_nursery - 1)

            if not (row, col) in current_state and not (row, col) in self.trees_set:
                return ((row, col))

    def getEnergy(self, state):

        no_attacking_lizards = 0
        row_move = [0, 1, 1, 1, 0, -1, -1, -1]
        column_move = [-1, -1, 0, 1, 1, 1, 0, -1]
        conflict_set = set()

        for lizard in state:

            for i in range(8):
                row_inc = row_move[i];
                column_inc = column_move[i];

                row_position = lizard[0] + row_inc;
                column_position = lizard[1] + column_inc;

                while (row_position >= 0 and row_position < self.size_of_nursery and
                               column_position >= 0 and column_position < self.size_of_nursery and
                           not ((row_position, column_position) in self.trees_set)):

                    if (row_position, column_position) in state:
                        conflict_set.add((row_position, column_position))
                        no_attacking_lizards += 1

                    row_position += row_inc
                    column_position += column_inc

        return no_attacking_lizards, conflict_set

    def probabilityFunction(self, delta_energy, temp):

        r = random.uniform(0, 1)
        expo_value = math.exp(-delta_energy / temp)

        if expo_value > r:
            return True
        else:
            return False

    def scheduleFuction(self, alpha, count):
        return alpha/math.log(count)

    def display(self, is_solution, position_set):
        a = ""
        if is_solution is False:
             result = "FAIL\n"
        else:
            result = "OK\n"
            for i in range(self.size_of_nursery):
                b = ""
                for j in range(self.size_of_nursery):

                    if (i, j) in self.trees_set:
                        a = a + "2"
                    elif (i, j) in position_set:
                        a = a + "1"
                    else:
                        a = a + "0"
                a = a + b + "\n"

        output_file = open("output.txt", "w")
        output_file.write(result+a)
        #print result+a
        output_file.close()

###########################DFS#######################


class DFS:

    size_of_nursery = 0
    number_of_lizards = 0
    trees_set = set()
    lizards_position_set = set()
    trees_hash_dequeue = {}
    trees_hash = {}

    def __init__(self, size_of_nursery, number_of_lizards, trees_set, trees_hash, trees_hash_dequeue):

        self.size_of_nursery = size_of_nursery
        self.number_of_lizards = number_of_lizards
        self.trees_set = trees_set
        self.trees_hash = trees_hash
        self.trees_hash_dequeue = trees_hash_dequeue

        for col in range(self.size_of_nursery):

            if col in self.trees_hash and len(self.trees_hash[col]) == self.size_of_nursery:
                continue

            if self.placeLizards(self.lizards_position_set, 0, col, 0):
                return self.display(True, self.lizards_position_set)


        return self.display(False, set())

    def placeLizards(self, lizards_position_set, row, col, ptr):

        if len(lizards_position_set) == self.number_of_lizards and col <= self.size_of_nursery:
            return True

        if col >= self.size_of_nursery or row > self.size_of_nursery:
            return False

        for i in range(row, self.size_of_nursery):

            if self.isLizardSafe(lizards_position_set, i, col):

                lizards_position_set.add((i, col))

                if col in self.trees_hash_dequeue and len(self.trees_hash_dequeue[col]) > ptr:

                    trees_row_deque = self.trees_hash_dequeue[col]
                    first_tree_pos = trees_row_deque[ptr]
                    ptr += 1

                    if first_tree_pos + 1 == self.size_of_nursery:

                        if self.placeLizards(lizards_position_set, 0, col + 1, 0) == True:
                            return True

                    else:

                        if self.placeLizards(lizards_position_set, first_tree_pos + 1, col, ptr) == True:
                            return True

                else:

                    if self.placeLizards(lizards_position_set, 0, col + 1, 0) == True:
                        return True

                lizards_position_set.remove((i, col))

            else:

                if (i, col) in self.trees_set:
                    ptr += 1

                    if self.isRestOfColumnHasTrees(ptr, i):
                        i = self.size_of_nursery - 1
                        return self.placeLizards(lizards_position_set, 0, col + 1, ptr)

            if i == self.size_of_nursery - 1:
                return self.placeLizards(lizards_position_set, 0, col + 1, 0)

        return False

    def isLizardSafe(self, all_possible_lizards_positions, row_no, column_no):

        if (row_no, column_no) in self.trees_set:
            return False

        row_move = [0, 1, -1]
        column_move = [-1, -1, -1]
        for i in range(3):
            row_inc = row_move[i]
            column_inc = column_move[i]

            row_position = row_no + row_inc
            column_position = column_no + column_inc

            while (row_position >= 0 and row_position < self.size_of_nursery and
                           column_position >= 0 and column_position < self.size_of_nursery and
                       not ((row_position, column_position) in self.trees_set)):

                if (row_position, column_position) in all_possible_lizards_positions:
                    return False

                row_position += row_inc
                column_position += column_inc

        return True

    def isRestOfColumnHasTrees(self, ptr, row):

        return (len(self.trees_set) - ptr) == row

    def display(self, is_solution, position_set):
        a = ""
        if is_solution is False:
            result = "FAIL\n"
        else:
            result = "OK\n"
            for i in range(self.size_of_nursery):
                b = ""
                for j in range(self.size_of_nursery):
                    if (i, j) in self.trees_set:
                        b = b + "2"
                    elif (i, j) in position_set:
                        b = b + "1"
                    else:
                        b = b + "0"

                a = a + b + "\n"

        output_file = open("output.txt", "w")
        output_file.write(result + a)
        #print result + a
        output_file.close()


###########################BFS#######################


class BFS(object):

    size_of_nursery = 0
    number_of_lizards = 0
    trees_set = set()

    def __init__(self, size_of_nursery, number_of_lizards, trees_set):

        self.size_of_nursery = size_of_nursery
        self.number_of_lizards = number_of_lizards
        self.trees_set = trees_set

        for start_column in range(size_of_nursery):

            lizards_position_set = set()
            queue = self.placeLizards(lizards_position_set, -1, start_column)

            for position_set in queue:

                if len(position_set) == self.number_of_lizards:
                    return self.display(True, position_set)


            for column in range(start_column+1, self.size_of_nursery):

                child_queue = []
                for lizards_position_set in queue:

                    updated_lizards_position_queue = self.placeLizards(lizards_position_set, -1, column)

                    if len(updated_lizards_position_queue) == 0:
                        updated_lizards_position_queue.append(lizards_position_set)

                    for position_set in updated_lizards_position_queue:
                        if len(position_set) == self.number_of_lizards:
                            return self.display(True, position_set)

                    child_queue += updated_lizards_position_queue

                if len(child_queue) != 0:
                    queue = child_queue

        return self.display(False, set())

    def cloneSet(self, lizards_position_set, row_no, col_no):

        new_lizards_position_set = copy.deepcopy(lizards_position_set)

        if row_no == -1 and col_no == -1:
            return new_lizards_position_set

        new_lizards_position_set.add((row_no, col_no))

        return new_lizards_position_set

    def placeLizards(self, lizards_position_set, row_no, column_no):

        queue = []
        #print "row",row_no,"col",column_no
        #self.display(True,lizards_position_set)
        #raw_input()

        for row in range(row_no + 1, self.size_of_nursery):

            if self.isLizardSafe(lizards_position_set, row, column_no):

                new_lizards_position_set = self.cloneSet(lizards_position_set, row, column_no)
                queue.append(new_lizards_position_set)
                if len(new_lizards_position_set) == self.number_of_lizards:
                    return queue

                queue += self.placeLizards(new_lizards_position_set, row, column_no)

        return queue

    def isLizardSafe(self, all_possible_lizards_positions, row_no, column_no):

        if (row_no, column_no) in self.trees_set:
            return False

        row_move =    [0,  1,  1, -1, -1]
        column_move = [-1, -1, 0,  0, -1]

        for i in range(5):
            row_inc = row_move[i];
            column_inc = column_move[i];

            row_position = row_no + row_inc;
            column_position = column_no + column_inc;

            while (row_position >= 0 and row_position < self.size_of_nursery and
                           column_position >= 0 and column_position < self.size_of_nursery and
                       not ((row_position, column_position) in self.trees_set)):

                if (row_position, column_position) in all_possible_lizards_positions:
                    return False

                row_position += row_inc
                column_position += column_inc

        return True

    def display(self, is_solution, position_set):
        a = ""
        if is_solution is False:
            result = "FAIL\n"
        else:
            result = "OK\n"
            for i in range(self.size_of_nursery):
                b = ""
                for j in range(self.size_of_nursery):

                    if (i, j) in self.trees_set:
                        a = a + '2'
                    elif (i, j) in position_set:
                        a = a + '1'
                    else:
                        a = a + '0'
                a += b + "\n"

        output_file = open("output.txt", "w")
        output_file.write(result + a)
        #print result + a
        output_file.close()

###########################MAIN#######################

#start_time = time.time()
try:
    #timer = 270
    #signal.signal(signal.SIGALRM, signal_handler)
    #ignal.alarm(timer)  # 4.5 seconds

    input_file = open("input.txt", 'r')
    output_file = open("output.txt",'w')
    output_file.write("FAIL\n")
    output_file.close()
    method = input_file.readline().split()

    size_of_nursery = int(input_file.readline())
    number_of_lizards = int(input_file.readline())

    trees_set = set()
    trees_hash = {}
    trees_hash_dequeue = {}

    for i in range(size_of_nursery):
        row = input_file.readline()
        int_row = list(row)
        for j in range(len(int_row)):
            if int_row[j] == '2':
                trees_set.add((i, j))
                if j in trees_hash:
                    trees_hash[j].append(i)
                    trees_hash_dequeue[j].append(i)
                else:
                    trees_hash[j] = [i]
                    trees_hash_dequeue[j] = collections.deque()
                    trees_hash_dequeue[j].append(i)

    if size_of_nursery == 0 or (size_of_nursery+len(trees_set) < number_of_lizards) or len(trees_set) == (size_of_nursery**2) or (size_of_nursery**2) - len(trees_set) < number_of_lizards:
        #print "FAIL"
        pass
    else:
        if method[0] in 'BFS':
            BFS(size_of_nursery, number_of_lizards, trees_set)
        elif method[0] in 'DFS':
            DFS(size_of_nursery, number_of_lizards, trees_set, trees_hash, trees_hash_dequeue)
        elif method[0] in 'SA':
            SA(size_of_nursery, number_of_lizards, trees_set)


except TimeoutError as exc:
    print "FAIL\n"
    pass
