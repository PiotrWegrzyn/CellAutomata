import datetime
from functools import partial

from kivy.clock import Clock
from kivy.graphics.context_instructions import Color

from model.CellAutomaton import *
from kivy.core.window import Window


class ViewController:
    def __init__(self, view, cell_size=9, cell_offset=1, mode=2, rule=90):
        self.view = view
        self.cell_size = cell_size
        self.cell_offset = cell_offset
        self.cell_box_size = cell_size + cell_offset
        self.collect_initial_data_from_view_mode = False
        self.menu_item_width = 100
        self.max_graphic_columns = self.get_view_max_columns()
        self.max_graphic_rows = self.get_view_max_rows()
        self.iteration_speed = 8

        self.data_frame = generate_empty_2d_list_of_list(size=self.max_graphic_rows)

        self.automaton_rule = rule
        self.automaton_mode = mode
        self.automaton_rows_count = self.get_view_max_columns()
        self.automaton_columns_count = self.get_view_max_rows()
        self.automaton_iterations = self.get_view_max_rows()
        self.cell_automaton = None
        self.set_cell_automaton()

    def set_cell_automaton(self):
        try:
            current_alive_percentage = self.cell_automaton.percentage_of_alive_cells
        except AttributeError:
            current_alive_percentage = 0.2

        if self.automaton_mode is CellAutomaton.modes["1D"]:
            self.cell_automaton = CellAutomaton(
                mode=self.automaton_mode,
                rows_count=self.automaton_rows_count,
                columns_count=self.automaton_columns_count,
                rule=self.automaton_rule,
                percentage_of_alive_cells=current_alive_percentage
            )

        if self.automaton_mode is CellAutomaton.modes["2D"]:
            self.cell_automaton = CellAutomaton(
                mode=self.automaton_mode,
                rows_count=self.automaton_rows_count,
                columns_count=self.automaton_columns_count,
                percentage_of_alive_cells=current_alive_percentage
            )

    def get_view_max_columns(self):
        return int((Window.size[0] - self.menu_item_width) / self.cell_box_size)

    def get_view_max_rows(self):
        return int(Window.size[1] / self.cell_box_size)

    def play_iterations_controller(self, instance):
        self.clear_and_draw_data_frame()
        self.restart_auto_iterations_clock()

    def stop_iterations_controller(self, instance):
        self.stop_iterations()

    def draw_one_iteration_controller(self, instance):
        self.set_next_data_frame()
        self.clear_and_draw_data_frame()
        self.update_alive_cells_label()

    def slower_iterations_controller(self, instance):
        new_value = self.calculate_new_speed_value(change=0.5)
        if self.validate_new_speed_value(new_value):
            self.iteration_speed = new_value
            self.restart_auto_iterations_clock()
            self.update_speed_label()

    def faster_iterations_controller(self, instance):
        self.iteration_speed = self.get_iteration_speed() * 2
        self.restart_auto_iterations_clock()
        self.update_speed_label()

    def change_mode_controller(self, btn_instance):
        self.stop_iterations()
        self.view.clear_canvas()
        self.view.clear_menu()

        if self.automaton_mode is CellAutomaton.modes["1D"]:
            self.automaton_mode = CellAutomaton.modes["2D"]
            self.view.draw_2d_menu()
        elif self.automaton_mode is CellAutomaton.modes["2D"]:
            self.automaton_mode = CellAutomaton.modes["1D"]
            self.view.draw_1d_menu()
        self.set_cell_automaton()

    def draw_initial_state_controller(self, btn_instance):
        self.cell_automaton.set_to_initial_state()
        self.set_next_data_frame()
        self.clear_and_draw_data_frame()

    def set_state_controller(self, btn_instance):
        self.collect_initial_data_from_view_mode = True

    def sub10_rule_controller(self, btn_instance):
        self.cell_automaton.change_rule((self.cell_automaton.get_rule() - 10) % 255)
        self.update_rule_label()
        self.reset_canvas()


    def add10_rule_controller(self, btn_instance):
        self.cell_automaton.change_rule((self.cell_automaton.get_rule() + 10) % 255)
        self.update_rule_label()
        self.reset_canvas()

    def sub10_rows_count_controller(self, btn_instance):
        change_value = 10
        if self.validate_size_change(change_value,0):
            self.cell_automaton.change_size((self.cell_automaton.get_rows_count() - change_value), self.cell_automaton.get_columns_count())
            self.automaton_rows_count -= change_value
            self.update_rows_count_label()
            self.reset_canvas()

    def add10_rows_count_controller(self, btn_instance):
        self.cell_automaton.change_size((self.cell_automaton.get_rows_count() + 10), self.cell_automaton.get_columns_count())
        self.automaton_rows_count += 10
        self.update_rows_count_label()
        self.reset_canvas()

    def sub10_columns_count_controller(self, btn_instance):
        change_value = 10
        if self.validate_size_change(0, change_value):
            self.cell_automaton.change_size(self.cell_automaton.get_rows_count(), (self.cell_automaton.get_columns_count() - change_value))
            self.automaton_columns_count -= change_value
            self.update_columns_count_label()
            self.reset_canvas()

    def add10_columns_count_controller(self, btn_instance):
        self.cell_automaton.change_size(self.cell_automaton.get_rows_count(), (self.cell_automaton.get_columns_count() + 10))
        self.automaton_columns_count += 10
        self.update_columns_count_label()
        self.reset_canvas()

    def sub10_iterations_controller(self, btn_instance):
        value = 10
        if self.automaton_iterations - value >= 0:
            self.automaton_iterations -= value
        self.update_iterations_label()
        self.automaton_rows_count -= value
        # self._reset_data_frame()
        self.reset_canvas()

    def add10_iterations_controller(self, btn_instance):
        self.automaton_iterations += 10
        self.update_iterations_label()
        self.automaton_rows_count += 10
        # self._reset_data_frame()
        self.reset_canvas()

    def sub5p_alive_cells_controller(self, btn_instance):
        value = 0.05
        if self.cell_automaton.get_alive_cell_percentage()-value >= 0:
            self.cell_automaton.change_alive_cells_percentage(self.cell_automaton.get_alive_cell_percentage()-value)
        self.update_alive_cells_label()
        self.reset_canvas()

    def add5p_alive_cells_controller(self,btn_instance):
        value = 0.05
        if self.cell_automaton.get_alive_cell_percentage()+value <= 1:
            self.cell_automaton.change_alive_cells_percentage(self.cell_automaton.get_alive_cell_percentage()+value)
        self.update_alive_cells_label()
        self.reset_canvas()

    def get_iterations(self):
        return self.automaton_iterations

    def get_rows_count(self):
        return self.automaton_rows_count

    def get_columns_count(self):
        return self.automaton_columns_count

    def get_iteration_speed(self):
        return self.iteration_speed

    def get_rule(self):
        return self.automaton_rule

    def stop_iterations(self):
        try:
            self.auto_iterations.cancel()
        except AttributeError:
            pass

    def get_menu_width(self):
        return self.menu_item_width

    def get_data_frame(self):
        return self.data_frame

    def _reset_data_frame(self):
        self.data_frame = generate_empty_2d_list_of_list(size=self.automaton_rows_count)

    def clear_and_draw_data_frame(self):
        self.view.clear_canvas()
        self.view.draw_data_frame(self.data_frame)

    def set_next_data_frame(self):
        if self.automaton_mode is CellAutomaton.modes["1D"]:
            for iteration in range(0, self.automaton_iterations):
                self.data_frame[iteration] = self.cell_automaton.get_current_state()
                self.cell_automaton.calculate_next_iteration()
            self.cell_automaton.set_to_initial_state()

        if self.automaton_mode is CellAutomaton.modes["2D"]:
            self.cell_automaton.calculate_next_iteration()
            self.data_frame = self.cell_automaton.get_current_state()

    def set_current_data_frame(self):
        if self.automaton_mode is CellAutomaton.modes["1D"]:
            for iteration in range(0, self.automaton_iterations):
                self.data_frame[iteration] = self.cell_automaton.get_current_state()
                self.cell_automaton.calculate_next_iteration()
            self.cell_automaton.set_to_initial_state()

        if self.automaton_mode is CellAutomaton.modes["2D"]:
            self.data_frame = self.cell_automaton.get_current_state()

    def update_rule_label(self):
        self.view.rule_label.text = "Rule: "+self.cell_automaton.get_rule().__str__()

    def update_rows_count_label(self):
        self.view.rows_count_label.text = "Rows: "+self.cell_automaton.get_rows_count().__str__()

    def update_columns_count_label(self):
        self.view.columns_count_label.text = "Columns: "+self.cell_automaton.get_columns_count().__str__()

    def update_iterations_label(self):
        self.view.iterations_label.text = "Iterations: "+self.get_iterations().__str__()

    def update_alive_cells_label(self):
        self.view.alive_cells_label.text = "Alive cells:\n"+"{:.1f}%".format(self.cell_automaton.percentage_of_alive_cells*100)

    def get_alive_cell_percentage(self):
        return self.cell_automaton.get_alive_cell_percentage()

    def _start_iterations(self):
        self.auto_iterations = Clock.schedule_interval(self.draw_one_iteration_controller, 1 / self.iteration_speed)

    def restart_auto_iterations_clock(self):
        self.stop_iterations()
        self._start_iterations()

    def update_speed_label(self):
        self.view.speed_label.text = "Speed: " + self.get_iteration_speed().__str__() +"fps"

    def calculate_new_speed_value(self, change):
        return int(self.get_iteration_speed() * change)

    def validate_new_speed_value(self, new_value):
        return new_value > 0

    def validate_size_change(self, dx, dy):
        return self.cell_automaton.get_rows_count() - dx > 0 and self.cell_automaton.get_columns_count() - dy > 0

    def set_clicked_cell(self, cell_row, cell_index):
        if self.clicked_on_grid(cell_row, cell_index):
            cstate = self.cell_automaton.get_current_state()
            if self.automaton_mode is CellAutomaton.modes["1D"]:
                if cell_row is 0:
                    current_value = cstate[cell_index]
                    new_value = int(not current_value)
                    if new_value is 1:
                        self.view.update_cell(cell_row, cell_index, Color(0, 0, 1))
                    else:
                        self.view.update_cell(cell_row, cell_index, Color(1, 1, 1))
                    self.cell_automaton.set_cell(new_value, cell_index)

            elif self.automaton_mode is CellAutomaton.modes["2D"]:
                current_value = cstate[cell_row][cell_index]
                new_value = int(not current_value)
                if new_value is 1:
                    self.view.update_cell(cell_row, cell_index, Color(0, 0, 1))
                else:
                    self.view.update_cell(cell_row, cell_index, Color(1, 1, 1))
                self.cell_automaton.set_cell(new_value, cell_index, cell_row)

    def clicked_on_grid(self, cell_row, cell_index):
        return 0 <= cell_index < self.cell_automaton.get_columns_count() and 0 <= cell_row < self.cell_automaton.get_rows_count()

    def save_current_state_controller(self, btn_instance):
        self.cell_automaton.print_iterations(1)
        self.save_current_state_to_file()

    def save_current_state_to_file(self):
        iteration = self.cell_automaton.iterations_to_list(1)
        file = open(self.generate_file_name(), "w+")
        for row in range(0, len(iteration[0])):
            file.write(iteration[0][row].__str__() + "\n")

    def reset_canvas(self):
        self.set_current_data_frame()
        self.clear_and_draw_data_frame()

    def generate_file_name(self):
        return "patterns\\CA"+self.cell_automaton.mode.__str__() +"-"+ datetime.datetime.now().__str__().replace(' ', '-').replace(':', '-') + ".txt"

    def load_state_from_file_controller(self, btn_instance):
        from ast import literal_eval
        # print(btn_instance.text)
        with open("./patterns/"+btn_instance.text) as f:
            saved_state = [list(literal_eval(line)) for line in f]
        self.cell_automaton.change_size(len(saved_state), len(saved_state[0]))
        self.cell_automaton.current_state = saved_state
        self.reset_canvas()

    def back_button_controller(self, btn_instanc):
        self.view.clear_menu()
        self.view.draw_2d_menu()

    def show_load_file_menu_controller(self, btn_instance):
        self.view.clear_menu()
        self.view.draw_choose_file_menu()


