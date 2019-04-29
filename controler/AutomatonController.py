from functools import partial

from kivy.core.window import Window

from controler.BaseController import BaseController, generate_empty_2d_list_of_list
from model.CellAutomata.CellAutomatonFactory import CellAutomatonFactory
from model.RuleSets.BinaryRuleSet import BinaryRuleSet
from view.BaseView import BaseView


class AutomatonController(BaseController):

    rule_set = BinaryRuleSet

    def __init__(self, app, cell_size=9, cell_offset=1):
        self.cell_size = cell_size
        self.cell_offset = cell_offset
        self.cell_box_size = cell_size + cell_offset
        super().__init__(app)
        self.update_labels()
        self.app.view.grid.on_touch_down = self.on_touch_down

    def set_initial_view(self):
        self.set_view(BaseView(self.modes, self.get_menu_width()))

    def bind_buttons(self):
        super().bind_buttons()
        self.bind_draw_button()
        self.bind_columns_buttons()
        self.bind_alive_cells_buttons()

    def setup(self):
        self.max_graphic_columns = self.get_view_max_columns()
        self.max_graphic_rows = self.get_view_max_rows()

        self.cell_automaton = None
        self.set_cell_automaton_to_starting_state()

        self.set_empty_data_frame()

    def set_cell_automaton_to_starting_state(self):
        self.set_cell_automaton(
            columns=self.get_view_max_columns(),
            rule_set=self.rule_set(90),
            p_of_alive=0.2
        )

    def set_cell_automaton(self, columns=None, rows=None, rule_set=None, p_of_alive=None, initial_state=None):
        if columns is None:
            columns = self.cell_automaton.get_columns()
        if rule_set is None:
            rule_set = self.cell_automaton.get_rule_set()
        if p_of_alive is None:
            p_of_alive = self.cell_automaton.get_percent_of_alive_cells()
        if rows is None:
            try:
                rows = self.cell_automaton.get_rows()
            except AttributeError:
                rows = None

        automaton_factory = CellAutomatonFactory()

        self.cell_automaton = automaton_factory.create(
            rule_set=rule_set,
            columns=columns,
            rows=rows,
            percent_of_alive_cells=p_of_alive,
            initial_state=initial_state
        )

    def _set_to_previous_values(self, columns, rows, rule_set, p_of_alive, initial_state):
        pass

    def get_view_max_columns(self):
        return int((Window.size[0] - self.menu_item_width) / self.cell_box_size)

    def get_view_max_rows(self):
        return int(Window.size[1] / self.cell_box_size)

    def get_columns(self):
        return self.cell_automaton.get_columns()

    def bind_draw_button(self):
        self.app.view.draw_btn.bind(on_press=partial(self.draw_button_controller))

    def bind_columns_buttons(self):
        self.app.view.add_columns.bind(on_press=partial(self.add_columns_controller))
        self.app.view.sub_columns.bind(on_press=partial(self.sub_columns_controller))

    def bind_alive_cells_buttons(self):
        self.app.view.sub_alive_cells.bind(on_press=partial(self.sub_alive_cells_controller))
        self.app.view.add_alive_cells.bind(on_press=partial(self.add_alive_cells_controller))

    def draw_button_controller(self, button_instance):
        self.draw_current_state()

    def sub_columns_controller(self, button_instance):
        self.change_columns(delta=-10)

    def add_columns_controller(self, button_instance):
        self.change_columns(delta=10)

    def change_columns(self, delta):
        current_value = self.cell_automaton.get_columns()
        if current_value + delta > 0:
            self.cell_automaton.change_columns(current_value + delta)
            self.update_columns_label()

    def sub_alive_cells_controller(self, button_instance):
        delta = -0.05
        current_value = self.cell_automaton.get_percent_of_alive_cells()
        if current_value + delta > 0:
            self.cell_automaton.change_alive_cells_percentage(current_value + delta)
            self.update_alive_cells_label()

    def add_alive_cells_controller(self, button_instance):
        delta = 0.05
        current_value = self.cell_automaton.get_percent_of_alive_cells()
        if current_value + delta <= 1:
            self.cell_automaton.change_alive_cells_percentage(current_value + delta)
            self.update_alive_cells_label()

    def update_labels(self):
        self.update_columns_label()
        self.update_alive_cells_label()

    def update_columns_label(self):
        self.app.view.columns_label.text = "Columns" + self.cell_automaton.get_columns().__str__()

    def update_alive_cells_label(self):
        self.app.view.alive_cells_label.text = \
            "Alive cells:\n"+"{:.1f}%".format(self.cell_automaton.get_percent_of_alive_cells()*100)

    def set_empty_data_frame(self):
        self.data_frame = generate_empty_2d_list_of_list(size=self.get_y_dimension_size())

    def on_touch_down(self, touch):
        print(self._get_graphic_cell_row_from_pos(touch.y), self._get_graphic_cell_column_from_pos(touch.x))
        self.set_clicked_cell(
            cell_row=self._get_graphic_cell_row_from_pos(touch.y),
            cell_index=self._get_graphic_cell_column_from_pos(touch.x)
        )

    def _get_graphic_cell_y_pos(self, row):
        return Window.size[1] - ((row + 1) * self.cell_box_size)

    def _get_graphic_cell_x_pos(self, column):
        return self.menu_item_width+(column * self.cell_box_size)

    def _get_graphic_cell_column_from_pos(self, pos_y):
        return int((pos_y-self.menu_item_width) / self.cell_box_size)

    def _get_graphic_cell_row_from_pos(self, pos_x):
        return int(((Window.size[1]-pos_x)/self.cell_box_size))

    def clicked_on_grid(self, cell_row, cell_index):
        return 0 <= cell_index < self.cell_automaton.get_columns() and 0 <= cell_row < self.get_y_dimension_size()

    def draw_current_state(self):
        self.clear_canvas()
        self.fetch_current_data_frame()
        self.app.view.draw_data_frame(self.data_frame)
        self.update_alive_cells_label()

        # self.cell_automaton.print_iterations(self.iterations)

    def get_y_dimension_size(self):
        pass

    def set_clicked_cell(self, cell_row, cell_index):
        pass

    def fetch_current_initial_state(self):
        if self.rule_set.get_required_dimension() is 1:
            self.data_frame[0] = self.cell_automaton.initial_state
        else:
            self.data_frame = self.cell_automaton.initial_state

    def fetch_current_data_frame(self):
        pass
