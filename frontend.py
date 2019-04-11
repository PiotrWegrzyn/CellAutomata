from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line

from CellAutomaton import CellularAutomaton


class MyPaintWidget(Widget):

    def __init__(self):
        super(MyPaintWidget, self).__init__()
        size = 50
        cell_automaton = CellularAutomaton(size, 30, number_of_ones=1)
        iterations = 100
        cell_automaton.print_rows(iterations)

        elipse_size=5
        elipse_offset=1
        with self.canvas:
            Color(1, 0, 0)
            for i in range(0, iterations):
                current_state = cell_automaton.get_current_state()
                for e in range(0, size):
                    if current_state[e] is 1:
                        Ellipse(pos=(e*(elipse_size+elipse_offset),(elipse_size+elipse_offset)*i), size=(elipse_size, elipse_size))
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
        return MyPaintWidget()

