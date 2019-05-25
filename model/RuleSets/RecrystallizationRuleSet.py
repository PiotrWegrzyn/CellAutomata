import random

from model.Cells.CrystalGrainCell import CrystalGrainCell
from model.Neighbourhoods.Moore import Moore
from model.RuleSets.NucleationRuleSet import NucleationRuleSet


class RecrystallizationRuleSet(NucleationRuleSet):
    cell_type = CrystalGrainCell
    required_dimension = 2

    def __init__(self, current_state, initial_mode='random', is_periodic=True, neighbourhood_type = Moore, radius=4, iteration=0):
        super().__init__(
            initial_mode=initial_mode,
            is_periodic=is_periodic,
            neighbourhood_type=neighbourhood_type,
            radius=radius
        )
        self.iteration = iteration

        # constants
        self.border_energy_change_rate = 2.5
        self.critical_energy_level = 5

        # calculated at the start of each iteration
        self.amount_of_cells = len(current_state) * len(current_state[0])
        self.energy_pool = 0
        self.calculate_energy_pool()
        self.average_energy = self.energy_pool / self.amount_of_cells

    def apply_pre_iteration(self, previous_state, current_state):
        self.calculate_energy_pool()
        self.distribute_energy()

    def calculate_energy_pool(self):
        # ro = A/b + (1- (A/B))e ^ (-Bt)
        # todo make it use the equation above
        self.energy_pool = 3*self.amount_of_cells

    def apply(self, previous_state, current_state, cell_row, cell_column):
        cell_in_prev_iteration = previous_state[cell_row][cell_column]
        cell_in_current_iteration = current_state[cell_row][cell_column]

        prev_neighbours_states = self.get_previous_neighbours_values(previous_state, cell_row, cell_column)
        if cell_in_prev_iteration.is_recrystallized() is not True:
            is_border = self.check_is_border(cell_in_prev_iteration,prev_neighbours_states)
            self.add_energy_to_cell(cell_in_current_iteration, cell_in_prev_iteration, is_border)

        if self.has_recystallized_neighbours(prev_neighbours_states):
            if self.has_highest_energy(cell_in_prev_iteration, prev_neighbours_states):
                cell_in_current_iteration.state.energy = 0
                cell_in_current_iteration.recrystallize()

        if self.check_for_critical_energy(cell_in_current_iteration):
            cell_in_current_iteration.state.energy = 0
            self.grow_recrystallized_grain(current_state, cell_row, cell_column)

    def add_energy_to_cell(self, current_cell, prev_cell, is_border):
        prev_energy = prev_cell.state.energy
        energy_gain = self.average_energy
        if is_border:
            energy_gain *= self.border_energy_change_rate
        energy_gain *= random.randrange(0, 10) / 10
        if self.energy_pool - energy_gain > 0:
            current_cell.state.energy = prev_energy + energy_gain
            self.energy_pool -= energy_gain

    def check_for_critical_energy(self, judged_cell):
        return judged_cell.state.energy > self.critical_energy_level

    def grow_recrystallized_grain(self, current_state, row, column):
        current_state[row][column].state.grain_id = CrystalGrainCell.get_new_grain_id()
        current_state[row][column].recrystallize()

    def has_recystallized_neighbours(self, neighbours_states):
        for state in neighbours_states:
            if state.is_recrystallized:
                return True
        return False

    def check_is_border(self, cell_in_prev_iteration, prev_neighbours_states):
        for state in prev_neighbours_states:
            if state.grain_id is not cell_in_prev_iteration.state.grain_id:
                return True
        return False

    def has_highest_energy(self,cell_in_prev, prev_neighbours_states):
        for state in prev_neighbours_states:
            if cell_in_prev.state.energy < state.energy and not state.is_recrystallized:
                return False
        return True

    def distribute_energy(self):
        pass




