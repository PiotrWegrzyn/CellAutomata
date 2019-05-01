from model.Cells.CrystalGrainCell import CrystalGrainCell
from model.RuleSets.NucleationRuleSet import NucleationRuleSet


class RecristalizationRuleSet(NucleationRuleSet):
    cell_type = CrystalGrainCell
    required_dimension = 2

    def __init__(self, iteration=0):
        super().__init__()
        self.iteration = iteration

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


