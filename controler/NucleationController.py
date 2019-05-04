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
        previous_data_frame = copy.deepcopy(self.data_frame)
        super().draw_next_iteration()
        if previous_data_frame == self.data_frame:
            self.handle_no_change_in_data_frame()

    def change_rule_set_to_recrystallization(self):
        self.rule_set = RecrystallizationRuleSet(self.cell_automaton.get_current_state())
        self.set_cell_automaton(
            rule_set=self.rule_set,
            initial_state=self.cell_automaton.get_current_state()
        )

    def change_rule_set_to_nucleation(self):
        self.rule_set = NucleationRuleSet()
        self.set_cell_automaton(
            rule_set=self.rule_set,
            initial_state=self.cell_automaton.get_current_state()
        )

    def handle_no_change_in_data_frame(self):
        if isinstance(self.cell_automaton.rule_set, RecrystallizationRuleSet):
            self.stop_iterations()
        if isinstance(self.cell_automaton.rule_set, NucleationRuleSet):
            self.change_rule_set_to_recrystallization()



