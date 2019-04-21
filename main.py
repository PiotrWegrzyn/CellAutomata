from view.view import *

if __name__ == '__main__':
    # CellAutomatonApp().run()
    from model.BinaryRule import *
    from model.CellAutomaton1D import *

    br = BinaryRule(90)
    ca = CellAutomaton1D(br, 10, 0.2)
    ca.print_iterations(10)
    ca.change_size(5)
    ca.print_iterations(10)
    ca.change_alive_cells_percentage(0.5)
    ca.print_iterations(10)

