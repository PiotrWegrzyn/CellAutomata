from functools import partial

from kivy.core.window import Window
from kivy.uix.label import Label

from controler.GameOfLifeController import GameOfLifeController, create_color
from controler.BaseController import BaseController, generate_empty_2d_list_of_list
from model.CellAutomata.CellAutomaton1D import CellAutomaton1D
from model.Cells.CellFactory import CellFactory
from model.RuleSets.BinaryRuleSet import BinaryRuleSet
from view.BinaryRuleSetView import BinaryRuleSetView


class BinaryRuleSetController(BaseController):
    modes = {
        "Game of Life": GameOfLifeController,
    }
    rule_set = BinaryRuleSet

    def __init__(self, app, cell_size=9, cell_offset=1):
        self.cell_size = cell_size
        self.cell_offset = cell_offset
        self.cell_box_size = cell_size + cell_offset
        super().__init__(app)
        self.update_labels()
        self.app.view.grid.on_touch_down = self.on_touch_down


    def set_initial_view(self):
        self.set_view(BinaryRuleSetView(self.modes, self.get_menu_width()))

    def bind_buttons(self):
        super().bind_buttons()
        self.bind_draw_button()
        self.bind_columns_buttons()
        self.bind_iterations_buttons()
        self.bind_rule_buttons()
        self.bind_alive_cells_buttons()

    def setup(self):
        self.max_graphic_columns = self.get_view_max_columns()
        self.max_graphic_rows = self.get_view_max_rows()

        self.iterations = self.get_view_max_rows()
        self.set_empty_data_frame()

        self.cell_automaton = None
        self.set_cell_automaton_to_starting_state()

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

    def get_view_max_columns(self):
        return int((Window.size[0] - self.menu_item_width) / self.cell_box_size)

    def get_view_max_rows(self):
        return int(Window.size[1] / self.cell_box_size)

    def get_columns(self):
        return self.cell_automaton.get_columns()

    def get_iterations(self):
        return self.iterations

    def bind_draw_button(self):
        self.app.view.draw_btn.bind(on_press=partial(self.draw_graphic))

    def bind_columns_buttons(self):
        self.app.view.add_columns.bind(on_press=partial(self.add_columns_controller))
        self.app.view.sub_columns.bind(on_press=partial(self.sub_columns_controller))

    def bind_iterations_buttons(self):
        self.app.view.sub_iterations.bind(on_press=partial(self.sub_iterations_controller))
        self.app.view.add_iterations.bind(on_press=partial(self.add_iterations_controller))

    def bind_rule_buttons(self):
        self.app.view.add_rule.bind(on_press=partial(self.add_rule_controller))
        self.app.view.sub_rule.bind(on_press=partial(self.sub_rule_controller))

    def bind_alive_cells_buttons(self):
        self.app.view.sub_alive_cells.bind(on_press=partial(self.sub_alive_cells_controller))
        self.app.view.add_alive_cells.bind(on_press=partial(self.add_alive_cells_controller))

    def draw_graphic(self, button_instance):
        self.clear_canvas()
        self.fetch_data_frame()
        self.app.view.draw_data_frame(self.data_frame)
        # self.cell_automaton.print_iterations(self.iterations)

    def sub_columns_controller(self, button_instance):
        delta = -10
        current_value = self.cell_automaton.get_columns()
        if self.cell_automaton.get_columns() + delta > 0:
            self.cell_automaton.change_columns(current_value + delta)
            self.update_columns_label()

    def add_columns_controller(self, button_instance):
        delta = 10
        current_value = self.cell_automaton.get_columns()
        if current_value + delta > 0:
            self.cell_automaton.change_columns(current_value + delta)
            self.update_columns_label()

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
        delta = -5
        current_value = self.cell_automaton.get_rule_set().get_rule_base_10()
        self.set_cell_automaton(
            rule_set=BinaryRuleSet((current_value + delta) % 255),
            initial_state=self.cell_automaton.initial_state
        )
        self.update_rule_label()

    def add_rule_controller(self, button_instance):
        delta = 5
        current_value = self.cell_automaton.get_rule_set().get_rule_base_10()
        self.set_cell_automaton(
            rule_set=BinaryRuleSet((current_value + delta) % 255),
            initial_state=self.cell_automaton.initial_state
        )
        self.update_rule_label()

    def sub_alive_cells_controller(self, button_instance):
        delta = -0.05
        current_value = self.cell_automaton.get_percent_of_alive_cells()
        if current_value + delta > 0:
            self.cell_automaton.change_alive_cells_percentage(current_value + delta)
            self.update_alive_cells_label()

    def add_alive_cells_controller(self, button_instance):
        delta = 0.05
        current_value = self.cell_automaton.get_percent_of_alive_cells()
        if current_value + delta > 0:
            self.cell_automaton.change_alive_cells_percentage(current_value + delta)
            self.update_alive_cells_label()

    def fetch_data_frame(self):
        for iteration in range(0, self.iterations):
            self.data_frame[iteration] = self.cell_automaton.get_current_state()
            self.cell_automaton.calculate_next_iteration()
        self.cell_automaton.set_to_initial_state()

    def update_labels(self):
        self.update_columns_label()
        self.update_iterations_label()
        self.update_rule_label()
        self.update_alive_cells_label()

    def update_columns_label(self):
        self.app.view.columns_label.text = "Columns" + self.cell_automaton.get_columns().__str__()

    def update_rule_label(self):
        self.app.view.rule_label.text = self.cell_automaton.get_rule_set().__str__()

    def update_iterations_label(self):
        self.app.view.iterations_label.text = "Iterations: " + self.iterations.__str__()

    def update_alive_cells_label(self):
        self.app.view.alive_cells_label.text = \
            "Alive cells:\n"+"{:.1f}%".format(self.cell_automaton.get_percent_of_alive_cells()*100)

    def set_empty_data_frame(self):
        self.data_frame = generate_empty_2d_list_of_list(size=self.iterations)

    def on_touch_down(self, touch):
        print(self._get_graphic_cell_row_from_pos(touch.y), self._get_graphic_cell_column_from_pos(touch.x))
        self.set_clicked_cell(
            cell_row=self._get_graphic_cell_row_from_pos(touch.y),
            cell_index=self._get_graphic_cell_column_from_pos(touch.x)
        )

    def set_clicked_cell(self, cell_row, cell_index):
        if cell_row is 0:
            if self.clicked_on_grid(cell_row, cell_index):
                current_initial_state = self.cell_automaton.initial_state

                clicked_cell = current_initial_state[cell_index]
                cell_factory = CellFactory(self.rule_set.get_cell_type())
                new_cell = cell_factory.create_cell_with_values(int(not clicked_cell.get_value()))
                self.app.view.update_cell(cell_row, cell_index, create_color(new_cell.get_color()))
                self.cell_automaton.update_cell(cell_index, new_cell)
                self.fetch_current_initial_state()

    def _get_graphic_cell_y_pos(self, row):
        return Window.size[1] - ((row + 1) * self.cell_box_size)

    def _get_graphic_cell_x_pos(self, column):
        return self.menu_item_width+(column * self.cell_box_size)

    def _get_graphic_cell_column_from_pos(self, pos_y):
        return int((pos_y-self.menu_item_width) / self.cell_box_size)

    def _get_graphic_cell_row_from_pos(self, pos_x):
        return int(((Window.size[1]-pos_x)/self.cell_box_size))

    def clicked_on_grid(self, cell_row, cell_index):
        return 0 <= cell_index < self.cell_automaton.get_columns() and 0 <= cell_row < self.iterations

    def fetch_current_initial_state(self):
        self.data_frame[0] = self.cell_automaton.initial_state



