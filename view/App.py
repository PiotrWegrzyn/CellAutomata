from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
import kivy
from kivy.app import App
from controler.BinaryRuleSetController import BinaryRuleSetController
from controler.NucleationController import NucleationController
from controler.GameOfLifeController import GameOfLifeController
from controler.MainController import MainController

from view.BaseView import BaseView

kivy.require('1.9.0')


class CellAutomatonApp(App):
    modes = {
        "Main Menu": "MainController",
        "Binary Rule": "BinaryRuleSetController",
        "Game of Life": "GameOfLifeController",
        "Nucleation": "NucleationController"
    }

    def __init__(self):
        super(CellAutomatonApp, self).__init__()
        Window.clearcolor = (0.2, 0.2, 0.2, 1)
        Window.size = (1000, 700)

    def build(self):
        self.root = BoxLayout()
        self.view = BaseView(MainController.modes, 100)
        self.set_view(self.view)
        self.controller = MainController(self)

        return self.root

    def set_view(self, view):
        self.view = view
        self.root.clear_widgets()
        self.root.add_widget(view)

    def set_controller(self, mode):
        self.controller = eval(self.modes[mode])(self)

    def get_modes(self):
        return self.modes



