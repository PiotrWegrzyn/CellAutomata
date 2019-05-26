import kivy
import kivy.uix.button as kb
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.widget import WidgetException

from view.DrawingView import DrawingView
from view.GameOfLifeView import GameOfLifeView

kivy.require('1.9.0')


class NucleationView(GameOfLifeView):
    def __init__(self, modes, menu_width, cell_size=9, cell_offset=1, **kwargs):
        super().__init__(modes, menu_width, cell_size, cell_offset, **kwargs)
        self.show_nucleation_menu()

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
        self.create_neighbourhood_elements()
        self.create_radius_elements()
        self.create_monte_carlo_elements()
        self.create_show_energy_items()
        self.create_total_energy_label()
        self.create_kt_input()
        self.create_iterations_elements()
        self.create_nucleation_elements()

    def show_menu(self):
        super(DrawingView, self).show_menu()
        self.add_draw_button()
        self.add_start_stop_btns_to_menu()
        self.add_clear_button()
        self.add_neighbourhood_elements()
        self.add_speed_elements_to_menu()
        self.add_columns_elements_to_menu()
        self.add_row_elements_to_menu()
        self.add_alive_cells_elements_to_menu()
        self.add_periodic_checkbox()
        self.add_show_energy_items()
        self.add_total_energy()
        self.add_mode_radio_elements()
        self.add_radius_elements()
        self.add_nucleation_elements()
        self.add_monte_carlo_button()
        self.add_recrystallize_button()

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
            text="Recrystallize",
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
        self.random_mode_continer = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.random_mode_label = Label(
            text="Random:",
            size_hint=(0.7, 1),
            color=[1, 0, 0, 1]
        )
        self.random_mode = CheckBox(color=[1, 0, 0, 1], size_hint=[0.3, 1], group="mode", active=True)
        self.random_mode_continer.add_widget(self.random_mode_label)
        self.random_mode_continer.add_widget(self.random_mode)

        self.equal_mode_continer = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.equal_mode_label = Label(
            text="Equal:",
            size_hint=(0.7, 1),
            color=[1, 0, 0, 1]
        )
        self.equal_mode = CheckBox(color=[1, 0, 0, 1], size_hint=[0.3, 1], group="mode")
        self.equal_mode_continer.add_widget(self.equal_mode_label)
        self.equal_mode_continer.add_widget(self.equal_mode)

        self.radius_mode_continer = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.radius_mode_label = Label(
            text="Radius:",
            size_hint=(0.7, 1),
            color=[1, 0, 0, 1]
        )
        self.radius_mode = CheckBox(color=[1, 0, 0, 1], size_hint=[0.3, 1], group="mode")
        self.radius_mode_continer.add_widget(self.radius_mode_label)
        self.radius_mode_continer.add_widget(self.radius_mode)

    def add_mode_radio_elements(self):
        self.menu.add_widget(self.random_mode_continer)
        self.menu.add_widget(self.equal_mode_continer)
        self.menu.add_widget(self.radius_mode_continer)

    def create_neighbourhood_elements(self):
        self.neighbourhood_select = Spinner(
            text_autoupdate=True,
            values=("Moore", 'VonNeumann', 'Pentagonal', 'HexagonalLeft', 'HexagonalRight', 'HexagonalRandom', 'Radius'),
            size_hint=(1, 0.1),
            pos_hint={'center_x': .5, 'center_y': .5})

    def add_neighbourhood_elements(self):
        self.menu.add_widget(self.neighbourhood_select)

    def create_radius_elements(self):
        self.radius_label = Label(
            text="Radius:",
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]
        )
        self.change_radius_btns_containter = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.sub_radius = kb.Button(
            text='-1',
            size_hint=(1, 1),
        )
        self.change_radius_btns_containter.add_widget(self.sub_radius)

        self.add_radius = kb.Button(
            text='+1',
            size_hint=(1, 1),
        )
        self.change_radius_btns_containter.add_widget(self.add_radius)

    def add_radius_elements(self):
        self.menu.add_widget(self.radius_label)
        self.menu.add_widget(self.change_radius_btns_containter)

    def create_monte_carlo_elements(self):
        self.monte_carlo_button = kb.Button(
            text="Monte Carlo",
            size_hint=(1, 0.1),
        )

    def create_nucleation_elements(self):
        self.nucleation_button = kb.Button(
            text="Nucleation",
            size_hint=(1, 0.1),
        )

    def add_nucleation_elements(self):
        self.menu.add_widget(self.nucleation_button)

    def add_monte_carlo_button(self):
        self.menu.add_widget(self.monte_carlo_button)

    def create_show_energy_items(self):
        self.show_energy_label = Label(
            text="Show Energy: ",
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]
        )
        self.show_energy_checkbox = CheckBox(color=[1, 0, 0, 1], size_hint=[1, 0.1])

    def add_show_energy_items(self):
        self.menu.add_widget(self.show_energy_label)
        self.menu.add_widget(self.show_energy_checkbox)

    def create_kt_input(self):
        self.kt_label = Label(
            text="kt constant: ",
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]
        )
        self.kt_input = TextInput(text="1", size_hint=[1, 0.1], multiline=False)

    def add_kt_input(self):
        self.menu.add_widget(self.kt_label)
        self.menu.add_widget(self.kt_input)

    def create_total_energy_label(self):
        self.total_energy_label = Label(
            text="Total energy: 0",
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]
        )

    def add_total_energy(self):
        self.menu.add_widget(self.total_energy_label)

    def show_nucleation_menu(self):
        self.reset_menu()
        self.menu.remove_widget(self.nucleation_button)

    def show_monte_carlo_menu(self):
        self.reset_menu()
        try:
            self.add_kt_input()
            self.add_iterations_elements()
            self.menu.remove_widget(self.monte_carlo_button)
        except WidgetException:
            print("Widget Exception")

    def show_recristallization_menu(self):
        self.reset_menu()
        self.menu.remove_widget(self.recrystallize_button)

    def reset_menu(self):
        self.menu.clear_widgets()
        self.show_menu()

    def create_iterations_elements(self):
        self.iterations_label = Label(
            text="Iterations:",
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]
        )
        self.iterations_input = TextInput(text="100", size_hint=[1, 0.1], multiline=False)

    def add_iterations_elements(self):
        self.menu.add_widget(self.iterations_label)
        self.menu.add_widget(self.iterations_input)

