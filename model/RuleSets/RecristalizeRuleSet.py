from model.Cells.CrystalGrainCell import CrystalGrainCell
from model.RuleSets.RuleSet import RuleSet


class NucleationRuleSet(RuleSet):
    cell_type = CrystalGrainCell
    required_dimension = 2

    def apply(self, previous_state, current_state, cell_row, cell_column):
        judged_cell = previous_state[cell_row][cell_column]
        if judged_cell.is_dead():
            previous_neighbours_values = self.get_previous_neighbours_values(previous_state, cell_row, cell_column)
            previous_grains_type_count = self.get_grain_type_count(previous_neighbours_values)
            try:
                most_common_grain_id = self.get_most_common_grain_id(previous_grains_type_count)
                current_state[cell_row][cell_column].state = most_common_grain_id
            except ValueError:
                self.no_grains_surrounding()

    def get_previous_neighbours_values(self, previous_state, cell_row, cell_column):
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
        for i in range(0, number_of_alive_cells):
            while True:
                x = random.randrange(0, rows)
                y = random.randrange(0, columns)
                if initial_state[x][y].is_dead():
                    initial_state[x][y].state = CrystalGrainCell.get_new_grain_id()
                    break

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

