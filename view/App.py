from kivy.core.window import Window
from kivy.properties import partial
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

from kivy.uix.label import Label

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
import kivy.uix.button as kb
from controler.MainController import MainController
from view.BaseView import BaseView
from view.DrawingView import DrawingView
kivy.require('1.9.0')


class CellAutomatonApp(App):
    def __init__(self):
        super(CellAutomatonApp, self).__init__()
        Window.clearcolor = (1, 1, 1, 1)
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
