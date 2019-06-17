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

    def create_cell_grid(self, data_frame):
        for cell_row in range(0, len(data_frame)):
            row_instructions = InstructionGroup()
            for cell_col in range(len(data_frame[cell_row])):
                color = create_color(data_frame[cell_row][cell_col])
                cell_instructions = self._create_cell(cell_row, cell_col, color)
                row_instructions.insert(cell_col, cell_instructions)

            self.grid.canvas.insert(cell_row, row_instructions)

    def _create_cell(self, cell_row, cell_col, cell_color):
        cell_instructions = InstructionGroup()
        cell_instructions.add(cell_color)
        rectangle = self._create_cell_graphic(cell_row, cell_col)
        cell_instructions.add(rectangle)
        return cell_instructions

    @timeit
    def draw_data_frame(self, new_data_frame):
        if self.initial or self.has_size_changed(new_data_frame):
            self.grid.canvas.clear()
            self.create_cell_grid(new_data_frame)
            self.initial = False
        else:
            for cell_row in range(len(new_data_frame)):
                for cell_col in range(len(new_data_frame[cell_row])):
                    color = create_color(new_data_frame[cell_row][cell_col])
                    if self.data_frame[cell_row][cell_col] != new_data_frame[cell_row][cell_col]:
                        self._update_cell_color(cell_row,cell_col,color)
        self.data_frame = new_data_frame

    def has_size_changed(self, new_data_frame):
        if len(new_data_frame) is not len(self.data_frame):
            return True
        else:
            for i,column in enumerate(new_data_frame):
                if len(column) is not len(self.data_frame[i]):
                    return True
        return False

    def _update_cell_color(self, cell_row, cell_col, cell_color):
        self.grid.canvas.children[cell_row].children[cell_col].children[0] = cell_color

    def update_cell(self, row, column, color=None):
        color = create_color(color)
        self._update_cell_color(row, column, color)
        self.grid.canvas.ask_update()

    def _create_cell_graphic(self, cell_row, cell_col):
        return Rectangle(
            pos=(
                self._column_to_coord(cell_col),
                self._row_to_coord(cell_row)
            ),
            size=(
                self.cell_size,
                self.cell_size
            )
        )

    def _row_to_coord(self, row):
        return Window.size[1] - ((row + 1) * self.cell_box_size)

    def _column_to_coord(self, column):
        return self.menu_width+(column * self.cell_box_size)

    def _get_graphic_cell_column_from_pos(self, pos_y):
        return int((pos_y-self.menu_width) / self.cell_box_size)

    def _get_graphic_cell_row_from_pos(self, pos_x):
        return int(((Window.size[1]-pos_x)/self.cell_box_size))

