from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics.instructions import InstructionGroup

from settings import BACKGROUND_COLOR
from time_measure.timeit_decorator import timeit
from view.BaseView import BaseView


def create_color(rgb):
    return Color(rgb[0], rgb[1], rgb[2])


class DrawingView(BaseView):
    def __init__(self, modes, menu_width, cell_size=9, cell_offset=1, **kwargs):
        super().__init__(modes, menu_width, **kwargs)
        self.cell_offset = cell_offset
        self.cell_size = cell_size
        self.cell_box_size = cell_offset+cell_size
        self.data_frame = [[]]
        self.initial = True

    def update_cell_size(self, size):
        self.cell_size = size

    def update_cell_offset(self, size):
        self.cell_offset = size

    @timeit
    def draw_data_frame(self, data_frame):
        self.data_frame = data_frame
        if self.initial:
            self.create_cell_grid(data_frame)
            self.initial = False
        else:
            for cell_row in range(0, len(data_frame)):
                for cell_col in range(len(data_frame[0])):
                    # if self.data_frame != data_frame[cell_row][cell_col]:
                    self.grid.canvas.children[cell_row][cell_col].insert(0,create_color(data_frame[cell_row][cell_col]))

    # self.data_frame = data_frame
        # for cell_row in range(0, len(data_frame)):
        #     self._draw_graphic_columns(cell_row)

    def create_cell_grid(self,data_frame):
        for cell_row in range(0, len(data_frame)):
            row_instructions = InstructionGroup()
            for cell_col in range(len(data_frame[0])):
                cell_instructions = InstructionGroup()
                cell_instructions.add(create_color(data_frame[cell_row][cell_col]))
                rectangle = Rectangle(
                    pos=(
                        self._get_graphic_cell_x_pos(cell_col),
                        self._get_graphic_cell_y_pos(cell_row)
                    ),

                    size=(
                        self.cell_size,
                        self.cell_size
                    )
                )
                cell_instructions.add(rectangle)
                row_instructions.insert(cell_col,cell_instructions)
            self.grid.canvas.insert(cell_row,row_instructions)

    def _draw_graphic_columns(self, row):
        for column in range(0, len(self.data_frame[row])):
            cell_color = self.data_frame[row][column]
            if not cell_color == BACKGROUND_COLOR:
                self._draw_cell(row, column, cell_color)

    def _draw_cell(self, row, column, cell_color):
        color = create_color(cell_color)
        self.grid.canvas.add(color)
        rectangle = Rectangle(
            pos=(
                self._get_graphic_cell_x_pos(column),
                self._get_graphic_cell_y_pos(row)
            ),

            size=(
                self.cell_size,
                self.cell_size
            )
        )
        self.grid.canvas.add(rectangle)

    def update_cell(self, row, column, color=None):
        self._draw_cell(row, column, color)

    def _get_graphic_cell_y_pos(self, row):
        return Window.size[1] - ((row + 1) * self.cell_box_size)

    def _get_graphic_cell_x_pos(self, column):
        return self.menu_width+(column * self.cell_box_size)

    def _get_graphic_cell_column_from_pos(self, pos_y):
        return int((pos_y-self.menu_width) / self.cell_box_size)

    def _get_graphic_cell_row_from_pos(self, pos_x):
        return int(((Window.size[1]-pos_x)/self.cell_box_size))

