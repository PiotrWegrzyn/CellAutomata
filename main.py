from model.CellAutomata.CellAutomaton1D import CellAutomaton1D
from model.RuleSets.BinaryRuleSet import BinaryRuleSet
from view.App import CellAutomatonApp

if __name__ == '__main__':
    CellAutomatonApp().run()
    # ca = CellAutomaton1D(BinaryRuleSet(90), 10, 0.2)
    # ca.print_iterations(10);
