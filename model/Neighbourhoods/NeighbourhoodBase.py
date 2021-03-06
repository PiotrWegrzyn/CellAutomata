

class NeighbourhoodBase:
    def __init__(self, state, row, column, is_periodic=True):
        self.state = state
        self.row = row
        self.column = column
        self.is_periodic = is_periodic
        self.row_count = len(self.state)
        self.column_count = len(self.state[0])
        self.neighbours = []
        self.neighbour_states = []

        self._set_neighbours()
        self._set_neighbour_states()

    def get_neighbours_states(self):
        return self.neighbour_states

    def get_neighbours(self):
        return self.neighbours

    def _set_neighbour_states(self):
        self.neighbour_states = [cell.get_state() for cell in self.neighbours]

    def _set_neighbours(self):
        self._append_in_rect_area()

    def _append_in_rect_area(self, row_start=-1, row_end=1, column_start=-1, column_end=1):
        for row_offset in range(row_start, row_end+1):
            for column_offset in range(column_start, column_end+1):
                if row_offset is 0 and column_offset is 0:  # cell in the middle - the cell itself, not a neighbour
                    continue
                self._append_neighbour(row_offset, column_offset)

    def _append_neighbour(self, row_offset, column_offset):
        neighbour = self.get_neighbour(row_offset, column_offset)
        if neighbour:
            self.neighbours.append(neighbour)

    def get_neighbour(self, row_offset, col_offset):
        row = self.row + row_offset
        col = self.column + col_offset
        if self.is_periodic:
            return self.state[row % self.row_count][col % self.column_count]
        else:
            if row >= 0 and col >= 0:
                try:
                    return self.state[row][col]
                except IndexError:
                    return None
            return None

