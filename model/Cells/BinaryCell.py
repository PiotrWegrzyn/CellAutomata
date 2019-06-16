from model.Cells.Cell import Cell
from settings import BACKGROUND_COLOR


class BinaryCell(Cell):
    dead_state = 0
    alive_states = [1]

    def __init__(self, state):
        super().__init__(state)

    def flip_state(self):
        self.state = int(not self.state)

    def get_color_representation(self):
        if self.state is 0:
            return BACKGROUND_COLOR
        else:
            return [1, 0, 0]

    def get_reversed_color(self):
        if self.state is 0:
            return [1, 0, 0]
        else:
            return BACKGROUND_COLOR

    @staticmethod
    def get_dead_state():
        return BinaryCell.dead_state

    @staticmethod
    def get_random_alive_state():
        return 1

    def die(self):
        self.state = 0

    def resurrect(self):
        self.state = 1


