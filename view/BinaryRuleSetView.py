import kivy.uix.button as kb
from view.DrawingView import DrawingView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import kivy

kivy.require('1.9.0')


class BinaryRuleSetView(DrawingView):
    def __init__(self, modes, menu_width, cell_size=9, cell_offset=1, **kwargs):
        super().__init__(modes, menu_width, cell_size, cell_offset, **kwargs)

    def _create_elements(self):
        super()._create_elements()
        self.create_draw_button()
        self.create_columns_elements()
        self.create_iterations_elements()
        self.create_rule_elements()
        self.create_alive_cells_elements()

    def show_menu(self):
        super().show_menu()
        self.add_draw_button()
        self.add_columns_elements_to_menu()
        self.add_iterations_elements_to_menu()
        self.add_rule_elements_to_menu()
        self.add_alive_cells_elements_to_menu()

    def add_columns_elements_to_menu(self):
        self.menu.add_widget(self.columns_label)
        self.menu.add_widget(self.columns_btns_containter)

    def add_iterations_elements_to_menu(self):
        self.menu.add_widget(self.iterations_label)
        self.menu.add_widget(self.change_iterations_btns_containter)

    def add_draw_initial_btn_to_menu(self):
        self.draw_btn = kb.Button(
            text="Draw\nInitial",
            size_hint=(1, 0.1),
        )
        self.menu.add_widget(self.draw_btn)

    def create_columns_elements(self):
        self.columns_label = Label(
            text="Columns: ",
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]
        )
        self.columns_btns_containter = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.sub_columns = kb.Button(
            text='-10',
            size_hint=(1, 1),

        )
        self.columns_btns_containter.add_widget(self.sub_columns)
        self.add_columns = kb.Button(
            text='+10',
            size_hint=(1, 1),
        )
        self.columns_btns_containter.add_widget(self.add_columns)

    def create_iterations_elements(self):
        self.iterations_label = Label(
            text="Iterations: ",
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]
        )
        self.change_iterations_btns_containter = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.sub_iterations = kb.Button(
            text='-10',
            size_hint=(1, 1),
        )
        self.change_iterations_btns_containter.add_widget(self.sub_iterations)

        self.add_iterations = kb.Button(
            text='+10',
            size_hint=(1, 1),
        )
        self.change_iterations_btns_containter.add_widget(self.add_iterations)


    def add_rule_elements_to_menu(self):
        self.menu.add_widget(self.rule_label)
        self.menu.add_widget(self.change_rule_btns_containter)

    def create_rule_elements(self):
        self.rule_label = Label(
            text="Rule: ",
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]
        )
        self.change_rule_btns_containter = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )

        self.sub_rule = kb.Button(
            text='-5',
            size_hint=(1, 1),
        )
        self.change_rule_btns_containter.add_widget(self.sub_rule)
        self.add_rule = kb.Button(
            text='+5',
            size_hint=(1, 1),
        )
        self.change_rule_btns_containter.add_widget(self.add_rule)

    def add_alive_cells_elements_to_menu(self):
        self.menu.add_widget(self.alive_cells_label)
        self.menu.add_widget(self.change_alive_cells_btns_containter)

    def create_alive_cells_elements(self):
        self.alive_cells_label = Label(
            text="Alive cells:\n",
            # +"{:.1f}%".format(self.controller.get_alive_cell_percentage()*100)
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1]
        )
        self.change_alive_cells_btns_containter = BoxLayout(
            size_hint=(1, 0.1),
            orientation='horizontal'
        )
        self.sub_alive_cells = kb.Button(
            text='-5%',
            size_hint=(1, 1),
        )
        self.change_alive_cells_btns_containter.add_widget(self.sub_alive_cells)

        self.add_alive_cells = kb.Button(
            text='+5%',
            size_hint=(1, 1),
        )
        self.change_alive_cells_btns_containter.add_widget(self.add_alive_cells)

    def add_draw_button(self):
        self.menu.add_widget(self.draw_btn)

    def create_draw_button(self):
       self.draw_btn = kb.Button(
           text="Draw",
           size_hint=(1, 0.1),
       )


