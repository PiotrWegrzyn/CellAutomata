from model.CellAutomaton1D import CellAutomaton1D


class CellAutomaton2D(CellAutomaton1D):
    def __init__(self, rule, columns_count, rows_count, percent_of_alive_cells=None, initial_state=None):
        super().__init__(rule, columns_count, percent_of_alive_cells, initial_state)
        self._set_columns_count(columns_count)
        self._set_rows_count(rows_count)

    def _set_rows_count(self, rows_count):
        if rows_count < 0:
            raise ValueError
        self.columns_count = rows_count

    def _set_columns_count(self, columns_count):
        if columns_count < 0:
            raise ValueError
        self.columns_count = columns_count






