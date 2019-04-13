from app import *
from CellAutomaton import CellularAutomaton
from multiprocessing import Pool as ThreadPool



if __name__ == '__main__':
    CellAutomatonApp().run()
    cell_automaton = CellularAutomaton(mode=2, size=10, rule=90, percentage_of_ones=0.3)


