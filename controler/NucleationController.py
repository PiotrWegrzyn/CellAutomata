from controler.Automaton2DController import Automaton2DController
from model.RuleSets.NucleationRuleSet import NucleationRuleSet
from view.NucleationView import NucleationView


class NucleationController(Automaton2DController):

    rule_set = NucleationRuleSet()

    def __init__(self, app, cell_size=9, cell_offset=1):
        super().__init__(app, cell_size, cell_offset)
        self.pattern_folder = "./patterns/Nucleation/"

    def set_initial_view(self):
        self.set_view(NucleationView(self.modes, self.get_menu_width()))
