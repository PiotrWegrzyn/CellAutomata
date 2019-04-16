from functools import partial

from kivy.clock import Clock

from model.CellAutomaton import *
from kivy.core.window import Window


class ViewController:
    def __init__(self, view, cell_size, cell_offset,mode = 2, window_width=640, window_height=400, rule=90):
        self.view = view
        self.cell_size = cell_size
        self.cell_offset = cell_offset
        self.cell_box_size = cell_size + cell_offset
        # self.set_view_cell_properties()
        self.menu_item_width = 100
        self.max_graphic_columns = self.get_view_max_columns()
        self.max_graphic_rows = self.get_view_max_rows()
        self.iteration_speed = 2

        self.data_frame = generate_empty_2d_list_of_list(size=self.max_graphic_rows)

        self.automaton_rule = rule
        self.automaton_mode = mode
        self.automaton_size = self.max_graphic_columns
        self.automaton_iterations = self.get_view_max_rows()
        self.cell_automaton = None
        self.set_cell_automaton()

    def set_cell_automaton(self):
        try:
            current_alive_percentage = self.cell_automaton.percentage_of_alive_cells
        except AttributeError:
            current_alive_percentage = 0.2

        if self.automaton_mode is CellularAutomaton.modes["1D"]:
            self.cell_automaton = CellularAutomaton(
                mode=self.automaton_mode,
                size=self.max_graphic_columns,
                rule=self.automaton_rule,
                percentage_of_alive_cells=current_alive_percentage
            )

        if self.automaton_mode is CellularAutomaton.modes["2D"]:
            self.cell_automaton = CellularAutomaton(
                mode=self.automaton_mode,
                size=self.max_graphic_rows,
                percentage_of_alive_cells=current_alive_percentage
            )

    def get_view_max_columns(self):
        return int((Window.size[0] - self.menu_item_width) / self.cell_box_size)

    def get_view_max_rows(self):
        return int(Window.size[1] / self.cell_box_size)

    def play_iterations_controller(self, instance):
        self.draw_data_frame()
        self.stop_iterations()
        self.auto_iterations = Clock.schedule_interval(self.draw_next_iteration_controller, 1/self.iteration_speed)

    def stop_iterations_controller(self, instance):
        self.stop_iterations()

    def draw_next_iteration_controller(self, instance):
        self.set_data_frame()
        self.draw_data_frame()

    def slower_iterations_controller(self, instance):
        pass

    def faster_iterations_controller(self, instance):
        pass

    def change_mode_controller(self, btn_instance):
        self.stop_iterations()
        # self.view.layout.canvas.clear()
        self.view.clear_menu()

        if self.automaton_mode is CellularAutomaton.modes["1D"]:
            self.automaton_mode = CellularAutomaton.modes["2D"]
            self.view.draw_2d_menu()
        elif self.automaton_mode is CellularAutomaton.modes["2D"]:
            self.automaton_mode = CellularAutomaton.modes["1D"]
            self.view.draw_1d_menu()
        self.set_cell_automaton()

    def draw_initial_state_controller(self, btn_instance):
        self.set_cell_automaton()
        self.draw_data_frame()

    def set_state_controller(self, btn_instance):
        pass

    def sub10_rule_controller(self, btn_instance):
        pass

    def add10_rule_controller(self, btn_instance):
        pass

    def sub10_size_controller(self, btn_instance):
        pass

    def add10_size_controller(self, btn_instance):
        pass

    def sub10_iterations_controller(self, btn_instance):
        pass

    def add10_iterations_controller(self, btn_instance):
        pass

    def get_iterations(self):
        return self.automaton_iterations

    def get_size(self):
        return self.automaton_size

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
        self.data_frame = generate_empty_2d_list_of_list(size=self.automaton_iterations)

    def draw_data_frame(self):
        self.view.grid.canvas.clear()
        self.view.draw_data_frame(self.data_frame)
        print(self.data_frame)

    def set_data_frame(self):
        if self.automaton_mode is CellularAutomaton.modes["1D"]:
            for iteration in range(0, self.automaton_iterations):
                self.data_frame[iteration] = self.cell_automaton.get_current_state()
                self.cell_automaton.calculate_next_iteration()
            self.cell_automaton.set_to_initial_state()

        if self.automaton_mode is CellularAutomaton.modes["2D"]:
            self.data_frame = self.cell_automaton.get_current_state()
            self.cell_automaton.calculate_next_iteration()