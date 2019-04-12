import threading
from app import *
from CellAutomaton import CellularAutomaton
import sys

sys.setrecursionlimit(100000)
threading.stack_size(200000000)
thread = threading.Thread(target=CellAutomatonApp().run())
thread.start()

# cell_automaton = CellularAutomaton(mode=2, size=10, rule=90, number_of_ones=60)
# cell_automaton.print_iterations(10)
