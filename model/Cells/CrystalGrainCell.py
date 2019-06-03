import random

from model.Cells.Cell import Cell


def id_generator():
    id = 1
    while True:
        yield id
        id += 1


class CrystalGrainCell(Cell):
    id_generator = id_generator()
    dead_grain_id = 0
    dead_state = dead_grain_id

    def __init__(self, state):
        super().__init__(state)
        self.x_center_offset = random.randrange(-5, 5) * 0.1
        self.y_center_offset = random.randrange(-5, 5) * 0.1

    def get_color_representation(self, color_indicator="grain_id"):
        if color_indicator == "grain_id":
            if self.is_dead():
                return [0.2, 0.2, 0.2]
            elif self.is_recrystallized():
                return [0, 0, 0]
            else:
                return self.grain_id_to_color()
        elif color_indicator == 'energy':
            if self.is_dead() or self.state.energy is 0:
                return [0.2, 0.2, 0.2]
            return [0.125 * self.state.energy, 0, 0]

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
        CrystalGrainCell.alive_states.append(CrystalGrainCell.State(grain_id=new_grain_id))
        return new_grain_id

    def recrystallize(self):
        self.state.recrystallize()

    def is_recrystallized(self):
        return self.state.is_recrystallized

    def grain_id_to_color(self):
        float_s = self.state.grain_id * 1.0
        return [float_s % 8/8, (float_s % 8 + float_s) % 13/13, (float_s + float_s % 13) % 21/21]

    def is_dead(self):
        if self.state.grain_id == self.dead_state:
            return True
        return False

    def flip_state(self):
        if self.is_dead():
            self.state = CrystalGrainCell.State(self.get_new_grain_id())
        else:
            self.state = self.get_dead_state()

    def add_dislocation_density(self, dislocation_package):
        self.state.add_dislocation_packet(dislocation_package)

    class State:
        def __init__(self, grain_id, energy=0, is_recrystallized=False, dislocation_density=0):
            self.grain_id = grain_id
            self.energy = energy
            self.is_recrystallized = is_recrystallized
            self.dislocation_density = dislocation_density

        def recrystallize(self):
            self.is_recrystallized = True
            self.dislocation_density = 0

        def add_dislocation_packet(self, dislocation):
            self.dislocation_density += dislocation
