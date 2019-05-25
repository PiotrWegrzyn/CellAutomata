from model.Neighbourhoods.NeighbourhoodBase import NeighbourhoodBase


class HexagonalLeft(NeighbourhoodBase):

    def _set_prev_neighbours(self):
        self._append_neighbour(-1, -1)
        self._append_neighbour(-1, 0)
        self._append_neighbour(0, -1)
        self._append_neighbour(0, 0)
        self._append_neighbour(0, 1)
        self._append_neighbour(1, 0)
        self._append_neighbour(1, 1)
