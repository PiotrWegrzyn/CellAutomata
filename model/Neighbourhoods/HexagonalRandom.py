import random

from model.Neighbourhoods.NeighbourhoodInterface import NeighborhoodInterface


class HexagonalRandom(NeighborhoodInterface):

    def _set_prev_neighbour_states(self):
        random.choice([self.left, self.right])()

    def right(self):
        self._append_neighbour_state(-1, 0)
        self._append_neighbour_state(-1, 1)
        self._append_neighbour_state(0, -1)
        self._append_neighbour_state(0, 0)
        self._append_neighbour_state(0, 1)
        self._append_neighbour_state(1, -1)
        self._append_neighbour_state(1, 0)

    def left(self):
        self._append_neighbour_state(-1, -1)
        self._append_neighbour_state(-1, 0)
        self._append_neighbour_state(0, -1)
        self._append_neighbour_state(0, 0)
        self._append_neighbour_state(0, 1)
        self._append_neighbour_state(1, 0)
        self._append_neighbour_state(1, 1)
