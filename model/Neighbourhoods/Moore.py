from model.Neighbourhoods.NeighbourhoodInterface import NeighborhoodInterface


class Moore(NeighborhoodInterface):

    def _get_neighbour_state(self, row_offset, col_offset):
        if self.is_periodic:
            return self.state[(self.row+row_offset) % self.row_count][(self.column+col_offset) % self.column_count].get_state()
        else:
            try:
                if self.row+row_offset < 0 or self.column + col_offset < 0:
                    raise IndexError
                return self.state[self.row+row_offset][self.column+col_offset].get_state()
            except IndexError:
                return None   # todo make it not return None

    def _append_neighbour(self, row_offset, column_offset):
        state = self._get_neighbour_state(row_offset, column_offset)
        if state:
            self.prev_neighbour_states.append(state)

    def _set_prev_neighbour_states(self):
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x is 0 and y is 0:
                    continue
                self._append_neighbour(x, y)

    def get_prev_neighbours_states(self):
        return self.prev_neighbour_states

