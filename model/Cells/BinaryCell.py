import random

from kivy.graphics.context_instructions import Color

from model.Cells.Cell import Cell


class BinaryCell(Cell):
    dead_state = 0
    alive_states = [1]

    def __init__(self, state):
        super().__init__(state)

    def flip_state(self):
        self.state = int(not self.state)

    def get_color_representation(self):
        if self.state is 0:
            return Color(1, 1, 1)
        if self.state is 1:
            return Color(1, 0, 0)

    @staticmethod
    def get_dead_state():
        return BinaryCell.dead_state

    @staticmethod
    def get_random_alive_state():
        return 1