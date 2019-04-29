import random

from model.Cells.BinaryCell import BinaryCell
from model.Cells.CellFactory import CellFactory
from model.RuleSets.RuleSet import RuleSet


class BinaryRuleSet(RuleSet):
    cell_type = BinaryCell
    required_dimension = 1

    def __init__(self, rule_base10):
        super().__init__()
        self.rule_base10 = rule_base10
        self._set_binary_rule()

    @staticmethod
    def get_cell_type():
        return BinaryRuleSet.cell_type

    def apply(self, previous_state, cell_column):
        prev_triplet_val = self.calculate_previous_triplet_value(previous_state, cell_column)
        new_state = self.determine_next_value(prev_triplet_val)
        return new_state

    def get_previous_neighbours(self, previous_state, cell_column):
        previous_triplet = self._get_previous_triplet(previous_state, cell_column)
        return previous_triplet

    def create_cell(self, value):
        if value is 0:
            return self.cell_factory.create_dead_cell()
        else:
            return self.cell_factory.create_random_alive_cell()

    def calculate_previous_triplet_value(self, previous_state, cell_column):
        previous_triplet = self.get_previous_neighbours(previous_state, cell_column)
        binary_array = [cell.get_state() for cell in previous_triplet]
        return self.convert_from_binary_array_to_int(binary_array)

    @staticmethod
    def convert_from_binary_array_to_int(binary_array):
        # generates a string array from array of ints
        # joins the array into empty string
        # converts to int base10 from base2
        # all in one line
        # python is beautiful
        # todo refactor
        return int(''.join(str(one_or_zero) for one_or_zero in binary_array), 2)

    def _set_binary_rule(self):
        self.rule_base2 = list(reversed(self.binary_array_from_int(self.rule_base10)))

    def binary_array_from_int(self, integer):
        return [int(x) for x in list(self._binary8b_string_from_int(integer))]

    @staticmethod
    def _binary8b_string_from_int(integer):
        return '{0:08b}'.format(integer)

    def _get_previous_triplet(self, previous_state, cell_column):
        size = len(previous_state)
        return [
            previous_state[(cell_column - 1)],
            previous_state[cell_column],
            previous_state[(cell_column + 1) % size]
        ]

    def determine_next_value(self, previous_state_index):
        # After converting the rule from base 10 to base 2 each index
        # represents a different state in previous iteration
        # so after we determine which state it was we use it's
        # combination's value to look up the index of the rule
        # and get the 0 or 1 that it holds - that is the state in the next iteration
        return self.rule_base2[previous_state_index]

    def get_rule_base_10(self):
        return self.rule_base10

    def __str__(self):
        return "Rule " + self.rule_base10.__str__()

    @staticmethod
    def get_required_dimension():
        return BinaryRuleSet.required_dimension

    def get_initial_random_state(self, number_of_alive_cells, columns, rows=None):
        initial_state = self._prepare_initial_dead_cells(columns)
        self._prepare_initial_alive_cells(initial_state, number_of_alive_cells, columns)
        return initial_state

    def _prepare_initial_dead_cells(self, columns):
        empty_state =[]
        for c in range(0,columns):
            empty_state.append(self.cell_factory.create_dead_cell())
        return empty_state

    def _prepare_initial_alive_cells(self, initial_state, number_of_alive_cells, columns):
        for i in range(0, number_of_alive_cells):
            while True:
                y = random.randrange(0, columns)
                if initial_state[y].is_dead():
                    initial_state[y] = self.cell_factory.create_random_alive_cell()
                    break

