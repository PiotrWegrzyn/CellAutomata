def add_start_stop_btns_to_menu(self):
    self.play_stop_btns_containter = BoxLayout(
        size_hint=(1, 0.1),
        orientation='horizontal'
    )
    self.menu.add_widget(self.play_stop_btns_containter)
    self.play_btn = kb.Button(
        text='Play',
        size_hint=(1, 1),
        on_press=partial(self.controller.play_iterations_controller)
    )
    self.play_stop_btns_containter.add_widget(self.play_btn)

    self.stop_btn = kb.Button(
        text='Stop',
        size_hint=(1, 1),
        on_press=partial(self.controller.stop_iterations_controller)
    )
    self.play_stop_btns_containter.add_widget(self.stop_btn)


def add_speed_btns_and_label_to_menu(self):
    self.speed_label = Label(
        text="Speed: " + self.controller.get_iteration_speed().__str__() + "fps",
        size_hint=(1, 0.1),
        color=[1, 0, 0, 1]

    )
    self.menu.add_widget(self.speed_label)

    self.faster_slower_btns_containter = BoxLayout(
        size_hint=(1, 0.1),
        orientation='horizontal'
    )
    self.menu.add_widget(self.faster_slower_btns_containter)

    self.slower_btn = kb.Button(
        text='x0.5',
        size_hint=(1, 1),
        on_press=partial(self.controller.slower_iterations_controller)
    )
    self.faster_slower_btns_containter.add_widget(self.slower_btn)

    self.faster_btn = kb.Button(
        text='x2',
        size_hint=(1, 1),
        on_press=partial(self.controller.faster_iterations_controller)
    )
    self.faster_slower_btns_containter.add_widget(self.faster_btn)


def add_one_iteration_btn_to_menu(self):
    one_iteration_btn = kb.Button(
        text="One\niteration",
        size_hint=(1, 0.1),
        on_press=partial(self.controller.draw_one_iteration_controller)
    )
    self.menu.add_widget(one_iteration_btn)


def add_empty_space_to_menu(self, size):
    self.empty_menu_space = BoxLayout(
        size_hint=(1, size),
        orientation='vertical'
    )
    self.menu.add_widget(self.empty_menu_space)


def add_change_mode_to_menu(self):
    self.change_mode_btn = kb.Button(
        text="Change\nmode",
        size_hint=(1, 0.1),
        on_press=partial(self.controller.choose_mode_controller)
    )
    self.menu.add_widget(self.change_mode_btn)


def add_draw_initial_btn_to_menu(self):
    self.draw_btn = kb.Button(
        text="Draw\nInitial",
        size_hint=(1, 0.1),
        on_press=partial(self.controller.draw_initial_state_controller)
    )
    self.menu.add_widget(self.draw_btn)


def add_set_state_btn_to_menu(self):
    self.set_state_btn = kb.Button(
        text="Set\nstate",
        size_hint=(1, 0.1),
        on_press=partial(self.controller.set_state_controller)
    )
    self.menu.add_widget(self.set_state_btn)


def add_rule_set_btns_and_label_to_menu(self):
    self.rule_set_label = Label(
        text="Rule Set: " + self.controller.get_rule_set().__str__(),
        size_hint=(1, 0.1),
        color=[1, 0, 0, 1]
    )
    self.menu.add_widget(self.rule_set_label)

    self.change_rule_set_btns_containter = BoxLayout(
        size_hint=(1, 0.1),
        orientation='horizontal'
    )
    self.menu.add_widget(self.change_rule_set_btns_containter)

    self.sub_rule_set = kb.Button(
        text='-10',
        size_hint=(1, 1),
        on_press=partial(self.controller.sub_rule_set_controller)
    )
    self.change_rule_set_btns_containter.add_widget(self.sub_rule_set)

    self.add_rule_set = kb.Button(
        text='+10',
        size_hint=(1, 1),
        on_press=partial(self.controller.add_rule_set_controller)
    )
    self.change_rule_set_btns_containter.add_widget(self.add_rule_set)


def add_rows_count_btns_and_label_to_menu(self):
    self.rows_count_label = Label(
        text="Rows: " + self.controller.get_rows_count().__str__(),
        size_hint=(1, 0.1),
        color=[1, 0, 0, 1]
    )
    self.menu.add_widget(self.rows_count_label)

    self.change_rows_count_btns_containter = BoxLayout(
        size_hint=(1, 0.1),
        orientation='horizontal'
    )
    self.menu.add_widget(self.change_rows_count_btns_containter)

    self.sub_rows_count = kb.Button(
        text='-10',
        size_hint=(1, 1),
        on_press=partial(self.controller.sub_rows_count_controller)
    )
    self.change_rows_count_btns_containter.add_widget(self.sub_rows_count)

    self.add_rows_count = kb.Button(
        text='+10',
        size_hint=(1, 1),
        on_press=partial(self.controller.add_rows_count_controller)
    )
    self.change_rows_count_btns_containter.add_widget(self.add_rows_count)


def add_alive_cells_btns_and_label_to_menu(self):
    self.alive_cells_label = Label(
        text="Alive cells:\n" + "{:.1f}%".format(self.controller.get_alive_cell_percentage() * 100),
        size_hint=(1, 0.1),
        color=[1, 0, 0, 1]
    )
    self.menu.add_widget(self.alive_cells_label)

    self.change_alive_cells_btns_containter = BoxLayout(
        size_hint=(1, 0.1),
        orientation='horizontal'
    )
    self.menu.add_widget(self.change_alive_cells_btns_containter)

    self.sub_5p_alive_cells = kb.Button(
        text='-5%',
        size_hint=(1, 1),
        on_press=partial(self.controller.sub_p_alive_cells_controller)
    )
    self.change_alive_cells_btns_containter.add_widget(self.sub_5p_alive_cells)

    self.add_5p_alive_cells = kb.Button(
        text='+5%',
        size_hint=(1, 1),
        on_press=partial(self.controller.add_p_alive_cells_controller)
    )
    self.change_alive_cells_btns_containter.add_widget(self.add_5p_alive_cells)


def add_save_current_state_btn(self):
    self.save_current_state = kb.Button(
        text="Save\nstate",
        size_hint=(1, 0.1),
        on_press=partial(self.controller.save_current_state_controller)
    )
    self.menu.add_widget(self.save_current_state)


def add_load_state_from_file(self):
    self.load_state_btn = kb.Button(
        text="Load\nstate",
        size_hint=(1, 0.1),
        on_press=partial(self.controller.show_load_file_menu_controller)
    )
    self.menu.add_widget(self.load_state_btn)


def add_back_button(self):
    self.back_button = kb.Button(
        text="Back",
        size_hint=(1, 0.1),
        on_press=partial(self.controller.back_button_controller)
    )
    self.menu.add_widget(self.back_button)


def add_file_buttons(self):
    import os
    for file in os.listdir("patterns"):
        if file.endswith(".txt"):
            print(os.path.join("/patterns", file))
            file_button = kb.Button(
                text=file.__str__(),
                size_hint=(1, 0.1),
                on_press=partial(self.controller.load_state_from_file_controller)
            )
            self.menu.add_widget(file_button)