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


