

class NeighborhoodInterface:
    def __init__(self, state, row, column, is_periodic=True):
        self.state = state
        self.row = row
        self.column = column
        self.is_periodic = is_periodic
        self.row_count = len(self.state)
        self.column_count = len(self.state[0])
        self.prev_neighbour_states = []

        self._set_prev_neighbour_states()

    def get_prev_neighbours_states(self):
        return self.prev_neighbour_states

    def _set_prev_neighbour_states(self):
        pass
