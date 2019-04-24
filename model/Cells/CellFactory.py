
class CellFactory:
    def __init__(self, cell_type):
        if not isinstance(cell_type, type):
            raise ValueError
        self.cell_type = cell_type

    def change_cell_type(self, new_cell_type):
        self.cell_type = new_cell_type

    def create_dead_cell(self):
        state = self.cell_type.get_dead_state()
        return self.cell_type(state)

    def create_random_alive_cell(self):
        return self.cell_type(self.cell_type.get_random_alive_state())

    def create_cell_with_values(self, value=None, **kwargs):
        return self.cell_type(self.cell_type.get_state_from_values(value, **kwargs))

