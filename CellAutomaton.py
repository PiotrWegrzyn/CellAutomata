class CellularAutomaton:

    def __init__(self, size, rule, number_of_ones=1):
        self.size = size
        self.previous_state = []
        self.number_of_ones = number_of_ones
        self.current_state = self.set_initial_state()
        self.rule = rule
        self.binary_rule = self.set_binary_rule()

    def calculate_next(self):
        self.previous_state = self.current_state
        self.current_state = []
        for cell_index in range(0, self.size):
            self._set_cell(cell_index)

    def apply_rule(self, cell_index):
        previous_triplet = self.get_previous_triplet(cell_index)
        rule_index = self.convert_from_binary_array_to_int(previous_triplet)
        return self.binary_rule[rule_index]

    def get_previous_triplet(self, index):
        return [
            self.previous_state[(index - 1)],
            self.previous_state[index],
            self.previous_state[(index + 1) % self.size]
        ]

    @staticmethod
    def convert_from_binary_array_to_int(binary_array):
        return int(''.join(str(e) for e in binary_array), 2)

    def set_binary_rule(self):
        return list(reversed(self.binary_array_from_int(self.rule)))

    def binary_array_from_int(self, integer):
        return [int(x) for x in list(self.binary8b_string_from_int(integer))]

    @staticmethod
    def binary8b_string_from_int(integer):
        return '{0:08b}'.format(integer)

    def _set_cell(self, cell_index):
        self.current_state.append(self.apply_rule(cell_index))

    def set_initial_state(self):
        if self.number_of_ones > int(self.size / 2):
            self.number_of_ones = int(self.size / 2)
        return [0] * int(self.size / 2) + [1] * self.number_of_ones + [0] * (int(self.size / 2) - self.number_of_ones)

    def print_rows(self, rows):
        print(self.current_state)
        for i in range(0, rows):
            self.calculate_next()
            print(self.current_state)
        self.current_state = self.set_initial_state()

