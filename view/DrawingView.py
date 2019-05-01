from contextlib import closing
from multiprocessing.pool import ThreadPool

from kivy.core.window import Window
from kivy.graphics import Rectangle

from kivy.graphics import Color
from view.BaseView import BaseView


def create_color(rgb):
    return Color(rgb[0], rgb[1], rgb[2])


class DrawingView(BaseView):
    def __init__(self, modes, menu_width, cell_size=9, cell_offset=1, **kwargs):
        super().__init__(modes, menu_width, **kwargs)
        self.cell_offset = cell_offset
        self.cell_size = cell_size
        self.cell_box_size = cell_offset+cell_size

    def update_cell_size(self, size):
        self.cell_size = size

    def update_cell_offset(self, size):
        self.cell_offset = size

    def draw_data_frame(self, data_frame):
        self.data_frame = data_frame
        # threads = int(len(data_frame)+1)
        # with closing(ThreadPool(threads)) as pool:
        #     parameters_list = [cell_row for cell_row in range(0, len(data_frame))]
        #     pool.map(self._draw_graphic_columns, parameters_list)
        for cell_row in range(0, len(data_frame)):
            self._draw_graphic_columns(cell_row)

    def _draw_graphic_columns(self, row):
        for column in range(0, len(self.data_frame[row])):
            cell_color = self.data_frame[row][column]
            if not cell_color == [1, 1, 1]:     # [1,1,1] is white
                color = create_color(cell_color)
                self._draw_cell(row, column, color)

    def _draw_cell(self, row, column, color):
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

