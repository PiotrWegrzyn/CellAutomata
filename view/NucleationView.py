from functools import partial

import kivy.uix.button as kb

from model.RuleSets.GameOfLifeRuleSet import GameOfLifeRuleSet
from view.DrawingView import DrawingView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import kivy

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
        self.create_load_btn()
        self.create_save_btn()
        self.create_speed_elements()
        self.create_start_stop_elements()
        self.create_reverse_colors_items()
        self.create_clear_button()

    def show_menu(self):
        super(DrawingView, self).show_menu()
        self.add_clear_button()
        self.add_draw_button()
        self.add_start_stop_btns_to_menu()
        self.add_speed_elements_to_menu()
        self.add_columns_elements_to_menu()
        self.add_row_elements_to_menu()
        self.add_alive_cells_elements_to_menu()
        self.add_save_current_state_btn()
        self.add_load_state_from_file()
        self.add_reverse_colors_items()

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

