from kivy.core.window import Window
from kivy.properties import partial
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

from kivy.uix.label import Label

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
import kivy.uix.button as kb
from controler.ViewController import ViewController
kivy.require('1.9.0')


class CellAutomatonApp(App):
    def __init__(self):
        super(CellAutomatonApp, self).__init__()
        self.controller = ViewController(self, 9, 1, window_width=800, window_height=700)
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (800, 700)
        self.cell_size = self.controller.cell_size
        self.column_width= self.controller.cell_box_size
        self.row_height = self.controller.cell_box_size

    def build(self):
        self.grid = Widget()

        self.menu = BoxLayout(size_hint=(None, 1), width=self.controller.get_menu_width(), orientation='vertical')
        self.draw_2d_menu()

        self.root = BoxLayout(orientation='horizontal')
        self.root.add_widget(self.menu)
        self.root.add_widget(self.grid)

        return self.root

    def draw_2d_menu(self):
        self.add_change_mode_to_menu()
        self.add_start_stop_btns_to_menu()
        self.add_speed_btns_and_label_to_menu()
        self.add_next_iteration_btn_to_menu()
        self.add_set_state_btn_to_menu()
        self.add_alive_cells_btns_and_label_to_menu()
        self.add_empty_space_to_menu(0.2)

    def draw_1d_menu(self):
        self.add_change_mode_to_menu()
        self.add_draw_initial_btn_to_menu()
        self.add_set_state_btn_to_menu()
        self.add_rule_btns_and_label_to_menu()
        self.add_size_btns_and_label_to_menu()
        self.add_alive_cells_btns_and_label_to_menu()
        self.add_iterations_btns_and_label_to_menu()

    def add_start_stop_btns_to_menu(self):
        self.play_stop_btns_containter = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.menu.add_widget(self.play_stop_btns_containter)
        self.play_btn = kb.Button(
            text='Play',
            size_hint=(1, 1),
            on_press=partial(self.controller.play_iterations_controller)
        )
        self.play_stop_btns_containter.add_widget(self.play_btn)

        self.stop_btn = kb.Button(
            text='Stop',
            size_hint=(1, 1),
            on_press=partial(self.controller.stop_iterations_controller)
        )
        self.play_stop_btns_containter.add_widget(self.stop_btn)

    def add_speed_btns_and_label_to_menu(self):
        self.speed_label = Label(
            text="Speed: " + self.controller.get_iteration_speed().__str__(),
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]

        )
        self.menu.add_widget(self.speed_label)

        self.faster_slower_btns_containter = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.menu.add_widget(self.faster_slower_btns_containter)

        self.slower_btn = kb.Button(
            text='x0.5',
            size_hint=(1, 1),
            on_press=partial(self.controller.slower_iterations_controller)
        )
        self.faster_slower_btns_containter.add_widget(self.slower_btn)

        self.faster_btn = kb.Button(
            text='x2',
            size_hint=(1, 1),
            on_press=partial(self.controller.faster_iterations_controller)
        )
        self.faster_slower_btns_containter.add_widget(self.faster_btn)

    def add_next_iteration_btn_to_menu(self):
        next_iteration_btn = kb.Button(
            text="Next\niteration",
            size_hint=(1, 0.1),
            on_press=partial(self.controller.draw_next_iteration_controller)
        )
        self.menu.add_widget(next_iteration_btn)

    def add_empty_space_to_menu(self, size):
        self.empty_menu_space = BoxLayout(
            size_hint=(1, size),
            orientation='vertical'
        )
        self.menu.add_widget(self.empty_menu_space)

    def add_change_mode_to_menu(self):
        self.change_mode_btn = kb.Button(
            text="Change\nmode",
            size_hint=(1, 0.1),
            on_press=partial(self.controller.change_mode_controller)
        )
        self.menu.add_widget(self.change_mode_btn)

    def add_draw_initial_btn_to_menu(self):
        self.draw_btn = kb.Button(
            text="Draw\nInitial",
            size_hint=(1, 0.1),
            on_press=partial(self.controller.draw_initial_state_controller)
        )
        self.menu.add_widget(self.draw_btn)

    def add_set_state_btn_to_menu(self):
        self.set_state_btn = kb.Button(
            text="Set\nstate",
            size_hint=(1, 0.1),
            on_press=partial(self.controller.set_state_controller)
        )
        self.menu.add_widget(self.set_state_btn)

    def add_rule_btns_and_label_to_menu(self):
        self.rule_label = Label(
            text="Rule: " + self.controller.get_rule().__str__(),
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]

        )
        self.menu.add_widget(self.rule_label)

        self.change_rule_btns_containter = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.menu.add_widget(self.change_rule_btns_containter)

        self.sub10rule = kb.Button(
            text='-10',
            size_hint=(1, 1),
            on_press=partial(self.controller.sub10_rule_controller)
        )
        self.change_rule_btns_containter.add_widget(self.sub10rule)

        self.add10rule = kb.Button(
            text='+10',
            size_hint=(1, 1),
            on_press=partial(self.controller.add10_rule_controller)
        )
        self.change_rule_btns_containter.add_widget(self.add10rule)

    def add_size_btns_and_label_to_menu(self):
        self.size_label = Label(
            text="Size: " + self.controller.get_size().__str__(),
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]

        )
        self.menu.add_widget(self.size_label)

        self.change_size_btns_containter = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.menu.add_widget(self.change_size_btns_containter)

        self.sub10size = kb.Button(
            text='-10',
            size_hint=(1, 1),
            on_press=partial(self.controller.sub10_size_controller)
        )
        self.change_size_btns_containter.add_widget(self.sub10size)

        self.add10size = kb.Button(
            text='+10',
            size_hint=(1, 1),
            on_press=partial(self.controller.add10_size_controller)
        )
        self.change_size_btns_containter.add_widget(self.add10size)

    def add_iterations_btns_and_label_to_menu(self):
        self.iterations_label = Label(
            text="Iterations: " + self.controller.get_iterations().__str__(),
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]

        )
        self.menu.add_widget(self.iterations_label)

        self.change_iterations_btns_containter = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.menu.add_widget(self.change_iterations_btns_containter)

        self.sub10iterations = kb.Button(
            text='-10',
            size_hint=(1, 1),
            on_press=partial(self.controller.sub10_iterations_controller)
        )
        self.change_iterations_btns_containter.add_widget(self.sub10iterations)

        self.add10iterations = kb.Button(
            text='+10',
            size_hint=(1, 1),
            on_press=partial(self.controller.add10_iterations_controller)
        )
        self.change_iterations_btns_containter.add_widget(self.add10iterations)

    def add_alive_cells_btns_and_label_to_menu(self):
        self.alive_cells_label = Label(
            text="Alive cells:\n"+"{:.1f}%".format(self.controller.get_alive_cell_percentage()*100),
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]
        )
        self.menu.add_widget(self.alive_cells_label)

        self.change_alive_cells_btns_containter = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.menu.add_widget(self.change_alive_cells_btns_containter)

        self.sub_01_alive_cells = kb.Button(
            text='-10',
            size_hint=(1, 1),
            on_press=partial(self.controller.sub01_alive_cells_controller)
        )
        self.change_alive_cells_btns_containter.add_widget(self.sub_01_alive_cells)

        self.add_01_alive_cells = kb.Button(
            text='+10',
            size_hint=(1, 1),
            on_press=partial(self.controller.add01_alive_cells_controller)
        )
        self.change_alive_cells_btns_containter.add_widget(self.add_01_alive_cells)

    def clear_menu(self):
        self.menu.clear_widgets()

    def draw_data_frame(self, data_frame):
        self.grid.canvas.add(Color(1, 0, 0))
        for row in range(0, len(data_frame)):
            self._draw_graphic_columns(row, data_frame)

    def _draw_graphic_columns(self, row, data_frame):
        for column in range(0, len(data_frame[row])):
            if data_frame[row][column] is 1:
                self._draw_graphic_cell(row, column)

    def _draw_graphic_cell(self, row, column):
        ellipse = Rectangle(
            pos=(
                self._get_graphic_cell_x_pos(column),
                self._get_graphic_cell_y_pos(row)
            ),
            size=(
                self.cell_size,
                self.cell_size
            )
        )
        self.grid.canvas.add(ellipse)

    def _get_graphic_cell_y_pos(self, row):
        return Window.size[1] - (row + 1) * self.row_height

    def _get_graphic_cell_x_pos(self, column):
        return self.controller.get_menu_width()+column * self.column_width