import pyglet
import numpy as np

class Grid:
    def __init__(self, width, height, rows, cols):
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.cells = np.
    def draw(self):
        for cell in self.cells:
            cell.draw()