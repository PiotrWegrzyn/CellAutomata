from functools import partial

from controler.Automaton2DController import Automaton2DController
from model.RuleSets.RecristalizationRuleSet import RecristalizationRuleSet
from model.RuleSets.NucleationRuleSet import NucleationRuleSet
from view.NucleationView import NucleationView


class NucleationController(Automaton2DController):

    rule_set = NucleationRuleSet()

    def __init__(self, app, cell_size=9, cell_offset=1):
        super().__init__(app, cell_size, cell_offset)
        self.pattern_folder = "./patterns/Nucleation/"

    def set_initial_view(self):
        self.set_view(NucleationView(self.modes, self.get_menu_width()))

    def bind_buttons(self):
        super().bind_buttons()
        self.bind_recristalize_button()

    def bind_recristalize_button(self):
        self.app.view.recristalize_button.bind(on_press=partial(self.recristalize_button_controller))

    def recristalize_button_controller(self, btn_instance):
        self.rule_set = RecristalizationRuleSet()
        self.set_cell_automaton(
            rule_set=self.rule_set,
            initial_state=self.cell_automaton.get_current_state()
        )


