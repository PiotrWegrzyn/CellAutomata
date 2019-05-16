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
        self.app.view.sub_alive_cells.text = "-1%"
        self.app.view.add_alive_cells.text = "+1%"

    def set_initial_view(self):
        self.set_view(NucleationView(self.modes, self.get_menu_width()))

    def bind_buttons(self):
        super().bind_buttons()
        self.bind_recrystallize_button()
        self.bind_periodic_checkbox()
        self.bind_mode_checkboxes()

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
        self.rule_set = NucleationRuleSet(self.rule_set.initial_mode, self.rule_set.is_periodic)
        self.set_cell_automaton(
            rule_set=self.rule_set,
            initial_state=self.cell_automaton.get_current_state()
        )

    def handle_no_change_in_data_frame(self):
        if self.cell_automaton.get_percent_of_alive_cells() > 0:
            if isinstance(self.cell_automaton.rule_set, RecrystallizationRuleSet):
                self.stop_iterations()
            if isinstance(self.cell_automaton.rule_set, NucleationRuleSet):
                self.change_rule_set_to_recrystallization()

    def clear_state_controller(self, instance):
        super(NucleationController, self).clear_state_controller(instance)
        self.change_rule_set_to_nucleation()

    def bind_periodic_checkbox(self):
        self.app.view.periodic_checkbox.bind(active=partial(self.toggle_periodic_controller))

    def toggle_periodic_controller(self, checkbox, value):
        self.rule_set.is_periodic = not self.rule_set.is_periodic
        self.set_cell_automaton(
            rule_set=self.rule_set
        )
        self.draw_current_state()

    def bind_mode_checkboxes(self):
        self.app.view.random_mode.bind(active=partial(self.random_mode_controller))
        self.app.view.equal_mode.bind(active=partial(self.equal_mode_controller))
        self.app.view.radius_mode.bind(active=partial(self.radius_mode_controller))

    def random_mode_controller(self, instance, value):
        if value is True:
            self.change_rule_set_initial_mode("random")

    def equal_mode_controller(self, instance, value):
        if value is True:
            self.change_rule_set_initial_mode("equal_spread")

    def radius_mode_controller(self, instance, value):
        if value is True:
            self.change_rule_set_initial_mode("radius")

    def change_rule_set_initial_mode(self, mode):
        self.rule_set.initial_mode = mode
        self.set_cell_automaton(
            rule_set=self.rule_set
        )
        self.draw_current_state()
        self.update_alive_cells_label()

    def sub_alive_cells_controller(self, button_instance):
        delta = -0.01
        current_value = self.cell_automaton.get_percent_of_alive_cells()
        if current_value + delta > 0:
            self.cell_automaton.change_alive_cells_percentage(current_value + delta)
            self.update_alive_cells_label()
            self.draw_current_state()

    def add_alive_cells_controller(self, button_instance):
        delta = 0.01
        current_value = self.cell_automaton.get_percent_of_alive_cells()
        if current_value + delta <= 1:
            self.cell_automaton.change_alive_cells_percentage(current_value + delta)
            self.update_alive_cells_label()
            self.draw_current_state()