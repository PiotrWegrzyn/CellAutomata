from model.BinaryCell import BinaryCell
from model.Rule import Rule


class BinaryRule(Rule):
    cell_type = BinaryCell
    required_dimension = 1

    def __init__(self, cell_automaton, rule):
        super().__init__(cell_automaton)
        self.rule = rule

    def apply(self, previous_triplet):
        rule_index = self.convert_from_binary_array_to_int(previous_triplet)
        return self.binary_rule[rule_index]

    def get_previous_neighbours(self, cell_column):
        previous_triplet = self._get_previous_triplet(cell_column)
        return previous_triplet

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

    def _get_previous_triplet(self, cell_column):
        previous_state = self.cell_automaton.get_previous_state()
        return [
            previous_state[(cell_column - 1)],
            previous_state[cell_column],
            previous_state[(cell_column + 1) % self.cell_automaton.get_columns_count()]
        ]
