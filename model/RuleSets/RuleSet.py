from model.Cells.Cell import Cell
from model.Cells.CellFactory import CellFactory


class RuleSet:
    dimensions = {
        "1D": 1,
        "2D": 2
    }
    cell_type = Cell
    required_dimension = None
    allow_dead_cells = True
    initial_alive_cells = 0
    initial_iteration_speed = 1

    def __init__(self, radius=4):
        self.cell_factory = CellFactory(self.get_cell_type())
        self.reverse_colors = False
        self.radius = radius

    def __str__(self):
        return self.__class__.__name__

    def apply(self, previous_state, cell_column):
        pass

    def get_initial_state(self, number_of_alive_cells, columns, rows=None):
        pass

    @staticmethod
    def get_cell_type():
        return RuleSet.cell_type

    @staticmethod
    def get_required_dimension():
        return RuleSet.required_dimension

    def get_dead_cell(self):
        return self.cell_type.get_dead_state()

    def apply_pre_iteration(self, previous_state, current_state):
        pass

    def apply_post_iteration(self, previous_state, current_state):
        pass

