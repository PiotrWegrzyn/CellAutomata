import kivy
import kivy.uix.button as kb
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from view.DrawingView import DrawingView
from view.GameOfLifeView import GameOfLifeView

kivy.require('1.9.0')


class NucleationView(GameOfLifeView):
    def __init__(self, modes, menu_width, cell_size=9, cell_offset=1, **kwargs):
        super().__init__(modes, menu_width, cell_size, cell_offset, **kwargs)

    def _create_elements(self):
        super(DrawingView, self)._create_elements()
        self.create_draw_button()
        self.create_columns_elements()
        self.create_rows_elements()
        self.create_alive_cells_elements()
        self.create_load_file_buttons()
        self.create_load_save_elements()
        self.create_speed_elements()
        self.create_start_stop_elements()
        self.create_clear_button()
        self.create_recrystallize_button()
        self.create_periodic_checkbox()
        self.create_mode_radio_elements()

    def show_menu(self):
        super(DrawingView, self).show_menu()
        self.add_draw_button()
        self.add_start_stop_btns_to_menu()
        self.add_clear_button()
        self.add_load_save_elements()
        self.add_recrystallize_button()
        self.add_speed_elements_to_menu()
        self.add_columns_elements_to_menu()
        self.add_row_elements_to_menu()
        self.add_alive_cells_elements_to_menu()
        self.add_periodic_checkbox()
        self.add_mode_radio_elements()

    def create_load_file_buttons(self):
        self.file_buttons = []
        import os
        for file in os.listdir("patterns\\Nucleation"):
            if file.endswith(".txt"):
                file_button = kb.Button(
                    text=file.__str__(),
                    size_hint=(1, 0.1),
                )
                self.file_buttons.append(file_button)

    def create_recrystallize_button(self):
        self.recrystallize_button= kb.Button(
            text="recrystallize",
            size_hint=(1, 0.1),
        )

    def add_recrystallize_button(self):
        self.menu.add_widget(self.recrystallize_button)

    def create_periodic_checkbox(self):
        self.periodic_label = Label(
            text="Periodic:",
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]
        )
        self.periodic_checkbox = CheckBox(color=[1, 0, 0, 1], size_hint=[1, 0.1], active=True)

    def add_periodic_checkbox(self):
        self.menu.add_widget(self.periodic_label)
        self.menu.add_widget(self.periodic_checkbox)

    def create_mode_radio_elements(self):
        self.mode_radio_continer = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.random_mode = CheckBox(color=[1, 0, 0, 1], size_hint=[0.33, 1], group="mode", active=True)
        self.equal_mode= CheckBox(color=[1, 0, 0, 1], size_hint=[0.33, 1], group="mode")
        self.radius_mode = CheckBox(color=[1, 0, 0, 1], size_hint=[0.33, 1], group="mode")
        self.mode_radio_continer.add_widget(self.random_mode)
        self.mode_radio_continer.add_widget(self.equal_mode)
        self.mode_radio_continer.add_widget(self.radius_mode)

    def add_mode_radio_elements(self):
        self.menu.add_widget(self.mode_radio_continer)

