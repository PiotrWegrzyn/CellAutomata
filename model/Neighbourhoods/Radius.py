from model.Neighbourhoods.NeighbourhoodInterface import NeighborhoodInterface


class Radius(NeighborhoodInterface):
    def __init__(self, state, row, column, is_periodic, radius):
        self.radius = radius
        super().__init__(state, row, column, is_periodic)

    def _set_prev_neighbour_states(self):
        for row_offset in range(-self.radius, self.radius+1):
            for column_offset in range(-self.radius, self.radius + 1):
                if self.is_in_radius(row_offset, column_offset):
                    self._append_neighbour_state(row_offset, column_offset)

    def is_in_radius(self, x_distance_from_center, y_distance_from_center):
        cell = self._get_neighbour_cell(x_distance_from_center, y_distance_from_center)
        if cell:
            x_distance = x_distance_from_center + cell.x_center_offset
            y_distance = y_distance_from_center + cell.y_center_offset
            return x_distance ** 2 + y_distance ** 2 <= self.radius ** 2
        else:
            return False

    def _get_neighbour_cell(self, row_offset, col_offset):
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