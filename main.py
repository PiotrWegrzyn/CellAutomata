from model.CellAutomata.CellAutomatonFactory import CellAutomatonFactory

if __name__ == '__main__':
    # CellAutomatonApp().run()
    from model.RuleSets.BinaryRule import *
    from model.CellAutomata.CellAutomaton1D import *

    br = BinaryRuleSet(90)
    factory = CellAutomatonFactory()
    ca = factory.create(br, 10, 0.2)
    ca.print_iterations(10)
    ca.change_size(5)
    ca.print_iterations(10)
    ca.change_alive_cells_percentage(0.5)
    ca.print_iterations(10)

