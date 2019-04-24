from contextlib import closing
from multiprocessing.pool import ThreadPool

from kivy.core.window import Window
from kivy.properties import partial
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

from kivy.uix.label import Label

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
import kivy.uix.button as kb
from view.BaseView import BaseView


def create_color(color):
    rgb = color.rgb
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
        threads = int(len(data_frame)+1)
        with closing(ThreadPool(threads)) as pool:
            parameters_list = [cell_row for cell_row in range(0, len(data_frame))]
            pool.map(self._draw_graphic_columns, parameters_list)

    def _draw_graphic_columns(self, row):
        for column in range(0, len(self.data_frame[row])):
            if self.data_frame[row][column].is_alive():
                color = create_color(self.data_frame[row][column].get_color())
                self._draw_cell(row, column, color)

    def _draw_cell(self, row, column, color=None):
        if color:
            self.grid.canvas.add(color)
        else:
            self.grid.canvas.add(Color(1, 1, 1))
        ellipse = Rectangle(
            pos=(
                self._get_graphic_cell_x_pos(column),
                self._get_graphic_cell_y_pos(row)
            ),

            size=(
                self.cell_size,
                self.cell_size
            )
        )
        self.grid.canvas.add(ellipse)

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
