import datetime

from kivy.properties import partial
import kivy.uix.button as kb


def generate_empty_2d_list_of_list(size):
    return [[] for i in range(0, size)]


class BaseController:
    modes = {}

    def __init__(self, app):
        self.app = app
        self.menu_item_width = 100
        self.setup()
        self.set_initial_view()
        self.bind_buttons()
        self.app.view.grid.on_touch_down = self.on_touch_down

    def set_initial_view(self):
        pass

    def set_view(self, view):
        self.app.set_view(view)

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
            button.bind(on_press=partial(self._change_mode))

    def bind_back_btn(self):
        self.app.view.back_btn.bind(on_press=self.back_btn_controller)

    def _change_mode(self, btn_instance):
        self.app.controller = self.modes[btn_instance.text](self.app)

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
        # print(self._get_graphic_cell_row_from_pos(touch.y), self._get_graphic_cell_column_from_pos(touch.x))
        print(self.app.view)
        print(touch.y, touch.x)
        pass

    def bind_buttons(self):
        self.bind_change_mode_btn()
        self.bind_change_mode_menu_buttons()

    def setup(self):
        pass


