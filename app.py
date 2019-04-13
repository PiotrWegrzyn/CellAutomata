import random
import threading
from multiprocessing.pool import ThreadPool

from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from CellAutomaton import CellularAutomaton,generate_empty_2d_list_of_list
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
import kivy.uix.button as kb
from kivy.core.window import Window
kivy.require('1.9.0')


class CellAutomatonWidget(Widget):
    def __init__(self, ellipse_size, ellipse_offset, window_width=640, window_height=400, rule=90):
        super(CellAutomatonWidget, self).__init__()
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (window_width, window_height)

        self.automaton_mode = 2
        self.rule = rule

        self.menu_item_width = 100
        self.menu_item_height = 50

        self.ellipse_offset = ellipse_offset
        self.ellipse_size = ellipse_size
        self.ellipse_box_size = self.ellipse_size + self.ellipse_offset

        self.current_canvas_graphic_items = []
        self.auto_iterations = None

        self.max_graphic_columns = int((Window.size[0] - self.menu_item_width) / self.ellipse_box_size)
        self.max_graphic_rows = int(Window.size[1] / self.ellipse_box_size)
        self.data_frame = generate_empty_2d_list_of_list(size=self.max_graphic_rows)

        self.iterations = int(Window.size[1]/self.ellipse_box_size)

        self.cell_automaton = None
        self.set_cell_automon()
        self.set_initial_display()

    def set_initial_display(self):
        self._draw_initial_menu()
        self.create_graphics()

    def draw_graphics(self):
        self._draw_graphic_rows()

    def _draw_graphic_rows(self):
        self.canvas.add(Color(1, 0, 0))
        pool = ThreadPool(int(len(self.data_frame)/10))
        pool.map(self._draw_graphic_columns, [col for col in range(0, len(self.data_frame))])
        pool.close()

    def _draw_graphic_columns(self, row):
        for column in range(0, len(self.data_frame[row])):
            if self.data_frame[row][column] is 1:
                self._draw_graphic_cell(row, column)

    def _draw_graphic_cell(self, row, column):
        ellipse = Ellipse(
            pos=(
                self._get_graphic_cell_x_pos(column),
                self._get_graphic_cell_y_pos(row)
            ),
            size=(
                self.ellipse_size,
                self.ellipse_size
            )
        )
        self.canvas.add(ellipse)
        self.current_canvas_graphic_items.append(ellipse)

    def get_menu_item_pos_y(self, position):
        return Window.size[1]-(self.menu_item_height*position)

    def _get_graphic_cell_y_pos(self, row):
        return Window.size[1] - (row + 1) * self.ellipse_box_size

    def _get_graphic_cell_x_pos(self, column):
        return self.menu_item_width + column * self.ellipse_box_size

    def clear_graphic(self):
        for item in self.current_canvas_graphic_items:
            self.canvas.remove(item)
        self.current_canvas_graphic_items = []

    def create_graphics(self):
        self.clear_graphic()
        self.fetch_data_frame()
        self.draw_graphics()


    def _draw_menu(self):
        if self.automaton_mode is CellularAutomaton.modes["1D"]:
            self.draw_1d_menu()
        if self.automaton_mode is CellularAutomaton.modes["2D"]:
            self.draw_2d_menu()

    def _reset_data_frame(self):
        self.data_frame = generate_empty_2d_list_of_list(size=self.iterations)

    def fetch_data_frame(self):
        if self.automaton_mode is CellularAutomaton.modes["1D"]:
            for iteration in range(0, self.iterations):
                self.data_frame[iteration] = self.cell_automaton.get_current_state()
                self.cell_automaton.calculate_next_iteration()
            self.cell_automaton.set_initial_state()

        if self.automaton_mode is CellularAutomaton.modes["2D"]:
            self.data_frame=self.cell_automaton.get_current_state()
            self.cell_automaton.calculate_next_iteration()

    def draw_mode_menu(self):
        change_mode_btn = kb.Button(
            text="Change\nMode",
            pos=(0, self.get_menu_item_pos_y(2)),
            size=(self.menu_item_width, self.menu_item_height * 2)
        )
        change_mode_btn.bind(on_press=self._change_mode_controller)
        self.add_widget(change_mode_btn)

    def draw_1d_menu(self):
        draw_btn = kb.Button(
            text="Draw",
            pos=(0, self.get_menu_item_pos_y(4)),
            size=(self.menu_item_width, self.menu_item_height * 2)
        )
        draw_btn.bind(on_press=self._draw_graphic_controller)
        self.add_widget(draw_btn)

        rule_sub10_btn = kb.Button(
            text="Rule\n-10",
            pos=(0, self.get_menu_item_pos_y(6)),
            size=(int(self.menu_item_width / 2), self.menu_item_height * 2)
        )
        rule_sub10_btn.bind(on_press=self._sub_10_rule_and_draw_controller)
        self.add_widget(rule_sub10_btn)

        rule_plus10_btn = kb.Button(
            text="Rule\n+10",
            pos=(int(self.menu_item_width / 2), self.get_menu_item_pos_y(6)),
            size=(int(self.menu_item_width / 2), self.menu_item_height * 2)
        )
        rule_plus10_btn.bind(on_press=self._add_10_rule_and_draw_controller)
        self.add_widget(rule_plus10_btn)

        self.rule_label = Label(
            text="Rule: " + self.cell_automaton.rule.__str__(),
            pos=(0, self.get_menu_item_pos_y(7)),
            size=(self.menu_item_width, self.menu_item_height)
        )
        self.rule_label.color = [1, 0, 0, 1]
        self.add_widget(self.rule_label)

        rule_input = TextInput(
            pos=(0, self.get_menu_item_pos_y(8)),
            size=(self.menu_item_width, self.menu_item_height)
        )
        rule_input.bind(text=self.rule_text_input_controller)
        self.add_widget(rule_input)

        self.size_label = Label(
            text="Size: " + self.cell_automaton.size.__str__(),
            pos=(0, self.get_menu_item_pos_y(9)),
            size=(self.menu_item_width, self.menu_item_height)
        )
        self.size_label.color = [1, 0, 0, 1]
        self.add_widget(self.size_label)

        size_input = TextInput(
            pos=(0, self.get_menu_item_pos_y(10)),
            size=(self.menu_item_width, self.menu_item_height)
        )
        size_input.bind(text=self.size_text_input_controller)
        self.add_widget(size_input)

        self.iterations_label = Label(
            text="Iterations: " + self.iterations.__str__(),
            pos=(0, self.get_menu_item_pos_y(11)),
            size=(self.menu_item_width, self.menu_item_height)
        )
        self.iterations_label.color = [1, 0, 0, 1]
        self.add_widget(self.iterations_label)

        iterations_input = TextInput(
            pos=(0, self.get_menu_item_pos_y(12)),
            size=(self.menu_item_width, self.menu_item_height)
        )
        iterations_input.bind(text=self.iterations_text_input_controller)
        self.add_widget(iterations_input)

        self.percentage_of_ones_label = Label(
            text="Alive cells: " + int(self.cell_automaton.percentage_of_ones*100).__str__()+"%",
            pos=(0, self.get_menu_item_pos_y(13)),
            size=(self.menu_item_width, self.menu_item_height)
        )
        self.percentage_of_ones_label.color = [1, 0, 0, 1]
        self.add_widget(self.percentage_of_ones_label)

        percentage_of_ones_input = TextInput(
            pos=(0, self.get_menu_item_pos_y(14)),
            size=(self.menu_item_width, self.menu_item_height)
        )
        percentage_of_ones_input.bind(text=self._percentage_of_ones_input_controller)
        self.add_widget(percentage_of_ones_input)

    def draw_2d_menu(self):
        play_btn = kb.Button(
            text='Play',
            pos=(0, self.get_menu_item_pos_y(4)),
            size=(int(self.menu_item_width / 2), self.menu_item_height * 2)
        )
        play_btn.bind(on_press=self._play_iterations_controller)
        self.add_widget(play_btn)

        stop_btn = kb.Button(
            text='Stop',
            pos=(int(self.menu_item_width / 2), self.get_menu_item_pos_y(4)),
            size=(int(self.menu_item_width / 2), self.menu_item_height * 2)
        )
        stop_btn.bind(on_press=self._stop_iterations_controller)
        self.add_widget(stop_btn)

        next_iteration_btn = kb.Button(
            text="Next\niteration",
            pos=(0, self.get_menu_item_pos_y(6)),
            size=(self.menu_item_width, self.menu_item_height * 2)
        )
        next_iteration_btn.bind(on_press=self._draw_next_iteration_controller)
        self.add_widget(next_iteration_btn)

    def _draw_initial_menu(self):
        self.draw_mode_menu()
        self._draw_menu()

    def stop_iterations(self):
        try:
            self.auto_iterations.cancel()
        except AttributeError:
            pass

    def set_cell_automon(self):
        try:
            current_alive_percentage = self.cell_automaton.percentage_of_ones
        except AttributeError:
            current_alive_percentage = 0.2

        if self.automaton_mode is CellularAutomaton.modes["1D"]:
            self.cell_automaton = CellularAutomaton(
                mode=self.automaton_mode,
                size=self.max_graphic_columns,
                rule=self.rule,
                percentage_of_ones=current_alive_percentage
            )

        if self.automaton_mode is CellularAutomaton.modes["2D"]:
            self.cell_automaton = CellularAutomaton(
                mode=self.automaton_mode,
                size=self.max_graphic_rows,
                percentage_of_ones=current_alive_percentage
            )

    # todo move all controllers to a different class
    def _draw_graphic_controller(self, instance):
        self.create_graphics()

    def _add_10_rule_and_draw_controller(self, instance):
        self.cell_automaton.set_rule((self.cell_automaton.rule+10) % 255)
        self.rule_label.text = "Rule: " + self.cell_automaton.rule.__str__()
        self.create_graphics()

    def _sub_10_rule_and_draw_controller(self, instance):
        self.cell_automaton.set_rule((self.cell_automaton.rule-10) % 255)
        self.rule_label.text = "Rule: " + self.cell_automaton.rule.__str__()
        self.create_graphics()

    def _draw_next_iteration_controller(self, instance):
        self.cell_automaton.calculate_next_iteration()
        self.create_graphics()

    def _play_iterations_controller(self, instance):
        self.create_graphics()
        self.stop_iterations()
        self.auto_iterations = Clock.schedule_interval(self._draw_next_iteration_controller, 0.02)

    def _stop_iterations_controller(self, instance):
        self.stop_iterations()

    def _change_mode_controller(self, instance):
        self.stop_iterations()
        self.canvas.clear()
        self.current_canvas_graphic_items=[]

        if self.automaton_mode is CellularAutomaton.modes["1D"]:
            self.automaton_mode = CellularAutomaton.modes["2D"]
        elif self.automaton_mode is CellularAutomaton.modes["2D"]:
            self.automaton_mode = CellularAutomaton.modes["1D"]

        self.set_cell_automon()
        self._draw_initial_menu()

    def size_text_input_controller(self, instance, value):
        if value is not "":
            try:
                if int(value) > 1:
                    self.cell_automaton.size = int(value)
                    self.cell_automaton.set_initial_state()
                    self.size_label.text = "Size: " + self.cell_automaton.size.__str__()
            except ValueError:
                self.size_label.text = "Size:\nOnly positive\nintegers."

    def iterations_text_input_controller(self, instance, value):
        if value is not "":
            try:
                if int(value) > 1:
                    self.iterations = int(value)
                    self.cell_automaton.set_initial_state()
                    self.iterations_label.text = "Iterations: " + self.iterations.__str__()
            except ValueError:
                self.iterations_label.text = "Iterations:\nOnly positive\nintegers."

    def rule_text_input_controller(self, instance, value):
        if value is not "":
            try:
                if 1 < int(value) < 255:
                    self.cell_automaton.set_rule(int(value))
                    self.cell_automaton.set_initial_state()
                    self.rule_label.text = "Rule: " + self.cell_automaton.rule.__str__()
            except ValueError:
                self.rule_label.text = "Rule:\nOnly positive\nintegers."

    def _percentage_of_ones_input_controller(self, instance, value):
        if value is not "":
            try:
                if 0 < int(value) < 100:
                    self.cell_automaton.set_percent_of_ones(float(int(value)/100))
                    self.percentage_of_ones_label.text = "Alive cells: " + float(self.cell_automaton.percentage_of_ones*100).__str__()+"%"
            except ValueError:
                self.rule_label.text = "Rule:\nOnly positive\nintegers."


class CellAutomatonApp(App):
    def build(self):
        return CellAutomatonWidget(9, 1, window_width=800, window_height=700)

