import kivy
import kivy.uix.button as kb
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
kivy.require('1.9.0')

Builder.load_file('view/menu.kv')

class Menu(BoxLayout):
    color = ListProperty()


class BaseView(BoxLayout):
    def __init__(self, modes, menu_width, **kwargs):
        super().__init__(**kwargs)
        self.menu_width = menu_width
        self.modes = modes
        self.menu = Menu(size_hint=(None, 1), width=menu_width, orientation='vertical')
        self.menu.color = [1, 1, 1, 1]
        self.add_widget(self.menu)

        self.grid = Widget()
        self.add_widget(self.grid)
        self._create_elements()
        self.show_menu()

    def clear_menu(self):
        self.menu.clear_widgets()

    def show_menu(self):
        self.add_select_mode_to_menu()

    def add_select_mode_to_menu(self):
        self.menu.add_widget(self.change_mode_btn)

    def show_choose_mode_menu(self):
        self.clear_menu()
        self.add_back_btn_to_menu()
        self.add_mode_buttons_to_menu()

    def add_back_btn_to_menu(self):
        self.menu.add_widget(self.back_btn)

    def add_mode_buttons_to_menu(self):
        for button in self.mode_buttons:
            self.menu.add_widget(button)

    def _create_elements(self):
        self._create_menu()
        self.create_back_btn()
        self.create_choose_mode_menu()

    def _create_menu(self):
        self.change_mode_btn = kb.Button(
            text="Change\nmode",
            size_hint=(1, 0.1),
        )

    def create_choose_mode_menu(self):
        self.mode_buttons = []
        for mode_name in self.modes:
            mode_button = kb.Button(
                text=mode_name,
                size_hint=(1, 0.1),
            )
            self.mode_buttons.append(mode_button)

    def create_back_btn(self):
        self.back_btn = kb.Button(
            text="Back",
            size_hint=(1, 0.1),
        )


