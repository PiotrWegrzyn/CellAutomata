import datetime
from functools import partial
from ast import literal_eval
from kivy.clock import Clock
from controler.AutomatonController import AutomatonController
from controler.BaseController import generate_empty_2d_list_of_list, create_color
from model.Cells.CellFactory import CellFactory
from model.RuleSets.GameOfLifeRuleSet import GameOfLifeRuleSet
from view.GameOfLifeView import GameOfLifeView


class GameOfLifeController(AutomatonController):

    rule_set = GameOfLifeRuleSet()

    def __init__(self, app, cell_size=9, cell_offset=1):
        self.iteration_speed = 8
        super().__init__(app, cell_size, cell_offset)
        self.app.view.draw_btn.text = "Next\nIteration"     # todo move to view
        self.app.view.grid.on_touch_down = self.on_touch_down
        self.draw_current_state()

    def set_initial_view(self):
        self.set_view(GameOfLifeView(self.modes, self.get_menu_width()))

    def bind_buttons(self):
        super().bind_buttons()
        self.bind_rows_buttons()
        self.bind_file_buttons()
        self.bind_load_btn()
        self.bind_save_btn()
        self.bind_speed_elements()
        self.bind_start_stop_elements()
        self.bind_rule_input()
        self.bind_reverse_colors_checkbox()
        self.bind_clear_button()

    def set_cell_automaton_to_starting_state(self):
        self.set_cell_automaton(
            columns=self.get_view_max_columns(),
            rows=self.get_view_max_rows(),
            rule_set=self.rule_set,
            p_of_alive=0.2
        )

    def get_rows(self):
        return self.cell_automaton.get_rows()

    def bind_rows_buttons(self):
        self.app.view.sub_rows.bind(on_press=partial(self.sub_rows_controller))
        self.app.view.add_rows.bind(on_press=partial(self.add_rows_controller))

    def draw_button_controller(self, button_instance):
        self.draw_next_iteration()

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

    def yield_next_data_frame(self):
        self.cell_automaton.calculate_next_iteration()
        self.fetch_current_state()

    def fetch_current_data_frame(self):
        self.fetch_current_state()

    def fetch_current_state(self):
        new_state = self.cell_automaton.get_current_state()
        if self.rule_set.reverse_colors is False:
            self.data_frame = \
                [[cell.get_color_representation() for cell in new_state[row]] for row in range(0, self.cell_automaton.get_rows())]
        else:
            self.data_frame = \
                [[cell.get_reversed_color_representation() for cell in new_state[row]] for row in
                 range(0, self.cell_automaton.get_rows())]

    def update_labels(self):
        self.update_columns_label()
        self.update_rows_label()
        self.update_alive_cells_label()
        self.update_speed_label()

    def update_rows_label(self):
        self.app.view.rows_label.text = "Rows: " + self.cell_automaton.get_rows().__str__()

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
        for row_index, row_content in zip(range(0, loaded_state_rows), raw_saved_state):
            for value in row_content:
                saved_state_cells[row_index].append(cell_factory.create_cell_with_values(value))
        self.cell_automaton.current_state = saved_state_cells

        self.draw_next_iteration()

    def load_btn_controller(self, btn_instance):
        self.app.view.show_choose_file_menu()

    def save_btn_controller(self, btn_instance):
        self.cell_automaton.print_iterations(1)
        self.save_current_state_to_file()

    def play_btn_controller(self, btn_instance):
        self.draw_next_iteration()
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
            file.write([cell.get_state() for cell in iteration[0][row]].__str__() + "\n")

    def generate_file_name(self):
        return "patterns\\"+self.cell_automaton.get_rule_set().__str__() \
               +"-"+ datetime.datetime.now().__str__().replace(' ', '-').replace(':', '-') + ".txt"

    def draw_next_iteration(self):
        self.clear_canvas()
        self.yield_next_data_frame()
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
        self.draw_current_state()
        self.auto_iterations = Clock.schedule_interval(self.draw_button_controller, 1 / self.iteration_speed)

    def update_speed_label(self):

        self.app.view.speed_label.text = "Speed:" + self.iteration_speed.__str__() + " fps"

    def on_touch_down(self, touch):
        print(self._get_graphic_cell_row_from_pos(touch.y), self._get_graphic_cell_column_from_pos(touch.x))
        self.set_clicked_cell(
            cell_row=self._get_graphic_cell_row_from_pos(touch.y),
            cell_index=self._get_graphic_cell_column_from_pos(touch.x)
        )

    def set_clicked_cell(self, cell_row, cell_index):
        if self.clicked_on_grid(cell_row, cell_index):
            cstate = self.cell_automaton.get_current_state()

            clicked_cell = cstate[cell_row][cell_index]
            clicked_cell.flip_state()

            self.app.view.update_cell(cell_row, cell_index, create_color(clicked_cell.get_color()))
            self.cell_automaton.update_cell(cell_row, cell_index, clicked_cell)
            self.fetch_current_state()

    def get_y_dimension_size(self):
        return self.get_rows()

    def set_y_dimension_size(self, size):
        self.cell_automaton.change_rows(size)

    def change_mode_controller(self, btn_instance):
        self.app.set_controller(btn_instance.text)
        self.stop_iterations()

    def bind_rule_input(self):
        self.app.view.rule_input.bind(on_text_validate=partial(self.rule_input_controller))

    def rule_input_controller(self, value):
        self.rule_set = GameOfLifeRuleSet(
            rule_code=value.text,
            reverse_colors=self.rule_set.reverse_colors
        )
        self.set_cell_automaton(rule_set=self.rule_set)
        self.clear_canvas()

    def bind_reverse_colors(self):
        self.app.view.rule_input.bind(on_text_validate=partial(self.rule_input_controller))

    def bind_reverse_colors_checkbox(self):
        self.app.view.reverse_colors_checkbox.bind(active=partial(self.on_checkbox_active))

    def on_checkbox_active(self, checkbox, value):
        self.rule_set = GameOfLifeRuleSet(
            rule_code=self.rule_set.rule_code,
            reverse_colors=value
        )
        self.set_cell_automaton(rule_set=self.rule_set)

    def bind_clear_button(self):
        self.app.view.clear_button.bind(on_press=partial(self.clear_state_controller))

    def clear_state_controller(self, instance):
       self.clear_ca_state_and_canvas()

    def clear_ca_state_and_canvas(self):
        self.cell_automaton.set_to_empty_state()
        self.draw_current_state()

