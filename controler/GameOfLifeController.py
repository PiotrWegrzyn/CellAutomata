import datetime
from functools import partial
from ast import literal_eval
from itertools import count

from kivy.clock import Clock
from kivy.graphics.context_instructions import Color

from controler.BaseController import BaseController, generate_empty_2d_list_of_list
from kivy.core.window import Window

from model.CellAutomata.CellAutomaton2D import CellAutomaton2D
from model.Cells.CellFactory import CellFactory
from model.RuleSets.GameOfLifeRuleSet import GameOfLifeRuleSet
from view.GameOfLifeView import GameOfLifeView


def create_color(color):
    rgb = color.rgb
    return Color(rgb[0], rgb[1], rgb[2])


class GameOfLifeController(BaseController):
    modes = {
         "Binary Rule": "BinaryRuleSetController",
    }
    rule_set = GameOfLifeRuleSet

    def __init__(self, app, cell_size=9, cell_offset=1):
        self.cell_size = cell_size
        self.cell_offset = cell_offset
        self.cell_box_size = cell_size + cell_offset
        super().__init__(app)
        self.iteration_speed = 8
        self.update_labels()
        self.app.view.grid.on_touch_down = self.on_touch_down

    def set_initial_view(self):
        self.set_view(GameOfLifeView(self.modes, self.get_menu_width()))

    def bind_buttons(self):
        super().bind_buttons()
        self.bind_draw_button()
        self.bind_columns_buttons()
        self.bind_rows_buttons()
        self.bind_alive_cells_buttons()
        self.bind_file_buttons()
        self.bind_load_btn()
        self.bind_save_btn()
        self.bind_speed_elements()
        self.bind_start_stop_elements()

    def setup(self):
        self.max_graphic_columns = self.get_view_max_columns()
        self.max_graphic_rows = self.get_view_max_rows()

        self.cell_automaton = None
        self.set_cell_automaton_to_starting_state()
        self.set_empty_data_frame()

    def set_cell_automaton_to_starting_state(self):
        self.set_cell_automaton(
            columns=self.get_view_max_columns(),
            rows = self.get_view_max_rows(),
            rule_set=self.rule_set(),
            p_of_alive=0.2
        )

    def set_cell_automaton(self, columns=None, rows=None, rule_set=None, p_of_alive=None):
        if columns is None:
            columns = self.cell_automaton.get_columns()
        if rows is None:
            rows = self.cell_automaton.get_rows()
        if rule_set is None:
            rule_set = self.cell_automaton.get_rule_set()
        if p_of_alive is None:
            p_of_alive = self.cell_automaton.get_percent_of_alive_cells()

        self.cell_automaton = CellAutomaton2D(
            columns=columns,
            rows = rows,
            rule_set=rule_set,
            percent_of_alive_cells=p_of_alive
        )

    def get_view_max_columns(self):
        return int((Window.size[0] - self.menu_item_width) / self.cell_box_size)

    def get_view_max_rows(self):
        return int(Window.size[1] / self.cell_box_size)

    def get_columns(self):
        return self.cell_automaton.get_columns()

    def get_rows(self):
        return self.cell_automaton.get_rows()

    def bind_draw_button(self):
        self.app.view.draw_btn.bind(on_press=partial(self.draw_btn_controller))

    def bind_columns_buttons(self):
        self.app.view.add_columns.bind(on_press=partial(self.add_columns_controller))
        self.app.view.sub_columns.bind(on_press=partial(self.sub_columns_controller))

    def bind_rows_buttons(self):
        self.app.view.sub_rows.bind(on_press=partial(self.sub_rows_controller))
        self.app.view.add_rows.bind(on_press=partial(self.add_rows_controller))

    def bind_alive_cells_buttons(self):
        self.app.view.sub_alive_cells.bind(on_press=partial(self.sub_alive_cells_controller))
        self.app.view.add_alive_cells.bind(on_press=partial(self.add_alive_cells_controller))

    def draw_btn_controller(self, button_instance):
        self.draw_one_iteration()

    def sub_columns_controller(self, button_instance):
        delta = -10
        current_value = self.cell_automaton.get_columns()
        if self.cell_automaton.get_columns() + delta > 0:
            self.cell_automaton.change_columns(current_value + delta)
            self.set_empty_data_frame()
            self.update_columns_label()

    def add_columns_controller(self, button_instance):
        delta = 10
        current_value = self.cell_automaton.get_columns()
        if current_value + delta > 0:
            self.cell_automaton.change_columns(current_value + delta)
            self.set_empty_data_frame()
            self.update_columns_label()

    def sub_rows_controller(self, button_instance):
        delta = -10
        current_value = self.cell_automaton.get_rows()
        if current_value + delta > 0:
            self.cell_automaton.change_rows(current_value + delta)
            self.set_empty_data_frame()
            self.update_rows_label()

    def add_rows_controller(self, button_instance):
        delta = 10
        current_value = self.cell_automaton.get_rows()
        if current_value + delta > 0:
            self.cell_automaton.change_rows(current_value + delta)
            self.set_empty_data_frame()
            self.update_rows_label()

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

    def yield_data_frame(self):
        self.fetch_current_state()
        self.cell_automaton.calculate_next_iteration()

    def fetch_current_state(self):
        self.data_frame = self.cell_automaton.get_current_state()

    def update_labels(self):
        self.update_columns_label()
        self.update_rows_label()
        self.update_alive_cells_label()
        self.update_speed_label()

    def update_columns_label(self):
        self.app.view.columns_label.text = "Columns" + self.cell_automaton.get_columns().__str__()

    def update_rows_label(self):
        self.app.view.rows_label.text = "Rows: " + self.cell_automaton.get_rows().__str__()

    def update_alive_cells_label(self):
        self.app.view.alive_cells_label.text = \
            "Alive cells:\n"+"{:.1f}%".format(self.cell_automaton.get_percent_of_alive_cells()*100)

    def set_empty_data_frame(self):
        self.data_frame = generate_empty_2d_list_of_list(size=self.cell_automaton.get_rows())

    def bind_file_buttons(self):
        for btn in self.app.view.file_buttons:
            btn.bind(on_press=partial(self.load_file_controller))

    def bind_load_btn(self):
        self.app.view.load_btn.bind(on_press=partial(self.load_btn_controller))

    def bind_save_btn(self):
        self.app.view.save_btn.bind(on_press=partial(self.save_btn_controller))

    def bind_start_stop_elements (self):
        self.app.view.play_btn.bind(on_press=partial(self.play_btn_controller))
        self.app.view.stop_btn.bind(on_press=partial(self.stop_btn_controller))

    def bind_speed_elements(self):
        self.app.view.faster_btn.bind(on_press=partial(self.faster_btn_controller))
        self.app.view.slower_btn.bind(on_press=partial(self.slower_btn_controller))

    def load_file_controller(self, btn_instance):
        with open("./patterns/" + btn_instance.text) as f:
            raw_saved_state = [list(literal_eval(line)) for line in f]

        loaded_state_rows = len(raw_saved_state)
        loaded_state_columns = len(raw_saved_state[0])

        self.cell_automaton.change_rows(loaded_state_rows)
        self.cell_automaton.change_columns(loaded_state_columns)

        cell_factory = CellFactory(self.rule_set.get_cell_type())
        saved_state_cells = generate_empty_2d_list_of_list(loaded_state_rows)
        # just python magic
        for row_index, row_content in zip(range(0, loaded_state_rows), raw_saved_state):
            for value in row_content:
                saved_state_cells[row_index].append(cell_factory.create_cell_with_values(value))
        self.cell_automaton.current_state = saved_state_cells

        self.draw_one_iteration()

    def load_btn_controller(self, btn_instance):
        self.app.view.show_choose_file_menu()

    def save_btn_controller(self, btn_instance):
        self.cell_automaton.print_iterations(1)
        self.save_current_state_to_file()

    def play_btn_controller(self, btn_instance):
        self.draw_one_iteration()
        self.restart_auto_iterations_clock()

    def stop_btn_controller(self, btn_instance):
        self.stop_iterations()

    def slower_btn_controller(self, btn_instance):
        self.change_iterations_speed(delta=0.5)

    def faster_btn_controller(self, btn_instance):
        self.change_iterations_speed(delta=2)

    def change_iterations_speed(self, delta):
        current_value = self.iteration_speed
        new_value = int(current_value * delta)
        if new_value > 0:
            self.iteration_speed = new_value
            self.restart_auto_iterations_clock()
            self.update_speed_label()

    def save_current_state_to_file(self):
        iteration = self.cell_automaton.iterations_to_list(1)
        file = open(self.generate_file_name(), "w+")
        for row in range(0, len(iteration[0])):
            file.write([cell.get_value() for cell in iteration[0][row]].__str__() + "\n")

    def generate_file_name(self):
        return "patterns\\CA"+self.cell_automaton.get_rule_set().__str__() \
               +"-"+ datetime.datetime.now().__str__().replace(' ', '-').replace(':', '-') + ".txt"

    def draw_one_iteration(self):
        self.clear_canvas()
        self.yield_data_frame()
        self.app.view.draw_data_frame(self.data_frame)
        self.update_alive_cells_label()
        # self.cell_automaton.print_rows(self.rows)

    def restart_auto_iterations_clock(self):
        self.stop_iterations()
        self._start_iterations()

    def stop_iterations(self):
        try:
            self.auto_iterations.cancel()
        except AttributeError:
            pass

    def _start_iterations(self):
        self.auto_iterations = Clock.schedule_interval(self.draw_btn_controller, 1 / self.iteration_speed)

    def update_speed_label(self):

        self.app.view.speed_label.text = "Speed:" + self.iteration_speed.__str__() + " fps"

    def on_touch_down(self, touch):
        print(self._get_graphic_cell_row_from_pos(touch.y),self._get_graphic_cell_column_from_pos(touch.x))
        self.set_clicked_cell(
            cell_row=self._get_graphic_cell_row_from_pos(touch.y),
            cell_index=self._get_graphic_cell_column_from_pos(touch.x)
        )

    def set_clicked_cell(self, cell_row, cell_index):
        if self.clicked_on_grid(cell_row, cell_index):
            cstate = self.cell_automaton.get_current_state()

            clicked_cell = cstate[cell_row][cell_index]
            cell_factory = CellFactory(self.rule_set.get_cell_type())
            new_cell = cell_factory.create_cell_with_values(int(not clicked_cell.get_value()))
            self.app.view.update_cell(cell_row, cell_index, create_color(clicked_cell.get_color()))
            self.cell_automaton.update_cell(cell_row, cell_index, new_cell)
            self.fetch_current_state()

    def _get_graphic_cell_y_pos(self, row):
        return Window.size[1] - ((row + 1) * self.cell_box_size)

    def _get_graphic_cell_x_pos(self, column):
        return self.menu_item_width+(column * self.cell_box_size)

    def _get_graphic_cell_column_from_pos(self, pos_y):
        return int((pos_y-self.menu_item_width) / self.cell_box_size)

    def _get_graphic_cell_row_from_pos(self, pos_x):
        return int(((Window.size[1]-pos_x)/self.cell_box_size))

    def clicked_on_grid(self, cell_row, cell_index):
        return 0 <= cell_index < self.cell_automaton.get_columns() and 0 <= cell_row < self.cell_automaton.get_rows()

