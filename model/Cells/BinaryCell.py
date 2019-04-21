from model.Cells.Cell import Cell


class BinaryCell(Cell):
    def __init__(self, state):
        super().__init__(state)
        # if isinstance(state, State):
        #     raise ValueError

    def flip_state(self):
        if self.state is self.dead_state:
            self.state = self.alive_states[0]
        else:
            self.state = self.dead_state


