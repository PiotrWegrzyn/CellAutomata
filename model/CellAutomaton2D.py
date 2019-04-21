from model.CellAutomaton import CellAutomaton


class CellAutomaton2D(CellAutomaton):
    def __init__(self, rule, columns_count, rows_count, initial_state=None):
        super().__init__(rule, initial_state)
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






