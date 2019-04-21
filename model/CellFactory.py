
class CellFactory:
    def create_dead_cell(self, cell_type):
        if not isinstance(cell_type, type):
            raise ValueError
        state = cell_type.get_dead_state()
        return cell_type(state)

    def create_random_alive_cell(self, cell_type):
        if not isinstance(cell_type, type):
            raise ValueError
        return cell_type(cell_type.get_random_alive_state())


