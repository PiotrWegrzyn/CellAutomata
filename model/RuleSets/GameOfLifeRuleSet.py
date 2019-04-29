import random

from model.Cells.BinaryCell import BinaryCell
from model.RuleSets.RuleSet import RuleSet
import re


class GameOfLifeRuleSet(RuleSet):
    cell_type = BinaryCell
    required_dimension = 2

    def __init__(self, rule_code="B3/23S"):
        super().__init__()
        self.decode(rule_code)

    def apply(self, previous_state, cell_row, cell_column):
        judged_cell = previous_state[cell_row][cell_column]
        previous_neighbours_values = self.get_previous_neighbours_state(previous_state, cell_row, cell_column)
        self._judgement_day(judged_cell, sum(previous_neighbours_values))

    def create_cell(self, value):
        if value is 0:
            return self.cell_factory.create_dead_cell(self.cell_type)
        else:
            return self.cell_factory.create_random_alive_cell(self.cell_type)

    def get_previous_neighbours_state(self, previous_state, cell_row, cell_column):
        # todo refactor this *somehow*
        rows = len(previous_state)
        columns = len(previous_state[0])
        return [
            previous_state[(cell_row - 1)][cell_column - 1].get_state(),
            previous_state[(cell_row - 1)][cell_column].get_state(),
            previous_state[(cell_row - 1)][(cell_column + 1) % columns].get_state(),

            previous_state[cell_row][cell_column - 1].get_state(),
            previous_state[cell_row][(cell_column + 1) % columns].get_state(),

            previous_state[(cell_row + 1) % rows][cell_column - 1].get_state(),
            previous_state[(cell_row + 1) % rows][cell_column].get_state(),
            previous_state[(cell_row + 1) % rows][(cell_column + 1) % columns].get_state()
        ]

    def _judgement_day(self, cell, neighbours_value):
        if cell.is_alive() and neighbours_value in self.survive_conditions:
            pass
        elif cell.is_dead() and neighbours_value in self.born_conditions:
            cell.resurrect()
        else:
            cell.die()

    @staticmethod
    def get_cell_type():
        return GameOfLifeRuleSet.cell_type

    @staticmethod
    def get_required_dimension():
        return GameOfLifeRuleSet.required_dimension

    def get_initial_random_state(self, number_of_alive_cells, columns, rows=None):
        initial_state = self._prepare_initial_dead_cells(rows, columns)
        self._prepare_initial_alive_cells(initial_state, number_of_alive_cells, rows, columns)
        return initial_state

    def _prepare_initial_alive_cells(self, initial_state, number_of_alive_cells, rows, columns):
        for i in range(0, number_of_alive_cells):
            while True:
                x = random.randrange(0, rows)
                y = random.randrange(0, columns)
                if initial_state[x][y].is_dead():
                    initial_state[x][y] = self.cell_factory.create_random_alive_cell()
                    break

    def _prepare_initial_dead_cells(self, rows, columns):
        clear_state = []
        for r in range(0, rows):
            row = []
            for c in range(0, columns):
                row.append(self.cell_factory.create_dead_cell())
            clear_state.append(row)
        return clear_state

    def decode(self, rule_code):
        self.born_conditions = self.get_born_conditions(rule_code)
        self.survive_conditions = self.get_survive_condition(rule_code)

    def get_born_conditions(self, rule_code):
        return [int(condition) for condition in re.sub("\D", "", rule_code.split("/")[0])]

    def get_survive_condition(self, rule_code):
        return [int(condition) for condition in re.sub("\D", "", rule_code.split("/")[1])]

