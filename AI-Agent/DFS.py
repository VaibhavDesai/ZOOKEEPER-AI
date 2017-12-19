import sys
import collections


sys.setrecursionlimit(1000000000)
orig_stdout = sys.stdout


class DFS:

    size_of_nursery = 0
    number_of_lizards = 0
    trees_set = set()
    trees_hash = {}
    trees_hash_dequeue = {}
    lizards_position_set = set()

    def __init__(self, size_of_nursery, number_of_lizards, trees_set):
        self.size_of_nursery = size_of_nursery
        self.number_of_lizards = number_of_lizards
        self.trees_set = trees_set

        self.trees_hash = self.createHash(trees_set)
        self.trees_deque = self.createDeque(trees_set)

        for col in range(self.size_of_nursery):

            if col in self.trees_hash and len(self.trees_hash[col]) == self.size_of_nursery:
                continue

            if self.placeLizards(self.lizards_position_set, 0, col, 0):
                self.display(True, self.lizards_position_set)

            else:
                self.display(False, set())


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

    def createHashAndDequeue(self, trees_set):

        trees_hash = {}
        trees_hash_dequeue = collections.deque()

        for trees in trees_set:

            if not trees[1] in trees_hash:
                trees_hash[trees[1]] = [trees[0]]
                trees_hash_dequeue[trees[1]] = collections.deque()
                trees_hash_dequeue[trees[1]].append(trees[0])
            else:
                trees_hash[trees[1]].append(trees[0])
                trees_hash_dequeue[trees[1]].append(trees[0])

        return trees_hash, trees_hash_dequeue

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


    def display(self, result, position_set):

        if result is False:
            print "FAIL"
        else:
            print "OK"
            for i in range(self.size_of_nursery):
                a = ""
                for j in range(self.size_of_nursery):

                    if (i, j) in self.trees_set:
                        a = a + "2"
                    elif (i, j) in position_set:
                        a = a + "1"
                    else:
                        a = a + "0"
                print(a)

