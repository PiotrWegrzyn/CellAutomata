from functools import partial

import kivy.uix.button as kb

from model.RuleSets.GameOfLifeRuleSet import GameOfLifeRuleSet
from view.DrawingView import DrawingView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import kivy

kivy.require('1.9.0')


class GameOfLifeView(DrawingView):
    def __init__(self, modes, menu_width, cell_size=9, cell_offset=1, **kwargs):
        super().__init__(modes, menu_width, cell_size, cell_offset, **kwargs)

    def _create_elements(self):
        super()._create_elements()
        self.create_draw_button()
        self.create_columns_elements()
        self.create_rows_elements()
        self.create_alive_cells_elements()
        self.create_file_buttons()
        self.create_load_btn()
        self.create_save_btn()
        self.create_speed_elements()
        self.create_start_stop_elements()

    def show_menu(self):
        super().show_menu()
        self.add_draw_button()
        self.add_start_stop_btns_to_menu()
        self.add_speed_elements_to_menu()
        self.add_columns_elements_to_menu()
        self.add_row_elements_to_menu()
        self.add_alive_cells_elements_to_menu()
        self.add_save_current_state_btn()
        self.add_load_state_from_file()

    def add_columns_elements_to_menu(self):
        self.menu.add_widget(self.columns_label)
        self.menu.add_widget(self.columns_btns_containter)

    def add_row_elements_to_menu(self):
        self.menu.add_widget(self.rows_label)
        self.menu.add_widget(self.change_rows_btns_containter)

    def add_draw_initial_btn_to_menu(self):
        self.draw_btn = kb.Button(
            text="Draw\nInitial",
            size_hint=(1, 0.1),
        )
        self.menu.add_widget(self.draw_btn)

    def create_columns_elements(self):
        self.columns_label = Label(
            text="Columns: ",
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]
        )
        self.columns_btns_containter = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.sub_columns = kb.Button(
            text='-10',
            size_hint=(1, 1),

        )
        self.columns_btns_containter.add_widget(self.sub_columns)
        self.add_columns = kb.Button(
            text='+10',
            size_hint=(1, 1),
        )
        self.columns_btns_containter.add_widget(self.add_columns)

    def create_rows_elements(self):
        self.rows_label = Label(
            text="Rows: ",
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]
        )
        self.change_rows_btns_containter = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.sub_rows = kb.Button(
            text='-10',
            size_hint=(1, 1),
        )
        self.change_rows_btns_containter.add_widget(self.sub_rows)

        self.add_rows = kb.Button(
            text='+10',
            size_hint=(1, 1),
        )
        self.change_rows_btns_containter.add_widget(self.add_rows)

    def add_alive_cells_elements_to_menu(self):
        self.menu.add_widget(self.alive_cells_label)
        self.menu.add_widget(self.change_alive_cells_btns_containter)

    def create_alive_cells_elements(self):
        self.alive_cells_label = Label(
            text="Alive cells:\n",
            # +"{:.1f}%".format(self.controller.get_alive_cell_percentage()*100)
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]
        )
        self.change_alive_cells_btns_containter = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.sub_alive_cells = kb.Button(
            text='-5%',
            size_hint=(1, 1),
        )
        self.change_alive_cells_btns_containter.add_widget(self.sub_alive_cells)

        self.add_alive_cells = kb.Button(
            text='+5%',
            size_hint=(1, 1),
        )
        self.change_alive_cells_btns_containter.add_widget(self.add_alive_cells)

    def add_draw_button(self):
        self.menu.add_widget(self.draw_btn)

    def create_draw_button(self):
        self.draw_btn = kb.Button(
            text="Draw",
            size_hint=(1, 0.1),
        )

    def show_choose_file_menu(self):
        self.clear_menu()
        self.add_back_btn_to_menu()
        self.add_file_buttons()

    def create_file_buttons(self):
        self.file_buttons = []
        import os
        for file in os.listdir("patterns"):
            if file.endswith(".txt"):
                print(os.path.join("/patterns", file))
                file_button = kb.Button(
                    text=file.__str__(),
                    size_hint=(1, 0.1),
                )
                self.file_buttons.append(file_button)

    # on_press = partial(self.controller.load_state_from_file_controller)

    def add_file_buttons(self):
        for button in self.file_buttons:
            self.menu.add_widget(button)

    def create_start_stop_elements(self):
        self.play_stop_btns_containter = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.play_btn = kb.Button(
            text='Play',
            size_hint=(1, 1),
            # on_press=partial(self.controller.play_iterations_controller)
        )
        self.play_stop_btns_containter.add_widget(self.play_btn)

        self.stop_btn = kb.Button(
            text='Stop',
            size_hint=(1, 1),
            # on_press=partial(self.controller.stop_iterations_controller)
        )
        self.play_stop_btns_containter.add_widget(self.stop_btn)


    def add_start_stop_btns_to_menu(self):
        self.menu.add_widget(self.play_stop_btns_containter)

    def create_speed_elements(self):
        self.speed_label = Label(
            text="Speed: ", #+ self.controller.get_iteration_speed().__str__() + "fps",
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]
        )
        self.faster_slower_btns_containter = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.slower_btn = kb.Button(
            text='x0.5',
            size_hint=(1, 1),
            # on_press=partial(self.controller.slower_iterations_controller)
        )
        self.faster_slower_btns_containter.add_widget(self.slower_btn)

        self.faster_btn = kb.Button(
            text='x2',
            size_hint=(1, 1),
            # on_press=partial(self.controller.faster_iterations_controller)
        )
        self.faster_slower_btns_containter.add_widget(self.faster_btn)

    def add_speed_elements_to_menu(self):
        self.menu.add_widget(self.speed_label)
        self.menu.add_widget(self.faster_slower_btns_containter)

    def create_save_btn(self):
        self.save_btn = kb.Button(
            text="Save\nstate",
            size_hint=(1, 0.1),
            # on_press=partial(self.controller.save_current_state_controller)
        )

    def add_save_current_state_btn(self):
        self.menu.add_widget(self.save_btn)

    def create_load_btn(self):
        self.load_btn = kb.Button(
            text="Load\nstate",
            size_hint=(1, 0.1)
        )

    def add_load_state_from_file(self):
        self.menu.add_widget(self.load_btn)



# on_press = partial(self.controller.back_btn_controller)




