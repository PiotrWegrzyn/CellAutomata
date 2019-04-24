from model.CellAutomata.CellAutomaton1D import CellAutomaton1D
from model.CellAutomata.CellAutomaton2D import CellAutomaton2D
from model.RuleSets.RuleSet import RuleSet


class CellAutomatonFactory:
    modes = {
        "1D": 1,
        "2D": 2
    }

    def create(self, rule_set, columns, rows_count=None,percent_of_alive_cells=None, initial_state=None):
        if not isinstance(rule_set, RuleSet):
            raise TypeError

        if rule_set.required_dimension is self.modes["1D"]:
            return CellAutomaton1D(rule_set, columns, percent_of_alive_cells, initial_state)
        if rule_set.required_dimension is self.modes["2D"]:
            return CellAutomaton2D(rule_set, columns, rows_count, percent_of_alive_cells, initial_state)
        else:
            raise ValueError
