from model.CellAutomaton1D import CellAutomaton1D
from model.CellAutomaton2D import CellAutomaton2D
from model.Rule import Rule


class CellAutomatonFactory:
    modes = {
        "1D": 1,
        "2D": 2
    }

    def create(self, rule, columns_count, rows_count=None, initial_state=None):
        if not isinstance(rule, Rule):
            raise TypeError

        if rule.required_dimension is self.modes["1D"]:
            return CellAutomaton1D(rule, columns_count, initial_state)
        if rule.required_dimension is self.modes["2D"]:
            return CellAutomaton2D(rule, columns_count, rows_count, initial_state)
        else:
            raise ValueError
