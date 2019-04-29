import random
from multiprocessing.pool import ThreadPool
from contextlib import closing
from model.CellAutomata.CellAutomaton1D import CellAutomaton1D


def generate_empty_2d_list_of_list(size):
    return [[] for i in range(0, size)]


class CellAutomaton2D(CellAutomaton1D):
    def __init__(self, rule_set, columns, rows, percent_of_alive_cells=None, initial_state=None):
        self._set_rows(rows)
        super().__init__(rule_set, columns, percent_of_alive_cells, initial_state)

    def create_random_initial_state(self):
        self._set_number_of_alive_cells()
        return self.rule_set.get_initial_random_state(
            number_of_alive_cells=self._number_of_alive_cells,
            columns=self.columns,
            rows=self.rows
        )

    def _set_rows(self, rows):
        if rows < 0:
            raise ValueError
        self.rows = rows

    # def _append_cell(self, cell_row, cell_index):
    #     self.current_state[cell_row].append(self.rule_set.apply(self.previous_state, ))

    def _apply_rule_to_cell(self, cell_row, cell_index):
        self.rule_set.apply(self.previous_state, cell_row, cell_index)

    def change_rows(self, rows):
        self._set_rows(rows)
        self._fit_initial_state_to_size()
        self.set_to_initial_state()

    def cell_count(self):
        return self.columns * self.rows

    def print_current_state(self):
        for row in self.current_state:
            print([cell.get_state() for cell in row])

    def print_stats(self):
        super().print_stats()
        print("Rows: ", self.rows.__str__())

    def __str__(self):
        return "Rule Set: " + self.rule_set.__str__() \
               + "Columns: " + self.columns.__str__()\
               + "Rows: " + self.rows.__str__()

    def create_empty_state(self):
        return generate_empty_2d_list_of_list(self.rows)

    def _set_cells(self):
        processes = int(self.rows / 3)
        if processes <= 0:
            processes = 1
        with closing(ThreadPool(processes)) as pool:
            pool.map(self.set_cells_in_row, [cell_row for cell_row in range(0, self.rows)])
        self.update_alive_cells()

    def set_cells_in_row(self, cell_row):
        for cell_index in range(0, self.columns):
            self._apply_rule_to_cell(cell_row, cell_index)
            # self._append_cell(cell_row, cell_index)

    def update_alive_cells(self):
        alive_sum = 0
        for row in self.current_state:
            alive_sum += sum([int(cell.is_alive()) for cell in row])
        self.set_percent_of_alive_cells(round(alive_sum/self.cell_count(), 2))

    def get_rows(self):
        return self.rows

    def update_cell(self, cell_row, cell_index, new_cell):
        self.current_state[cell_row][cell_index] = new_cell

