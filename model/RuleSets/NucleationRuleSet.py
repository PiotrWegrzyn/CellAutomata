import random

from model.Cells.CrystalGrainCell import CrystalGrainCell
from model.Neighbourhoods.Moore import Moore
from model.RuleSets.RuleSet import RuleSet


class NucleationRuleSet(RuleSet):
    cell_type = CrystalGrainCell
    required_dimension = 2
    initial_alive_cells = 0.01
    initial_iteration_speed = 2

    def __init__(self, initial_mode="random", is_periodic=True):
        super(NucleationRuleSet, self).__init__()
        self.is_periodic = is_periodic
        self.initial_mode = initial_mode

    def apply(self, previous_state, current_state, cell_row, cell_column):
        judged_cell = previous_state[cell_row][cell_column]
        if judged_cell.is_dead():
            previous_neighbours_states = self.get_previous_neighbours_values(previous_state, cell_row, cell_column)
            previous_neighbours_grain_ids = [state.grain_id for state in previous_neighbours_states]
            previous_grains_type_count = self.get_grain_type_count(previous_neighbours_grain_ids)
            try:
                most_common_grain_id = self.get_most_common_grain_id(previous_grains_type_count)
                current_state[cell_row][cell_column].state.grain_id = most_common_grain_id
            except ValueError:
                self.no_grains_surrounding()

    def get_previous_neighbours_values(self, previous_state, cell_row, cell_column):
        prev_neighbours_states = Moore(previous_state, cell_row, cell_column, self.is_periodic).get_prev_neighbours_states()
        return prev_neighbours_states

    @staticmethod
    def get_required_dimension():
        return NucleationRuleSet.required_dimension

    @staticmethod
    def get_cell_type():
        return NucleationRuleSet.cell_type

    def get_grain_type_count(self, previous_neighbours_values):
        distinct_neighbours_ids = self.get_distinct_grain_ids(previous_neighbours_values)
        return {v: previous_neighbours_values.count(v) for v in distinct_neighbours_ids}

    def get_distinct_grain_ids(self, previous_neighbours_values):
        distinct_neighbours_ids = set(previous_neighbours_values)
        try:
            distinct_neighbours_ids.remove(0)     # 0 is the indicator that cell is dead
        except KeyError:
            pass
        return distinct_neighbours_ids

    def get_most_common_grain_id(self, previous_grains_type_count):
        return max(previous_grains_type_count, key=lambda key: previous_grains_type_count[key])

    def get_initial_random_state(self, number_of_alive_cells, columns, rows=None):
        initial_state = self._prepare_initial_dead_cells(rows, columns)
        self._prepare_initial_alive_cells(initial_state, number_of_alive_cells, rows, columns)
        return initial_state

    def _prepare_initial_alive_cells(self, initial_state, number_of_alive_cells, rows, columns):
        if self.initial_mode is "random":
            self._prepare_random_alive_cells(initial_state, number_of_alive_cells, rows, columns)
        elif self.initial_mode is "equal_spread":
            self._prepare_equaly_spread_alive_cells(initial_state, rows, columns)

    def _prepare_initial_dead_cells(self, rows, columns):
        clear_state = []
        for r in range(0, rows):
            row = []
            for c in range(0, columns):
                row.append(self.cell_factory.create_dead_cell())
            clear_state.append(row)
        return clear_state

    def no_grains_surrounding(self):
        pass

    def _prepare_random_alive_cells(self, initial_state, number_of_alive_cells, rows, columns):
        for i in range(0, number_of_alive_cells):
            while True:
                x = random.randrange(0, rows)
                y = random.randrange(0, columns)
                if initial_state[x][y].is_dead():
                    initial_state[x][y].state = CrystalGrainCell.State(grain_id=CrystalGrainCell.get_new_grain_id())
                    break

    def _prepare_equaly_spread_alive_cells(self, initial_state, rows, columns):
        for row in range(0, rows):
            if row % 3 is 0:
                for column in range(0, columns):
                    if column % 3 is 0:
                        initial_state[row][column].state = CrystalGrainCell.State(grain_id=CrystalGrainCell.get_new_grain_id())


