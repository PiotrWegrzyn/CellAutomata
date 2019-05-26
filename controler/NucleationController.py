import copy
from functools import partial

from controler.Automaton2DController import Automaton2DController
from model.RuleSets.MonteCarloRuleSet import MonteCarloRuleSet
from model.RuleSets.NucleationRuleSet import NucleationRuleSet
from model.RuleSets.RecrystallizationRuleSet import RecrystallizationRuleSet
from time_measure.timeit_decorator import timeit
from view.NucleationView import NucleationView


class NucleationController(Automaton2DController):

    rule_set = NucleationRuleSet()

    def __init__(self, app, cell_size=9, cell_offset=1):
        self.iterations = 0
        super().__init__(app, cell_size, cell_offset)
        self.pattern_folder = "./patterns/Nucleation/"
        self.app.view.sub_alive_cells.text = "-1%"
        self.app.view.add_alive_cells.text = "+1%"

    def update_labels(self):
        super().update_labels()
        self.update_radius_label()
        self.update_total_energy_label()
        self.update_iterations_label()

    def set_initial_view(self):
        self.set_view(NucleationView(self.modes, self.get_menu_width()))

    def bind_buttons(self):
        super().bind_buttons()
        self.bind_recrystallize_button()
        self.bind_periodic_checkbox()
        self.bind_mode_checkboxes()
        self.bind_add_radius()
        self.bind_sub_radius()
        self.bind_monte_carlo_button()
        self.bind_show_energy_checkbox()
        self.bind_kt_input()
        self.bind_iteration_input()
        self.bind_nucleation_button()
        self.bind_initialize_button()
        self.bind_initialize_back_button_button()

    def bind_recrystallize_button(self):
        self.app.view.recrystallize_button.bind(on_press=partial(self.recrystallize_button_controller))

    def bind_periodic_checkbox(self):
        self.app.view.periodic_checkbox.bind(active=partial(self.toggle_periodic_controller))

    def bind_add_radius(self):
        self.app.view.add_radius.bind(on_press=partial(self.add_radius_controller))

    def bind_sub_radius(self):
        self.app.view.sub_radius.bind(on_press=partial(self.sub_radius_controller))

    def bind_monte_carlo_button(self):
        self.app.view.monte_carlo_button.bind(on_press=partial(self.start_monte_carlo_controller))

    def bind_mode_checkboxes(self):
        self.app.view.random_mode.bind(active=partial(self.random_mode_controller))
        self.app.view.equal_mode.bind(active=partial(self.equal_mode_controller))
        self.app.view.radius_mode.bind(active=partial(self.radius_mode_controller))

    def set_data_frame_to_current_colors(self):
        new_state = self.cell_automaton.get_current_state()
        self.data_frame = \
            [[cell.get_color_representation(self.rule_set.color_indicator) for cell in new_state[row]] for row in
             range(0, self.cell_automaton.get_rows())]

    @timeit
    def draw_next_iteration(self):
        print("__new__iteration__")
        if isinstance(self.rule_set, MonteCarloRuleSet):
            if self.iterations <= 0:
                self.stop_iterations()
                return
        previous_data_frame = copy.deepcopy(self.data_frame)
        super().draw_next_iteration()
        if isinstance(self.rule_set, MonteCarloRuleSet):
            self.iterations -=1
            self.update_iterations_label()
        if previous_data_frame == self.data_frame:
            self.handle_no_change_in_data_frame()
        self.update_total_energy_label()

    def handle_no_change_in_data_frame(self):
        if self.cell_automaton.get_percent_of_alive_cells() > 0:
            if isinstance(self.cell_automaton.rule_set, RecrystallizationRuleSet):
                self.stop_iterations()

            if isinstance(self.cell_automaton.rule_set, NucleationRuleSet):
                self.change_rule_set_to_monte_carlo()

    def bind_nucleation_button(self):
        self.app.view.nucleation_button.bind(on_press=partial(self.nucleation_button_controller))

    def nucleation_button_controller(self, instance):
        self.change_rule_set_to_nucleation()

    def recrystallize_button_controller(self, btn_instance):
        self.change_rule_set_to_recrystallization()

    def change_rule_set_to_recrystallization(self):
        self.rule_set = RecrystallizationRuleSet(
            current_state=self.cell_automaton.get_current_state(),
            initial_mode=self.rule_set.initial_mode,
            is_periodic=self.rule_set.is_periodic,
            neighbourhood_type=self.rule_set.neighbourhood_type,
            radius=self.rule_set.radius,
            color_indicator=self.rule_set.color_indicator
        )
        self.set_cell_automaton(
            rule_set=self.rule_set,
            initial_state=self.cell_automaton.get_current_state()
        )
        self.app.view.show_recristallization_menu()

    def change_rule_set_to_monte_carlo(self):
        self.rule_set = MonteCarloRuleSet(
            initial_mode=self.rule_set.initial_mode,
            is_periodic=self.rule_set.is_periodic,
            neighbourhood_type=self.rule_set.neighbourhood_type,
            radius=self.rule_set.radius,
            kt_constant=self.get_kt_constant(),
            color_indicator=self.rule_set.color_indicator
        )
        self.set_cell_automaton(
            rule_set=self.rule_set,
            initial_state=self.cell_automaton.get_current_state()
        )
        self.app.view.show_monte_carlo_menu()

    def change_rule_set_to_nucleation(self):
        self.rule_set = NucleationRuleSet(
            initial_mode=self.rule_set.initial_mode,
            is_periodic=self.rule_set.is_periodic,
            neighbourhood_type=self.rule_set.neighbourhood_type,
            radius=self.rule_set.radius,
            color_indicator=self.rule_set.color_indicator
        )
        self.set_cell_automaton(
            rule_set=self.rule_set,
            initial_state=self.cell_automaton.get_current_state()
        )
        self.app.view.show_nucleation_menu()


    def clear_state_controller(self, instance):
        super(NucleationController, self).clear_state_controller(instance)
        self.change_rule_set_to_nucleation()

    def toggle_periodic_controller(self, checkbox, value):
        self.rule_set.is_periodic = not self.rule_set.is_periodic
        self.set_cell_automaton(
            rule_set=self.rule_set,
            initial_state=self.cell_automaton.get_current_state()
        )
        self.draw_current_state()

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

    def add_radius_controller(self, instance):
        if self.rule_set.radius + 1 <= 10:
            self.rule_set.radius += 1
            self.update_radius_label()
        else:
            print("Ain't nobody got calcualtiontime for dat.")

    def sub_radius_controller(self, instance):
        if self.rule_set.radius - 1 > 0:
            self.rule_set.radius -= 1
            self.update_radius_label()

    def update_radius_label(self):
        self.app.view.radius_label.text = "Radius: " + self.rule_set.radius.__str__()

    def get_kt_constant(self):
        try:
            return self.rule_set.kt_constant
        except AttributeError:
            return 1

    def start_monte_carlo_controller(self, instance):
        self.change_rule_set_to_monte_carlo()

    def bind_kt_input(self):
        self.app.view.kt_input.bind(on_text_validate=partial(self.kt_input_controller))

    def kt_input_controller(self, input):
        try:
            self.rule_set.change_kt_constant(float(input.text))
        except ValueError or TypeError:
            print("Wrong input. Should be int or float.")
        except AttributeError:
            print("Wrong Rule Set")

    def bind_show_energy_checkbox(self):
        self.app.view.show_energy_checkbox.bind(active=partial(self.show_energy_controller))

    def show_energy_controller(self, checkbox, value):
        if value:
            self.set_show_energy_mode()
        else:
            self.set_show_grain_mode()

    def set_show_energy_mode(self):
        self.rule_set.color_indicator = 'energy'
        self.set_cell_automaton(
            rule_set=self.rule_set,
            initial_state=self.cell_automaton.get_current_state()
        )
        self.draw_current_state()

    def set_show_grain_mode(self):
        self.rule_set.color_indicator = 'grain_id'
        self.set_cell_automaton(
            rule_set=self.rule_set,
            initial_state=self.cell_automaton.get_current_state()
        )
        self.draw_current_state()

    def update_total_energy_label(self):
        self.app.view.total_energy_label.text = "Total energy: " + self.get_total_energy().__str__()

    def get_total_energy(self):
        return self.rule_set.get_total_energy()

    def bind_iteration_input(self):
        self.app.view.iterations_input.bind(on_text_validate=partial(self.iterations_input_controller))

    def iterations_input_controller(self, text_input):
        try:
            self.add_iterations(int(text_input.text))
        except ValueError:
            print("Not an int.")

    def add_iterations(self, iterations):
        self.iterations += iterations
        self.update_iterations_label()
        # self.restart_auto_iterations_clock()

    def update_iterations_label(self):
        self.app.view.iterations_label.text = "Iterations: " + self.iterations.__str__()

    def bind_initialize_button(self):
        self.app.view.initialize_button.bind(on_press=partial(self.initialize_button_controller))

    def initialize_button_controller(self, instance):
        self.app.view.show_initialize_menu()

    def bind_initialize_back_button_button(self):
        self.app.view.initialize_back_button.bind(on_press=partial(self.initialize_back_button_controller))

    def initialize_back_button_controller(self, instance):
        if isinstance(self.rule_set, NucleationRuleSet):
            self.app.view.show_nucleation_menu()
        if isinstance(self.rule_set, MonteCarloRuleSet):
            self.app.view.show_monte_carlo_menu()
        if isinstance(self.rule_set, RecrystallizationRuleSet):
            self.app.view.show_recristallization_menu()

