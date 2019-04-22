import datetime

from kivy.properties import partial
import kivy.uix.button as kb


class BaseController:
    modes = {}

    def __init__(self, view):
        self.view = view
        self.menu_item_width = view.menu.width
        self.initialize_view()

    def draw_menu(self):
        self.add_change_mode_to_menu()

    def choose_mode_controller(self, btn_instance):
        self.clear_menu()
        self.draw_choose_mode_menu()

    def _change_mode(self, btn_instance):
        self.view.controller = self.modes[btn_instance.text](self.view)

    def add_change_mode_to_menu(self):
        self.change_mode_btn = kb.Button(
            text="Change\nmode",
            size_hint=(1, 0.1),
            on_press=partial(self.choose_mode_controller)
        )
        self.view.menu.add_widget(self.change_mode_btn)


    def back_button_controller(self, btn_instanc):
        self.clear_menu()
        self.draw_menu()

    def initialize_view(self):
        self.clear_canvas()
        self.clear_menu()
        self.draw_menu()
        self.view.grid.on_touch_down = self.on_touch_down

    def draw_choose_mode_menu(self):
        for mode_name in self.modes:
            file_button = kb.Button(
                text=mode_name,
                size_hint=(1, 0.1),
                on_press=partial(self._change_mode)
            )
            self.view.menu.add_widget(file_button)

    def clear_canvas(self):
        self.view.grid.canvas.clear()

    def clear_grid(self):
        self.view.grid.clear_widgets()

    def clear_menu(self):
        self.view.menu.clear_widgets()

    def get_menu_width(self):
        return self.menu_item_width

    def clicked_on_grid(self, cell_row, cell_index):
        pass

    def on_touch_down(self, touch):
        # todo remove print on release
        # print(self._get_graphic_cell_row_from_pos(touch.y), self._get_graphic_cell_column_from_pos(touch.x))
        print(touch.y, touch.x)
        pass
