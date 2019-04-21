import random

from model.BinaryCell import BinaryCell
from model.CellAutomaton import CellAutomaton
from model.CellFactory import CellFactory
from model.State import State


class CellAutomaton1D(CellAutomaton):
    def __init__(self, rule, columns_count, initial_state=None):
        super().__init__(rule, columns_count, initial_state)

    def _prepare_initial_dead_cells(self):
        cell_type = self.rule.get_cell_type()
        cell_factory = CellFactory()
        self.initial_state = [cell_factory.create_dead_cell(cell_type)] * self.columns_count

    def _prepare_initial_alive_cells(self):
        self._set_number_of_alive_cells()
        cell_type = self.rule.get_cell_type()
        cell_factory = CellFactory()
        for i in range(0, self.number_of_alive_cells):
            while True:
                y = random.randrange(0, self.columns_count)
                if self.initial_state[y] is not 1:
                    self.initial_state[y] = cell_factory.create_random_alive_cell(cell_type)
                    break

    def _set_number_of_alive_cells(self):
        self.number_of_alive_cells = int(self.columns_count * self.percentage_of_alive_cells)

    def set_percent_of_alive_cells(self, percent):
        self.percentage_of_alive_cells = percent
        self._set_number_of_alive_cells()

    def change_size(self, columns_count):
        self._set_size(columns_count)
        self._fit_to_size()
        self.set_to_initial_state()

    def get_rule(self):
        return self.rule

    def change_alive_cells_percentage(self, percentage_of_alive_cells):
        self.set_percent_of_alive_cells(round(percentage_of_alive_cells, 2))
        self._set_number_of_alive_cells()
        self._prepare_initial_state()
        self.set_to_initial_state()
