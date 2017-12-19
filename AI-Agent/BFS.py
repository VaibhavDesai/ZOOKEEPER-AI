import copy


class BFS(object):

    def __init__(self, size_of_nursery, number_of_lizards, trees_set):
        self.size_of_nursery = size_of_nursery
        self.number_of_lizards = number_of_lizards
        self.trees_set = trees_set

        queue = []

        for start_column in range(size_of_nursery):
            queue = self.placeLizards(self.lizards_position_set, -1, start_column)
            for position_set in queue:
                if len(position_set) == self.number_of_lizards:
                    return True, position_set
            if len(queue) != 0:
                break

        for column in range(start_column + 1, self.size_of_nursery):

            child_queue = []

            for lizards_position_set in queue:

                updated_lizards_position_queue = self.placeLizards(lizards_position_set, -1, column)

                for position_set in updated_lizards_position_queue:
                    if len(position_set) == self.number_of_lizards:
                        return self.display(True, position_set)

                child_queue += updated_lizards_position_queue
            queue = child_queue

        return self.display(False, set())



    def cloneSet(self, lizards_position_set, row_no, col_no):

        new_lizards_position_set = copy.deepcopy(lizards_position_set)
        new_lizards_position_set.add((row_no, col_no))

        return new_lizards_position_set

    def placeLizards(self, lizards_position_set, row_no, column_no):

        queue = []
        for row in range(row_no + 1, self.size_of_nursery):

            if self.isLizardSafe(lizards_position_set, row, column_no):

                new_lizards_position_set = self.cloneSet(lizards_position_set, row, column_no)
                queue.append(new_lizards_position_set)
                queue += self.placeLizards(new_lizards_position_set, row, column_no)

        return queue


    def isLizardSafe(self, all_possible_lizards_positions, row_no, column_no):

        if (row_no, column_no) in self.trees_set:
            return False

        row_move = [0, 1, 1, 1, 0, -1, -1, -1]
        column_move = [-1, -1, 0, 1, 1, 1, 0, -1]

        for i in range(8):
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
