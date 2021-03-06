import concurrent
import multiprocessing
import random
import threading
from concurrent.futures.process import ProcessPoolExecutor

from model.Cells.CrystalGrainCell import CrystalGrainCell
from model.Neighbourhoods.Moore import Moore
from model.Neighbourhoods.Radius import Radius
from model.Neighbourhoods.VonNeumann import VonNeumann
from model.Neighbourhoods.Pentagonal import Pentagonal
from model.Neighbourhoods.HexagoanlRight import HexagonalRight
from model.Neighbourhoods.HexagonalLeft import HexagonalLeft
from model.Neighbourhoods.HexagonalRandom import HexagonalRandom
from model.RuleSets.RuleSet import RuleSet
from time_measure.timeit_decorator import timeit


class NucleationRuleSet(RuleSet):
    cell_type = CrystalGrainCell
    required_dimension = 2
    initial_alive_cells = 0.01
    initial_iteration_speed = 2

    def __init__(self, initial_mode="random",is_periodic=True, neighbourhood_type=Moore, radius=4, color_indicator='grain_id'):
        super(NucleationRuleSet, self).__init__(radius)
        self.color_indicator = color_indicator
        self.is_periodic = is_periodic
        self.initial_mode = initial_mode
        self.neighbourhood_type = neighbourhood_type
        self.total_energy = 0

    def apply(self, previous_state, current_state, cell_row, cell_column):
        judged_cell = previous_state[cell_row][cell_column]
        if judged_cell.is_dead():
            previous_neighbours_states = self.get_neighbour_states(previous_state, cell_row, cell_column)
            previous_neighbours_grain_ids = [state.grain_id for state in previous_neighbours_states]
            previous_grains_type_count = self.get_grain_type_count(previous_neighbours_grain_ids)
            try:
                most_common_grain_id = self.get_most_common_grain_id(previous_grains_type_count)
                current_state[cell_row][cell_column].state.grain_id = most_common_grain_id
            except ValueError:
                self.no_grains_surrounding()

    @timeit
    def apply_post_iteration(self, previous_state, current_state):
        self.update_energy_in_cells(current_state)
        self.calculate_total_energy(current_state)

    def update_energy_in_cells(self, state):
        for row_id in range(0, len(state)):
            self.update_energy_in_row(row_id, state)

    def update_energy_in_row(self, row_id, state):
        columns_count = len(state[0])
        for col_id in range(columns_count):
            state[row_id][col_id].state.energy = self.calculate_energy(state, row_id, col_id)

    def calculate_energy(self, state, row, column):
        energy = 0
        neighbour_states = self.get_neighbour_states(state, row, column)
        self_grain_id = state[row][column].state.grain_id
        for state in neighbour_states:
            if state.grain_id is not self_grain_id:
                energy += 1
        return energy

    def calculate_total_energy(self, state):
        self.total_energy = 0
        for row_id in range(len(state)):
            self.total_energy += sum([cell.state.energy for cell in state[row_id]])

    def get_neighbour_states(self, state, cell_row, cell_column):
        neighbourhood = self.get_neighbourhood(state, cell_row, cell_column)
        prev_neighbours_states = neighbourhood.get_neighbours_states()
        return prev_neighbours_states

    @staticmethod
    def get_required_dimension():
        return NucleationRuleSet.required_dimension

    @staticmethod
    def get_cell_type():
        return NucleationRuleSet.cell_type

    def get_grain_type_count(self, previous_neighbours_values):
        distinct_neighbours_ids = self.get_distinct_grain_ids(previous_neighbours_values)
        return {v: previous_neighbours_values.count(v) for v in distinct_neighbours_ids}

    def get_distinct_grain_ids(self, previous_neighbours_values):
        distinct_neighbours_ids = set(previous_neighbours_values)
        try:
            distinct_neighbours_ids.remove(0)     # 0 is the indicator that cell is dead
        except KeyError:
            pass
        return distinct_neighbours_ids

    def get_most_common_grain_id(self, previous_grains_type_count):
        return max(previous_grains_type_count, key=lambda key: previous_grains_type_count[key])

    def get_initial_state(self, number_of_alive_cells, columns, rows=None):
        initial_state = self._prepare_initial_dead_cells(rows, columns)
        self._prepare_initial_alive_cells(initial_state, number_of_alive_cells)
        return initial_state

    def _prepare_initial_alive_cells(self, initial_state, number_of_alive_cells):
        if self.initial_mode is "random":
            self._prepare_random_alive_cells(initial_state, number_of_alive_cells)
        elif self.initial_mode is "equal_spread":
            self._prepare_equaly_spread_alive_cells(initial_state)
        elif self.initial_mode is "radius":
            self._prepare_radius_spread_alive_cells(initial_state,number_of_alive_cells)

    def _prepare_initial_dead_cells(self, rows, columns):
        clear_state = []
        for r in range(0, rows):
            row = []
            for c in range(0, columns):
                row.append(self.cell_factory.create_dead_cell())
            clear_state.append(row)
        return clear_state

    def no_grains_surrounding(self):
        pass

    def _prepare_random_alive_cells(self, initial_state, number_of_alive_cells):
        rows = len(initial_state)
        columns = len(initial_state[0])
        if number_of_alive_cells > rows*columns:
            number_of_alive_cells = rows*columns
        for i in range(0, number_of_alive_cells):
            while True:
                x = random.randrange(0, rows)
                y = random.randrange(0, columns)
                if initial_state[x][y].is_dead():
                    initial_state[x][y].state = CrystalGrainCell.State(grain_id=CrystalGrainCell.get_new_grain_id())
                    break

    def _prepare_equaly_spread_alive_cells(self, initial_state, row_offset=3, col_offset=3):
        rows = len(initial_state)
        columns = len(initial_state[0])

        for row in range(0, rows, row_offset):
            for column in range(0, columns, col_offset):
                initial_state[row][column].state = CrystalGrainCell.State(grain_id=CrystalGrainCell.get_new_grain_id())

    def _prepare_radius_spread_alive_cells(self, initial_state, number_of_alive_cells):
        rows = len(initial_state)
        columns = len(initial_state[0])
        retries = int(rows*columns*0.01)
        if number_of_alive_cells > rows*columns:
            number_of_alive_cells = rows*columns
        failed_count = 0
        for cell in range(number_of_alive_cells):
            if failed_count < 10:
                for i in range(retries):
                    x = random.randrange(0, rows)
                    y = random.randrange(0, columns)
                    if initial_state[x][y].is_dead() and self._no_alive_cells_in_radius(initial_state, x, y):
                        initial_state[x][y].state = CrystalGrainCell.State(grain_id=CrystalGrainCell.get_new_grain_id())
                        failed_count = 0
                        break
            failed_count += 1

    def _no_alive_cells_in_radius(self, state, row, column):
        neighbours = Radius(state, row, column, self.is_periodic, self.radius).get_neighbours()
        for cell in neighbours:
            if cell.is_alive():
                return False
        return True

    def get_neighbourhood_type(self):
        return self.neighbourhood_type

    def get_neighbourhood(self, previous_state, cell_row, cell_column):
        NeighbourhoodClass = self.get_neighbourhood_type()
        if issubclass(NeighbourhoodClass, Radius):
            return NeighbourhoodClass(previous_state, cell_row, cell_column, self.is_periodic, radius=self.radius)
        else:
            return NeighbourhoodClass(previous_state, cell_row, cell_column, self.is_periodic)

    def get_total_energy(self):
        return self.total_energy

