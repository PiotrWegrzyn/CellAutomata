from functools import partial
from kivy.properties import partial
from kivy.uix.label import Label

import kivy.uix.button as kb
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from view.BaseView import BaseView
from view.DrawingView import DrawingView


class BinaryRuleSetView(DrawingView):
    def __init__(self,modes, menu_width, columns_count, iterations, cell_size=9, cell_offset=1, **kwargs):
        super().__init__(modes,menu_width, cell_size, cell_offset, **kwargs)
        self.columns_count = columns_count
        self.add_columns_count_btns_and_label_to_menu()
        print("lol")

    def add_columns_count_btns_and_label_to_menu(self):
        self.columns_count_label = Label(
            text="Columns: " + self.columns_count.__str__(),
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]
        )
        self.menu.add_widget(self.columns_count_label)

        self.change_columns_count_btns_containter = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.menu.add_widget(self.change_columns_count_btns_containter)

        self.sub10columns_count = kb.Button(
            text='-10',
            size_hint=(1, 1),
        )
        self.change_columns_count_btns_containter.add_widget(self.sub10columns_count)

        self.add10columns_count = kb.Button(
            text='+10',
            size_hint=(1, 1),
        )
        self.change_columns_count_btns_containter.add_widget(self.add10columns_count)

    def add_iterations_btns_and_label_to_menu(self):
        self.iterations_label = Label(
            text="Iterations: ",
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
        )
        self.change_iterations_btns_containter.add_widget(self.sub10iterations)

        self.add10iterations = kb.Button(
            text='+10',
            size_hint=(1, 1),
        )
        self.change_iterations_btns_containter.add_widget(self.add10iterations)

    def add_draw_initial_btn_to_menu(self):
        self.draw_btn = kb.Button(
            text="Draw\nInitial",
            size_hint=(1, 0.1),
        )
        self.menu.add_widget(self.draw_btn)
