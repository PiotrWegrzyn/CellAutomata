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

    def __init__(self):
        self.cell_factory = CellFactory(self.cell_type)

    def apply(self, previous_state, cell_column):
        pass

    def get_cell_type(self):
        return self.cell_type

    def get_required_dimension(self):
        return self.required_dimension

    def get_dead_cell(self):
        return self.cell_type.get_dead_state()

