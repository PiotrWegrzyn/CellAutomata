import random
from multiprocessing.pool import ThreadPool


def generate_empty_2d_list_of_list(size):
    return [[] for i in range(0, size)]


class CellularAutomaton:
    modes = {
        "1D": 1,
        "2D": 2
    }

    def __init__(self, mode, rows_count, columns_count, rule=None, percentage_of_alive_cells=0.3, initial_data=None):

        self.mode = mode
        # for now only a square
        self.rows_count = rows_count
        self.columns_count = columns_count
        self.number_of_alive_cells = 0
        self.percentage_of_alive_cells = 0
        self.set_percent_of_alive_cells(percentage_of_alive_cells)
        self._set_number_of_alive_cells()

        self.initial_data = initial_data
        self.initial_state = []
        self._prepare_initial_state()

        self.previous_state = []
        self.current_state = []

        self.set_to_initial_state()

        if rule is not None:
            self.rule = rule
            self.binary_rule = []
            self._set_binary_rule()

        self.print_stats()

    def calculate_next_iteration(self):
        self.previous_state = self.current_state
        self._reset_current_state()
        self._set_cells()

    def _apply_rule(self, cell_index, cell_row=None):
        apply_rule_method = self.get_apply_rule_method()
        return apply_rule_method(cell_row=cell_row, cell_index=cell_index)

    def _judgement_day(self, is_alive, neighbours_value):
        if is_alive and neighbours_value < 2:
            return self._die()

        if is_alive and neighbours_value in [2, 3]:
            return is_alive

        if is_alive and neighbours_value > 3:
            return self._die()

        if not is_alive and neighbours_value is 3:
            return self._resurrect()

        return self._die()

    def _get_previous_triplet(self, index):
        return [
            self.previous_state[(index - 1)],
            self.previous_state[index],
            self.previous_state[(index + 1) % self.rows_count]
        ]

    def _get_neighbour_values(self,row, index):
        return [
            self.previous_state[(row-1)][index-1], self.previous_state[(row-1)][index], self.previous_state[(row-1)][(index+1) % self.columns_count],
            self.previous_state[row][index-1], self.previous_state[row][(index+1) % self.columns_count],
            self.previous_state[(row+1) % self.rows_count][index-1], self.previous_state[(row+1) % self.rows_count][index], self.previous_state[(row+1) % self.rows_count][(index+1) % self.columns_count],
        ]

    @staticmethod
    def convert_from_binary_array_to_int(binary_array):
        # generates a string array from array of ints
        # joins the array into empty string
        # converts to int base10 from base2
        # all in one line
        # python is beautiful
        return int(''.join(str(one_or_zero) for one_or_zero in binary_array), 2)

    def _set_binary_rule(self):
        self.binary_rule = list(reversed(self.binary_array_from_int(self.rule)))

    def binary_array_from_int(self, integer):
        return [int(x) for x in list(self._binary8b_string_from_int(integer))]

    @staticmethod
    def _binary8b_string_from_int(integer):
        return '{0:08b}'.format(integer)

    def _append_cell(self, cell_index, cell_row=None):
        if self.mode is self.modes['1D']:
            self.current_state.append(self._apply_rule(cell_index))
        if self.mode is self.modes['2D']:
            self.current_state[cell_row].append(self._apply_rule(cell_index, cell_row))

    def _prepare_initial_state(self):
        self._prepare_initial_dead_cells()
        self._prepare_initial_alive_cells()

    def get_current_state(self):
        return self.current_state

    def print_current_state(self):
        if self.mode is self.modes['1D']:
            print(self.current_state)
        if self.mode is self.modes['2D']:
            for row in range(0, self.rows_count):
                print(self.current_state[row])

    def print_iterations(self, iterations):
        print(iterations)
        print("Iteration: 0")
        self.print_current_state()
        for i in range(1, iterations):
            print("Iteration: " + i.__str__())
            self.calculate_next_iteration()
            self.print_current_state()

    def iterations_to_list(self, iterations):
        list = generate_empty_2d_list_of_list(iterations)
        list[0] = self.current_state
        for i in range(1, iterations):
            self.calculate_next_iteration()
            list[i] = self.current_state
        return list

    def print_stats(self):
        print("Mode: " + self.mode.__str__())
        print("Size: " + self.rows_count.__str__())
        print("Size: " + self.columns_count.__str__())
        try:
            print("Rule: " + self.rule.__str__())
        except AttributeError:
            pass

    def _prepare_initial_alive_cells(self):
        self._set_number_of_alive_cells()
        if self.mode is self.modes["1D"]:
            for i in range(0, self.number_of_alive_cells):
                while True:
                    y = random.randrange(0, self.columns_count)
                    if self.initial_state[y] is not 1:
                        self.initial_state[y] = 1
                        break
        if self.mode is self.modes["2D"]:
            for i in range(0, self.number_of_alive_cells):
                while True:
                    x = random.randrange(0, self.rows_count)
                    y = random.randrange(0, self.columns_count)
                    if self.initial_state[x][y] is not 1:
                        self.initial_state[x][y] = 1
                        break

    def _set_rule(self, rule):
        self.rule = rule
        self._set_binary_rule()

    def _set_size(self, x, y):
        self.rows_count = x
        self.columns_count = y

    def _set_cells(self):
        if self.mode is self.modes['1D']:
            for cell_index in range(0, self.rows_count):
                self._append_cell(cell_index)
        if self.mode is self.modes['2D']:
            pool = ThreadPool(int(self.rows_count/10))
            pool.map(self.set_cells_in_row, [cell_row for cell_row in range(0, self.rows_count)])
            pool.close()
        self.update_alive_cells()

    def set_cells_in_row(self, cell_row):
        for cell_index in range(0, self.columns_count):
            self._append_cell(cell_index, cell_row)

    def _get_cell_previous_value(self, cell_row, cell_index):
        return self.previous_state[cell_row][cell_index]

    def _die(self):
        return 0

    def _resurrect(self):
        return 1

    def _reset_current_state(self):
        if self.mode is self.modes['1D']:
           self.current_state=[]
        if self.mode is self.modes['2D']:
            self.current_state = generate_empty_2d_list_of_list(self.rows_count)

    def _set_number_of_alive_cells(self):
        if self.mode is self.modes['1D']:
            self.number_of_alive_cells = int(self.columns_count*self.percentage_of_alive_cells)
        if self.mode is self.modes['2D']:
            self.number_of_alive_cells = int(self.rows_count * self.columns_count * self.percentage_of_alive_cells)

    def set_percent_of_alive_cells(self, percent):
        self.percentage_of_alive_cells = percent
        self._set_number_of_alive_cells()

    def set_to_initial_state(self):
        self.current_state = self.initial_state

    def _prepare_initial_dead_cells(self):
        if self.mode is self.modes["1D"]:
            self.initial_state = [0] * self.columns_count
        if self.mode is self.modes["2D"]:
            self.initial_state = [[0] * self.columns_count for i in range(0, self.rows_count)]

    def change_size(self, rows_count, columns_count):
        self._set_size(rows_count, columns_count)
        self._prepare_initial_state()
        self.set_to_initial_state()

    def change_rule(self, rule):
        self._set_rule(rule)
        self._prepare_initial_state()
        self.set_to_initial_state()

    def get_rule(self):
        return self.rule

    def get_rows_count(self):
        return self.rows_count

    def get_columns_count(self):
        return self.columns_count

    def change_alive_cells_percentage(self, percentage_of_alive_cells):
        self.set_percent_of_alive_cells(round(percentage_of_alive_cells, 2))
        self._set_number_of_alive_cells()
        self._prepare_initial_state()
        self.set_to_initial_state()

    def get_apply_rule_method(self):
        if self.mode is self.modes['1D']:
            return self.apply_1d_rule
        if self.mode is self.modes['2D']:
            return self.apply_game_of_life_rules

    def apply_1d_rule(self, cell_index, **kwargs):
        previous_triplet = self._get_previous_triplet(cell_index)
        rule_index = self.convert_from_binary_array_to_int(previous_triplet)
        return self.binary_rule[rule_index]

    def apply_game_of_life_rules(self, cell_row, cell_index):
        previous_neighbours_values = self._get_neighbour_values(cell_row, cell_index)
        cell_value = self._get_cell_previous_value(cell_row, cell_index)
        return self._judgement_day(cell_value, sum(previous_neighbours_values))

    def get_alive_cell_percentage(self):
        return self.percentage_of_alive_cells

    def set_cell(self, value, column, row=None):
        if self.mode is self.modes['1D']:
            self.current_state[column] = value
        if self.mode is self.modes['2D']:
            self.current_state[row][column] = value

    def update_alive_cells(self):
        s = 0
        if self.mode is self.modes['1D']:
            s += sum(self.current_state)
        if self.mode is self.modes['2D']:
            for row in range(0, self.rows_count):
                s += sum(self.current_state[row])
        self.number_of_alive_cells = s
        self._set_alive_cells_percentage()

    def _set_alive_cells_percentage(self):
        if self.mode is self.modes['1D']:
            self.percentage_of_alive_cells = round(self.number_of_alive_cells/self.columns_count, 2)
        if self.mode is self.modes['2D']:
            self.percentage_of_alive_cells = round(self.number_of_alive_cells/(self.rows_count*self.columns_count), 2)

