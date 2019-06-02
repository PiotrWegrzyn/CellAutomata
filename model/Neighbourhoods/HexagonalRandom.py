import random

from model.Neighbourhoods.NeighbourhoodBase import NeighbourhoodBase


class HexagonalRandom(NeighbourhoodBase):

    def _set_neighbours(self):
        random.choice([self.left, self.right])()

    def right(self):
        self._append_neighbour(-1, 0)
        self._append_neighbour(-1, 1)
        self._append_neighbour(0, -1)
        self._append_neighbour(0, 0)
        self._append_neighbour(0, 1)
        self._append_neighbour(1, -1)
        self._append_neighbour(1, 0)

    def left(self):
        self._append_neighbour(-1, -1)
        self._append_neighbour(-1, 0)
        self._append_neighbour(0, -1)
        self._append_neighbour(0, 0)
        self._append_neighbour(0, 1)
        self._append_neighbour(1, 0)
        self._append_neighbour(1, 1)
