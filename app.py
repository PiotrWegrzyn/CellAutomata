from kivy.graphics.instructions import InstructionGroup
import random
from CellAutomaton import CellularAutomaton
import kivy
from kivy.config import Config
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
import kivy.uix.button as kb
kivy.require('1.9.0')


class CellAutomatonWidget(Widget):
    def __init__(self, ellipse_size, ellipse_offset, window_width=640, window_height=400, rule=90,):
        super(CellAutomatonWidget, self).__init__()
        Window.size = (window_width, window_height)
        self.ellipse_offset = ellipse_offset
        self.ellipse_size = ellipse_size
        self.ellipse_box_size = self.ellipse_size + self.ellipse_offset
        self.current_canvas_graphic_items = []
        self.graphic_columns = int(Window.size[0]/self.ellipse_box_size)
        self.graphic_rows = int(Window.size[1]/self.ellipse_box_size)

        self.cell_automaton = CellularAutomaton(size=self.graphic_columns, rule=rule, number_of_ones=1)

        self.set_initial_display()

    def create_graphic(self):
        self.canvas.add(Color(random.choice([0, 1]), random.choice([0, 1]), random.choice([0, 1])))
        self._draw_graphic_rows()

    def set_initial_display(self):
        btn1 = kb.Button(text="Random Rule")
        btn1.bind(on_press=self._draw_graphic_controller)
        self.add_widget(btn1)

    def _draw_graphic_controller(self, instance):
        self.clear_graphic()
        self.create_graphic()
        self.cell_automaton.set_initial_state()
        self.cell_automaton.set_rule((30+self.cell_automaton.rule) % 250)

    def _draw_graphic_rows(self):
        for row in range(0, self.graphic_rows):
            self._draw_graphic_columns(row)
            self.cell_automaton.calculate_next_iteration()

    def _draw_graphic_columns(self, row):
        current_state = self.cell_automaton.get_current_state()
        for column in range(0, self.graphic_columns):
            if current_state[column] is 1:
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

    def _get_graphic_cell_y_pos(self, row):
        return Window.size[1] - (row + 1) * self.ellipse_box_size

    def _get_graphic_cell_x_pos(self, column):
        return column * self.ellipse_box_size

    def clear_graphic(self):
        for item in self.current_canvas_graphic_items:
            self.canvas.remove(item)
        self.current_canvas_graphic_items = []


class CellAutomatonApp(App):
    def build(self):
        return CellAutomatonWidget(4, 1, window_width=1000, window_height=600)

