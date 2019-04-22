from model.Cells.BinaryCell import BinaryCell
from model.RuleSets.RuleSet import RuleSet


class GameOfLifeRuleSet(RuleSet):
    cell_type = BinaryCell
    required_dimension = 2

    def apply(self, previous_state, cell_row, cell_column):
        judged_cell = previous_state[cell_row][cell_column]
        previous_neighbours_values = self.get_previous_neighbours_values(previous_state, cell_row, cell_column)

        return self._judgement_day(judged_cell, sum(previous_neighbours_values))

    def create_cell(self, value):
        if value is 0:
            return self.cell_factory.create_dead_cell(self.cell_type)
        else:
            return self.cell_factory.create_random_alive_cell(self.cell_type)

    def get_previous_neighbours_values(self, previous_state, cell_row, cell_column):
        # todo refactor this *somehow*
        rows_count = len(previous_state)
        columns_count = len(previous_state[0])
        return [
            previous_state[(cell_row - 1)][cell_column - 1].get_value(),
            previous_state[(cell_row - 1)][cell_column].get_value(),
            previous_state[(cell_row - 1)][(cell_column + 1) % columns_count].get_value(),

            previous_state[cell_row][cell_column - 1].get_value(),
            previous_state[cell_row][(cell_column + 1) % columns_count].get_value(),

            previous_state[(cell_row + 1) % rows_count][cell_column - 1].get_value(),
            previous_state[(cell_row + 1) % rows_count][cell_column].get_value(),
            previous_state[(cell_row + 1) % rows_count][(cell_column + 1) % columns_count].get_value()
        ]

    def _judgement_day(self, cell, neighbours_value):
        if cell.is_alive() and neighbours_value < 2:
            return self.cell_factory.create_dead_cell()

        if cell.is_alive() and neighbours_value in [2, 3]:
            return cell

        if cell.is_alive() and neighbours_value > 3:
            return self.cell_factory.create_dead_cell()

        if cell.is_dead() and neighbours_value is 3:
            return self.cell_factory.create_random_alive_cell()

        return self.cell_factory.create_dead_cell()
