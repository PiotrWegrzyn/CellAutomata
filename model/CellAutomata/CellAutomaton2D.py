from model.CellAutomata.CellAutomaton1D import CellAutomaton1D


class CellAutomaton2D(CellAutomaton1D):
    def __init__(self, rule_set, columns_count, rows_count, percent_of_alive_cells=None, initial_state=None):
        super().__init__(rule_set, columns_count, percent_of_alive_cells, initial_state)
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


    def _set_cells(self):
        for cell_index in range(0, self.columns_count):
            self._append_cell(cell_index)

  def _prepare_initial_alive_cells(self):
        self._set_number_of_alive_cells()
        cell_type = self.rule_set.get_cell_type()
        cell_factory = CellFactory()
        for i in range(0, self._number_of_alive_cells):
            while True:
                y = random.randrange(0, self.columns_count)
                if self.initial_state[y].is_dead():
                    self.initial_state[y] = cell_factory.create_random_alive_cell(cell_type)
                    break

    def _prepare_initial_dead_cells(self):
        cell_type = self.rule_set.get_cell_type()
        cell_factory = CellFactory()
        self.initial_state = [cell_factory.create_dead_cell(cell_type)] * self.columns_count


  def print_current_state(self):
            print([cell.get_value() for cell in self.current_state])



