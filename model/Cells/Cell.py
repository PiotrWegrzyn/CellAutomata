import random
from kivy.graphics.context_instructions import Color
from model.State.State import State


class Cell:
    dead_state = State(0, Color(1, 1, 1))
    alive_states = [State(1, Color(1, 0, 0))]

    def __init__(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_value(self):
        return self.state.get_value()

    def get_color(self):
        return self.state.get_color_representation()

    def is_dead(self):
        if self.state is self.dead_state:
            return True
        return False

    def is_alive(self):
        if self.state is not self.dead_state:
            return True
        return False

    @staticmethod
    def get_dead_state():
        return Cell.dead_state

    @staticmethod
    def get_random_alive_state():
        return random.choice(Cell.alive_states)

    @staticmethod
    def get_state_from_values(value=None, **kwargs):
        if value is 0:
            return Cell.dead_state
        else:
            return Cell.get_random_alive_state()





