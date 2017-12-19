import random
import math
import collections
import signal
import copy


class SA(object):

    size_of_nursery = 0
    number_of_lizards = 0
    trees_set = set()

    def __init__(self, size_of_nursery, number_of_lizards, trees_set):
        self.size_of_nursery = size_of_nursery
        self.number_of_lizards = number_of_lizards
        self.trees_set = trees_set

        temp = 1000.0
        alpha = 0.9
        step_count_inc = 1.000005
        step_count = 1
        iter_count = 0
        temp_values = list()
        temp_values.append(str(temp))

        # place the initState randomly
        current_energy, current_state = self.generateRandomInitState()
        try:
            signal.signal(signal.SIGALRM, self.signal_handler)
            signal.alarm(270)  # 4.5 seconds

            while True:

                if current_energy == 0 or temp < 0:
                    break

                next_energy, next_state = self.generateNextRandomState(current_state)
                delta_energy = next_energy - current_energy

                if delta_energy < 0:
                    current_state = next_state
                    current_energy = next_energy

                else:
                    if self.probabilityFunction(delta_energy, temp):
                        current_state = next_state
                        current_energy = next_energy

                temp = self.scheduleFuction(temp, alpha, step_count)
                temp_values.append(str(temp))
                step_count *= step_count_inc
                iter_count += 1

        finally:
            #Timed Out
            self.display(current_energy is 0, current_state)


    def generateRandomInitState(self):
        inital_state = collections.deque()
        for i in range(self.number_of_lizards):
            inital_state.append((self.placeLizard(inital_state)))

        return self.getEnergy(inital_state), inital_state

    def generateNextRandomState(self, current_state):

        next_state = copy.deepcopy(current_state)
        next_lizard_x = random.randint(0, self.number_of_lizards - 1)
        next_lizard_y = random.randint(0, self.number_of_lizards - 1)

        while True:
            if (next_lizard_x, next_lizard_y) in current_state or (next_lizard_x, next_lizard_y) in self.trees_set:
                next_lizard_x = random.randint(0, self.number_of_lizards - 1)
                next_lizard_y = random.randint(0, self.number_of_lizards - 1)
            else:
                break

        select_random_lizard_index = random.randint(0, self.number_of_lizards - 1)
        next_state[select_random_lizard_index] = (next_lizard_x, next_lizard_y)

        return self.getEnergy(next_state), next_state

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
                        no_attacking_lizards += 1

                    row_position += row_inc
                    column_position += column_inc

        return no_attacking_lizards

    def probabilityFunction(self, delta_energy, temp):

        r = random.uniform(0, 1)
        expo_value = math.exp(-delta_energy / temp)

        if expo_value > r:
            return True
        else:
            return False

    def scheduleFuction(self, t0, alpha, step_count):
        return t0 * (alpha ** step_count)

    def signal_handler(self, signum, frame):
        return
