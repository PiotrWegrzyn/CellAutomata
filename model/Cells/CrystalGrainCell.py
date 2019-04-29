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
    dead_state = 0

    def __init__(self, state):
        super().__init__(state)

    def get_color_representation(self):
        if self.state is 1:
            return [1, 1, 1]
        else:
            color_table = self.state_to_color()
            return color_table #[1, 0, 0]

    @staticmethod
    def get_dead_state():
        return CrystalGrainCell.dead_state

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
        CrystalGrainCell.alive_states.append(new_grain_id)
        return new_grain_id

    def state_to_color(self):
        float_s = self.state * 1.0
        return [float_s%8/8,float_s%13/13,float_s%21/21]

