import random

from kivy.uix.label import Label

from controler.BaseController import BaseController

from view.BaseView import BaseView


class MainController(BaseController):

    def __init__(self, app):
        super().__init__(app)
        self.app.view.grid.on_touch_down = self.on_touch_down

    def set_initial_view(self):
        self.set_view(BaseView(self.modes, self.get_menu_width()))

