import random
import math

from model.Cells.CrystalGrainCell import CrystalGrainCell
from model.Neighbourhoods.Moore import Moore
from model.RuleSets.NucleationRuleSet import NucleationRuleSet
from time_measure.timeit_decorator import timeit


class MonteCarloRuleSet(NucleationRuleSet):
    cell_type = CrystalGrainCell
    required_dimension = 2

    def __init__(self, kt_constant=1.0, initial_mode='random', is_periodic=True, neighbourhood_type = Moore, radius=4, color_indicator='grain_id'):
        super().__init__(
            initial_mode=initial_mode,
            is_periodic=is_periodic,
            neighbourhood_type=neighbourhood_type,
            radius=radius,
            color_indicator=color_indicator
        )
        if 0.1 <= kt_constant <= 6:
            self.probability_calculator = ProbabilityCalculator(kt_constant)
        else:
            raise ValueError

    def apply(self, previous_state, current_state, cell_row, cell_column):
        pass

    @timeit
    def apply_pre_iteration(self, previous_state, current_state):

        coords = self.get_shuffled_list_of_all_cell_cords(previous_state)

        for coord in coords:
            row = coord[0]
            col = coord[1]
            pre_energy = self.calculate_energy(current_state, row, col)

            self.set_cell_to_random_neighbour_id(previous_state, current_state, row, col)

            post_energy = self.calculate_energy(current_state, row, col)

            energy_delta = post_energy - pre_energy

            if self.probability_calculator.should_accept(energy_delta):
                current_state[row][col].state.energy = post_energy
            else:
                self.revert_cell(previous_state, current_state, row, col)

    def apply_post_iteration(self, previous_state, current_state):
        self.calculate_total_energy(current_state)

    @timeit
    def get_shuffled_list_of_all_cell_cords(self, state):
        coords = [(x, y) for x in range(len(state)) for y in range(len(state[0]))]
        random.shuffle(coords)
        return coords

    def set_cell_to_random_neighbour_id(self, previous_state, current_state, row, col):
        neighbour_states = self.get_neighbour_states(previous_state, row, col)
        chosen_id = random.choice(neighbour_states).grain_id
        current_state[row][col].state.grain_id = chosen_id

    def revert_cell(self, previous_state, current_state, row, col):
        current_state[row][col].state.grain_id = previous_state[row][col].state.grain_id

    def change_kt_constant(self, new_value):
        self.probability_calculator.kt_constant = new_value

    def get_kt_constant(self):
        return self.probability_calculator.kt_constant


class ProbabilityCalculator:
    def __init__(self, kt_constant):
        self.kt_constant = kt_constant

    @timeit
    def should_accept(self, energy_delta):
        probability = self.get_probability(energy_delta)
        if probability is 1:
            return True
        probability_percent = probability * 100
        if self.attempt(percent=probability_percent, accuracy=2):
            return True
        return False

    def get_probability(self, energy_delta):
        if energy_delta <= 0:
            return 1
        else:
            return math.exp(-energy_delta / self.kt_constant)

    @staticmethod
    def attempt(percent, accuracy):
        return random.randrange(0, 10 ** (2 + accuracy)) <= percent * 10 ** accuracy
