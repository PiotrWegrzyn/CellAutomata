import math
import random

from model.Cells.CrystalGrainCell import CrystalGrainCell
from model.Neighbourhoods.Moore import Moore
from model.RuleSets.NucleationRuleSet import NucleationRuleSet


class RecrystallizationRuleSet(NucleationRuleSet):
    cell_type = CrystalGrainCell
    required_dimension = 2

    def __init__(self, current_state, initial_mode='random', is_periodic=True, neighbourhood_type=Moore, radius=4, iteration=0, color_indicator='grain_id'):
        super().__init__(
            initial_mode=initial_mode,
            is_periodic=is_periodic,
            neighbourhood_type=neighbourhood_type,
            radius=radius,
            color_indicator=color_indicator
        )

        self.amount_of_cells = len(current_state) * len(current_state[0])
        self.iteration = iteration
        self.time_step = 0.001
        self.const_a = 86710969050178.5
        self.const_b = 9.41268203527779
        self.a_over_b = self.const_a/self.const_b
        self.rho = self.calculate_rho()
        self.rho_critical = self.calculate_rho(65)/self.amount_of_cells
        # constants
        self.border_dislocation_density_change_rate = 2.5
        self.critical_dislocation_density_level = 5

        # calculated at the start of each iteration
        self.dislocation_density_pool = 0
        self._calculate_dislocation_density_pool()
        self.average_dislocation_package = self.calculate_average_dislocation_package()

    def apply_pre_iteration(self, previous_state, current_state):
        self._calculate_dislocation_density_pool()
        self.average_dislocation_package = self.calculate_average_dislocation_package()
        self.distribute_dislocation_density(current_state, 0.2, 1)

    def _calculate_dislocation_density_pool(self):
        new_rho = self.calculate_rho()
        self.dislocation_density_pool = new_rho - self.rho
        self.rho = new_rho

    def calculate_rho(self, iteration = None):
        # ro = A/b + (1- (A/B))e ^ (-Bt)
        if iteration is None:
            iteration = self.iteration
        return self.a_over_b + (1-self.a_over_b) * math.exp(-self.const_b*self.time_step*iteration)

    def calculate_average_dislocation_package(self):
        return self.dislocation_density_pool / self.amount_of_cells

    def distribute_dislocation_density(self, state, first_package_size, second_package_size):
        self.distribute_across_all_cells(state, first_package_size)
        self.distribute_remaining_pool(state, second_package_size)

    def distribute_across_all_cells(self, state, percent_of_dislocation_package):
        dislocation_package = percent_of_dislocation_package*self.average_dislocation_package
        for row in state:
            for cell in row:
                self.add_dislocation_density_to_cell(cell, dislocation_package)

    def add_dislocation_density_to_cell(self, cell, dislocation_package):
        if self.dislocation_density_pool - dislocation_package >= 0:
            self.dislocation_density_pool -= dislocation_package
            cell.add_dislocation_density(dislocation_package)
            if cell.state.dislocation_density > self.rho_critical:
                cell.recrystallize()

    def distribute_remaining_pool(self, state, percent_of_dislocation_package):
        border_cells = []
        inside_cells = []
        for row in state:
            for cell in row:
                if self.check_is_border(cell):
                    border_cells.append(cell)
                else:
                    inside_cells.append(cell)

        dislocation_package = percent_of_dislocation_package*self.average_dislocation_package

        while self.dislocation_density_pool - dislocation_package > 0:
            print("adding")
            if self.where_to_add() == "border_cell":
                try:
                    cell_to_add = random.choice(border_cells)
                except IndexError:
                    # handle no border cells
                    cell_to_add = random.choice(inside_cells)
            else:
                cell_to_add = random.choice(inside_cells)
            self.add_dislocation_density_to_cell(cell_to_add, dislocation_package)

    def where_to_add(self):
        return random.choice(["border_cell"]*4+["inside_cell"])

    def handle_no_border_cells(self):
        pass

    def apply(self, previous_state, current_state, cell_row, cell_column):
        cell_in_current_iteration = current_state[cell_row][cell_column]
        if not cell_in_current_iteration.state.is_recrystallized:
            current_neighbours_states = self.get_neighbour_states(current_state, cell_row, cell_column)
            for state in current_neighbours_states:
                if state.is_recrystallized:
                    if self.try_recrystallize(cell_in_current_iteration, current_neighbours_states):
                        cell_in_current_iteration.recrystallize()
                    break

    def check_for_critical_dislocation_density(self, judged_cell):
        return judged_cell.state.dislocation_density > self.critical_dislocation_density_level

    def grow_recrystallized_grain(self, current_state, row, column):
        current_state[row][column].state.grain_id = CrystalGrainCell.get_new_grain_id()
        current_state[row][column].recrystallize()

    def has_recystallized_neighbours(self, neighbours_states):
        for state in neighbours_states:
            if state.is_recrystallized:
                return True
        return False

    def check_is_border(self, cell):
        return cell.state.energy > 0

    def has_highest_dislocation_density(self, cell_in_prev, prev_neighbours_states):
        for state in prev_neighbours_states:
            if cell_in_prev.state.dislocation_density < state.dislocation_density and not state.is_recrystallized:
                return False
        return True

    def apply_post_iteration(self, previous_state, current_state):
        self.calculate_total_energy(current_state)
        self.iteration += 1

    def try_recrystallize(self, cell, neighbour_states):
        neighbour_states_dislocation_energies = [state.dislocation_density for state in neighbour_states]
        return cell.state.dislocation_density > max(neighbour_states_dislocation_energies)






