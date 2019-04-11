class CellularAutomaton:

    def __init__(self, size, rule, number_of_ones=1):
        self.size = size
        self.number_of_ones = number_of_ones

        self.previous_state = []
        self.current_state = []
        self.set_initial_state()

        self.rule = rule
        self.binary_rule = []
        self._set_binary_rule()

        self.print_stats()

    def calculate_next_iteration(self):
        self.previous_state = self.current_state
        self.current_state = []
        for cell_index in range(0, self.size):
            self._set_cell(cell_index)

    def _apply_rule(self, cell_index):
        previous_triplet = self._get_previous_triplet(cell_index)
        rule_index = self.convert_from_binary_array_to_int(previous_triplet)
        return self.binary_rule[rule_index]

    def _get_previous_triplet(self, index):
        return [
            self.previous_state[(index - 1)],
            self.previous_state[index],
            self.previous_state[(index + 1) % self.size]
        ]

    @staticmethod
    def convert_from_binary_array_to_int(binary_array):
        return int(''.join(str(e) for e in binary_array), 2)

    def _set_binary_rule(self):
        self.binary_rule = list(reversed(self.binary_array_from_int(self.rule)))

    def binary_array_from_int(self, integer):
        return [int(x) for x in list(self._binary8b_string_from_int(integer))]

    @staticmethod
    def _binary8b_string_from_int(integer):
        return '{0:08b}'.format(integer)

    def _set_cell(self, cell_index):
        self.current_state.append(self._apply_rule(cell_index))

    def set_initial_state(self):
        self.current_state = [0] * self.size
        self.set_initial_ones()

    def get_current_state(self):
        return self.current_state

    def print_rows(self, rows):
        print(self.current_state)
        for i in range(0, rows):
            self.calculate_next_iteration()
            print(self.current_state)
        self.set_initial_state()

    def print_stats(self):
        print("Size: " + self.size.__str__())
        print("Rule: " + self.rule.__str__())
        print("Current state: " + self.current_state.__str__())

    def set_initial_ones(self):
        if self.number_of_ones > int(self.size / 2):
            self.number_of_ones = int(self.size / 2)
        middle = int(self.size/2)
        for i in range(middle, middle+self.number_of_ones):
            self.current_state[i] = 1

    def set_rule(self, rule):
        self.rule = rule
        self._set_binary_rule()
