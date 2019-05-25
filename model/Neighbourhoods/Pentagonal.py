import random

from model.Neighbourhoods.NeighbourhoodInterface import NeighborhoodInterface


class Pentagonal(NeighborhoodInterface):

    def _set_prev_neighbour_states(self):
        random_choice = random.randrange(0, 4)
        if random_choice is 0:
            self._append_in_area(row_start=0)
        if random_choice is 1:
            self._append_in_area(row_end=0)
        if random_choice is 2:
            self._append_in_area(column_start=0)
        if random_choice is 3:
            self._append_in_area(column_end=0)

