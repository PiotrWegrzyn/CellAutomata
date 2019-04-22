from kivy.core.window import Window

from controler.GameOfLifeController import GameOfLifeController
from controler.MainController import BaseController
from model.CellAutomata.CellAutomaton1D import CellAutomaton1D
from model.RuleSets.BinaryRule import BinaryRuleSet


def generate_empty_2d_list_of_list(size):
    return [[] for i in range(0, size)]


class BinaryRuleSetController(BaseController):
    modes = {
        "Game of Life": GameOfLifeController,
    }
    rule_set = BinaryRuleSet
    def __init__(self, view, cell_size=9, cell_offset=1,rule=90):
        super().__init__(view)

        self.cell_size = cell_size
        self.cell_offset = cell_offset
        self.cell_box_size = cell_size + cell_offset

        self.max_graphic_columns = self.get_view_max_columns()
        self.max_graphic_rows = self.get_view_max_rows()
        self.iteration_speed = 8

        self.data_frame = generate_empty_2d_list_of_list(size=self.max_graphic_rows)

        self.automaton_columns_count = self.get_view_max_rows()
        self.automaton_iterations = self.get_view_max_rows()
        self.cell_automaton = None
        self.set_cell_automaton()

    def set_cell_automaton(self):
        if self.cell_automaton is None:
            self.cell_automaton = CellAutomaton1D(
                columns_count=self.get_view_max_columns(),
                rule_set=self.rule_set(90),
                percent_of_alive_cells=0.2
            )
        else:
            self.cell_automaton = CellAutomaton1D(
                columns_count=self.cell_automaton.get_columns_count(),
                rule_set=self.cell_automaton.get_rule_set(),
                percent_of_alive_cells=self.cell_automaton.get_percent_of_alive_cells()
            )

    def get_view_max_columns(self):
        return int((Window.size[0] - self.menu_item_width) / self.cell_box_size)

    def get_view_max_rows(self):
        return int(Window.size[1] / self.cell_box_size)