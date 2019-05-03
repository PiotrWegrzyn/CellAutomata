import sys
from functools import reduce

from kivy.graphics.context_instructions import Color
from kivy.properties import partial


def generate_empty_2d_list_of_list(size):
    main_list = []
    for i in range(0, size):
        child_list = []
        main_list.append(child_list)
    return main_list


class BaseController:
    modes = {}

    def __init__(self, app):
        self.app = app
        self.menu_item_width = 100
        self.set_modes()
        self.setup()
        self.set_initial_view()
        self.bind_buttons()
        self.app.view.grid.on_touch_down = self.on_touch_down

    def set_initial_view(self):
        pass

    def set_view(self, view):
        self.app.set_view(view)

    def change_mode(self, mode):
        self.app.set_controller(mode)

    def draw_menu(self):
        self.app.view.show_menu()

    def bind_change_mode_btn(self):
        self.app.view.change_mode_btn.bind(on_press=partial(self.choose_mode_controller))

    def choose_mode_controller(self, btn_instance):
        self.clear_menu()
        self.draw_choose_mode_menu()

    def bind_change_mode_menu_buttons(self):
        self.bind_back_btn()
        for button in self.app.view.mode_buttons:
            button.bind(on_press=partial(self.change_mode_controller))

    def bind_back_btn(self):
        self.app.view.back_btn.bind(on_press=self.back_btn_controller)

    def change_mode_controller(self, btn_instance):
        self.app.set_controller(btn_instance.text)

    def back_btn_controller(self, btn_instanc):
        self.clear_menu()
        self.draw_menu()

    def draw_choose_mode_menu(self):
        self.app.view.show_choose_mode_menu()

    def clear_canvas(self):
        self.app.view.grid.canvas.clear()

    def clear_grid(self):
        self.app.view.grid.clear_widgets()

    def clear_menu(self):
        self.app.view.clear_menu()

    def get_menu_width(self):
        return self.menu_item_width

    def clicked_on_grid(self, cell_row, cell_index):
        pass

    def on_touch_down(self, touch):
        # todo remove print on release
        print(self.app.view)
        print(touch.y, touch.x)
        pass

    def bind_buttons(self):
        self.bind_change_mode_btn()
        self.bind_change_mode_menu_buttons()

    def setup(self):
        pass

    @staticmethod
    def str_to_class(class_name):
        # return reduce(getattr, str.split("."), sys.modules[__name__])
        return globals()[class_name]

    def set_modes(self):
        self.modes = self.fetch_modes()

    def fetch_modes(self):
        return self.app.get_modes()