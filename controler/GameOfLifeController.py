from functools import partial

from controler.Automaton2DController import Automaton2DController
from model.RuleSets.GameOfLifeRuleSet import GameOfLifeRuleSet
from view.GameOfLifeView import GameOfLifeView


class GameOfLifeController(Automaton2DController):

    rule_set = GameOfLifeRuleSet()

    def __init__(self, app, cell_size=9, cell_offset=1):
        super().__init__(app, cell_size, cell_offset)
        self.pattern_folder = "patterns/LifelikeAutomata/"

    def set_initial_view(self):
        self.set_view(GameOfLifeView(self.modes, self.get_menu_width()))

    def bind_buttons(self):
        super().bind_buttons()
        self.bind_rule_input()
        self.bind_reverse_colors_checkbox()

    def bind_rule_input(self):
        self.app.view.rule_input.bind(on_text_validate=partial(self.rule_input_controller))

    def rule_input_controller(self, value):
        self.rule_set = GameOfLifeRuleSet(
            rule_code=value.text,
            reverse_colors=self.rule_set.reverse_colors
        )
        self.set_cell_automaton(
            rule_set=self.rule_set,
            initial_state=self.cell_automaton.get_current_state()
        )
        self.clear_canvas()

    def bind_reverse_colors(self):
        self.app.view.rule_input.bind(on_text_validate=partial(self.rule_input_controller))

    def bind_reverse_colors_checkbox(self):
        self.app.view.reverse_colors_checkbox.bind(active=partial(self.on_checkbox_active))

    def on_checkbox_active(self, checkbox, value):
        self.rule_set = GameOfLifeRuleSet(
            rule_code=self.rule_set.rule_code,
            reverse_colors=value
        )
        self.set_cell_automaton(
            rule_set=self.rule_set,
            initial_state=self.cell_automaton.get_current_state()
        )
