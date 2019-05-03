import copy
from functools import partial

from controler.Automaton2DController import Automaton2DController
from model.RuleSets.NucleationRuleSet import NucleationRuleSet
from model.RuleSets.RecrystallizationRuleSet import RecrystallizationRuleSet
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
        self.bind_recrystallize_button()

    def bind_recrystallize_button(self):
        self.app.view.recrystallize_button.bind(on_press=partial(self.recrystallize_button_controller))

    def recrystallize_button_controller(self, btn_instance):
        self.change_rule_set_to_recrystallization()

    def draw_next_iteration(self):
        old_df = copy.deepcopy(self.data_frame)
        if isinstance(self.cell_automaton.rule_set, RecrystallizationRuleSet):
            self.cell_automaton.rule_set.next_iteration()
        super().draw_next_iteration()
        if old_df == self.data_frame:
            if isinstance(self.cell_automaton.rule_set, RecrystallizationRuleSet):
                self.stop_iterations()
            if isinstance(self.cell_automaton.rule_set, NucleationRuleSet):
                self.change_rule_set_to_recrystallization()

    def change_rule_set_to_recrystallization(self):
        self.rule_set = RecrystallizationRuleSet(self.cell_automaton.get_current_state())
        self.set_cell_automaton(
            rule_set=self.rule_set,
            initial_state=self.cell_automaton.get_current_state()
        )


