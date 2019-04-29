import random
from kivy.graphics.context_instructions import Color


class Cell:
    dead_state = None
    alive_states = []

    def __init__(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_color(self):
        return self.get_color_representation()

    def is_dead(self):
        if self.state == self.dead_state:
            return True
        return False

    def is_alive(self):
        if not self.is_dead():
            return True
        return False

    @staticmethod
    def get_dead_state():
        pass

    @staticmethod
    def get_random_alive_state():
        pass

    def get_color_representation(self):
        pass


