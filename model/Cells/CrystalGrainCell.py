import random

from model.Cells.Cell import Cell


def id_generator(start=1):
    id = start
    while True:
        yield id
        id += 1


class CrystalGrainCell(Cell):
    last_generated_id = 1
    id_generator = id_generator()
    dead_grain_id = 0
    dead_state = dead_grain_id

    def __init__(self, state):
        super().__init__(state)

    def get_color_representation(self):
        if self.state.grain_id is 0:
            return [1, 1, 1]
        elif self.is_recrystallized():
            return [0, 0, 0]
        else:
            return self.state_to_color()

    @staticmethod
    def get_dead_state():
        return CrystalGrainCell.State(grain_id=0)

    @staticmethod
    def get_random_alive_state():
        try:
            return random.choice(CrystalGrainCell.alive_states)
        except IndexError:
            # when there are no alive cells.
            return CrystalGrainCell.dead_state

    @staticmethod
    def get_new_grain_id():
        new_grain_id = CrystalGrainCell.id_generator.__next__()
        CrystalGrainCell.last_generated_id += new_grain_id
        CrystalGrainCell.alive_states.append(CrystalGrainCell.State(grain_id=new_grain_id))
        return new_grain_id

    def recrystallize(self):
        self.state.recrystallize()

    def is_recrystallized(self):
        return self.state.is_recrystallized

    def state_to_color(self):
        float_s = self.state.grain_id * 1.0
        return [float_s % 8/8, float_s % 13/13, float_s % 21/21]

    def is_dead(self):
        if self.state.grain_id == self.dead_state:
            return True
        return False

    def flip_state(self):
        if self.is_dead():
            self.state = CrystalGrainCell.State(self.get_new_grain_id())
        else:
            self.state = self.get_dead_state()

    class State:
        def __init__(self, grain_id, energy=0, is_recrystallized=False, ):
            self.grain_id = grain_id
            self.energy = energy
            self.is_recrystallized = is_recrystallized

        def recrystallize(self):
            self.is_recrystallized = True

