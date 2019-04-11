from CellAutomaton import CellularAutomaton
import kivy
from kivy.config import Config
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
kivy.require('1.9.0')

class MyPaintWidget(Widget):
    def __init__(self, ellipse_size,ellipse_offset):
        super(MyPaintWidget, self).__init__()
        Window.size = (1280, 800)
        ellipse_offset = ellipse_offset
        ellipse_size = ellipse_size

        size = int(Window.size[0]/(ellipse_size+ellipse_offset))
        iterations = int(Window.size[1]/(ellipse_size+ellipse_offset))
        rule = 90
        cell_automaton = CellularAutomaton(size, rule, number_of_ones=1)
        cell_automaton.print_rows(iterations)

        with self.canvas:
            Color(1, 0, 0)
            for i in range(0, iterations):
                current_state = cell_automaton.get_current_state()
                for e in range(0, size):
                    if current_state[e] is 1:
                        Ellipse(
                            pos=(
                                e*(ellipse_size+ellipse_offset),
                                Window.size[1]-i*(ellipse_size+ellipse_offset)
                            ),
                            size=(
                                ellipse_size,
                                ellipse_size
                            )
                        )
                cell_automaton.calculate_next()

    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, 1, 0)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


class MyPaintApp(App):
    def build(self):
        return MyPaintWidget(4,1)

