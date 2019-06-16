import random
from model.Cells.Cell import Cell
from settings import BACKGROUND_COLOR


def id_generator():
    id = 1
    while True:
        yield id
        id += 1


class CrystalGrainCell(Cell):
    id_generator = id_generator()
    dead_grain_id = 0
    dead_state = dead_grain_id
    max_dislocation = 1

    def __init__(self, state):
        super().__init__(state)
        self.x_center_offset = random.randrange(-5, 5) * 0.1
        self.y_center_offset = random.randrange(-5, 5) * 0.1

    def get_color_representation(self, color_indicator="grain_id"):
        if color_indicator == "grain_id":
            if self.is_dead():
                return BACKGROUND_COLOR
            return self.grain_id_to_color()
        elif color_indicator == 'energy':
            if self.is_dead() or self.state.energy is 0:
                return BACKGROUND_COLOR
            return [0.125 * self.state.energy, 0, 0]
        elif color_indicator == 'dislocation':
            if self.is_dead() or (self.state.dislocation_density == 0 and not self.is_recrystallized()):
                return BACKGROUND_COLOR
            elif self.is_recrystallized() and self.state.dislocation_density == 0:
                return [1, 0, 0]
            try:
                return [0, 0, self.state.dislocation_density/self.max_dislocation]
            except ZeroDivisionError:
                return [0, 0, self.state.dislocation_density]


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

    def set_new_grain_id(self):
        self.state.grain_id = self.get_new_grain_id()

    def recrystallize(self, iteration):
        self.state.recrystallize(iteration)

    def is_recrystallized(self):
        return self.state.is_recrystallized

    def grain_id_to_color(self):
        id = self.state.grain_id
        if not self.is_recrystallized():
            return [0, (id % 8 + id) % 13/13, (id + id % 13) % 21/21]
        else:
            return [(id % 8 + id % 13) % 21/21, 0, 0]

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
        def __init__(self, grain_id, energy=0, is_recrystallized=False, dislocation_density=0, recrystallize_iteration=None):
            self.grain_id = grain_id
            self.energy = energy
            self.is_recrystallized = is_recrystallized
            self.dislocation_density = dislocation_density
            self.recrystallize_iteration = recrystallize_iteration

        def recrystallize(self, iteration):
            self.is_recrystallized = True
            self.dislocation_density = 0
            self.recrystallize_iteration = iteration

        def add_dislocation_packet(self, dislocation):
            self.dislocation_density += dislocation

        def recrystallized_in_prev(self, current_iteration):
            return self.recrystallize_iteration == current_iteration - 1


