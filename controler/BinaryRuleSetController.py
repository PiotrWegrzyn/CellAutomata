from functools import partial

from kivy.core.window import Window

from controler.AutomatonController import AutomatonController
from controler.BaseController import generate_empty_2d_list_of_list, create_color
from model.CellAutomata.CellAutomaton1D import CellAutomaton1D
from model.Cells.CellFactory import CellFactory
from model.RuleSets.BinaryRuleSet import BinaryRuleSet
from view.BinaryRuleSetView import BinaryRuleSetView


class BinaryRuleSetController(AutomatonController):

    rule_set = BinaryRuleSet

    def __init__(self, app, cell_size=9, cell_offset=1):
        self.cell_size = cell_size
        self.cell_offset = cell_offset
        self.cell_box_size = cell_size + cell_offset
        super().__init__(app)
        self.update_labels()
        self.app.view.grid.on_touch_down = self.on_touch_down
        self.draw_current_state()

    def set_initial_view(self):
        self.set_view(BinaryRuleSetView(self.modes, self.get_menu_width()))

    def bind_buttons(self):
        super().bind_buttons()
        self.bind_iterations_buttons()
        self.bind_rule_buttons()

    def setup(self):
        self.iterations = self.get_view_max_rows()
        super().setup()

    def set_cell_automaton_to_starting_state(self):
        self.set_cell_automaton(
            columns=self.get_view_max_columns(),
            rule_set=self.rule_set(90),
            p_of_alive=0.2
        )

    def set_cell_automaton(self, columns=None, rule_set=None, p_of_alive=None, initial_state=None):
        if columns is None:
            columns = self.cell_automaton.get_columns()
        if rule_set is None:
            rule_set = self.cell_automaton.get_rule_set()
        if p_of_alive is None:
            p_of_alive = self.cell_automaton.get_percent_of_alive_cells()

        self.cell_automaton = CellAutomaton1D(
            columns=columns,
            rule_set=rule_set,
            percent_of_alive_cells=p_of_alive,
            initial_state = initial_state
        )

    def get_iterations(self):
        return self.iterations

    def bind_iterations_buttons(self):
        self.app.view.sub_iterations.bind(on_press=partial(self.sub_iterations_controller))
        self.app.view.add_iterations.bind(on_press=partial(self.add_iterations_controller))

    def bind_rule_buttons(self):
        self.app.view.add_rule.bind(on_press=partial(self.add_rule_controller))
        self.app.view.sub_rule.bind(on_press=partial(self.sub_rule_controller))

    def draw_button_controller(self, button_instance):
        self.draw_current_state()

    def sub_iterations_controller(self, button_instance):
        delta = -10
        current_value = self.iterations
        if current_value + delta > 0:
            self.iterations = current_value + delta
            self.set_empty_data_frame()
            self.update_iterations_label()

    def add_iterations_controller(self, button_instance):
        delta = 10
        current_value = self.iterations
        if current_value + delta > 0:
            self.iterations = current_value + delta
            self.set_empty_data_frame()
            self.update_iterations_label()

    def sub_rule_controller(self, button_instance):
        self.change_rule(delta=-5)
        self.draw_current_state()

    def add_rule_controller(self, button_instance):
        self.change_rule(delta=5)
        self.draw_current_state()

    def change_rule(self, delta):
        current_value = self.cell_automaton.get_rule_set().get_rule_base_10()
        self.set_cell_automaton(
            rule_set=BinaryRuleSet((current_value + delta) % 255),
            initial_state=self.cell_automaton.initial_state
        )
        self.update_rule_label()

    def fetch_current_data_frame(self):
        for iteration in range(0, self.iterations):
            new_state = self.cell_automaton.get_current_state()
            self.data_frame[iteration] = [cell.get_color_representation() for cell in new_state]
            self.cell_automaton.calculate_next_iteration()
        self.cell_automaton.set_to_initial_state()

    def update_labels(self):
        super().update_labels()
        self.update_iterations_label()
        self.update_rule_label()

    def update_rule_label(self):
        self.app.view.rule_label.text = self.cell_automaton.get_rule_set().__str__()

    def update_iterations_label(self):
        self.app.view.iterations_label.text = "Iterations: " + self.iterations.__str__()

    def set_clicked_cell(self, cell_row, cell_index):
        if cell_row is 0:
            if self.clicked_on_grid(cell_row, cell_index):
                current_initial_state = self.cell_automaton.initial_state

                clicked_cell = current_initial_state[cell_index]
                cell_factory = CellFactory(self.rule_set.get_cell_type())
                new_cell = cell_factory.create_cell_with_values(int(not clicked_cell.get_state()))
                self.app.view.update_cell(cell_row, cell_index, create_color(new_cell.get_color()))
                self.cell_automaton.update_cell(cell_index, new_cell)
                self.fetch_current_initial_state()

    def get_y_dimension_size(self):
        return self.get_iterations()

    def set_y_dimension_size(self, size):
        self.set_iterations(size)

    def set_iterations(self, iterations):
        self.iterations = iterations



