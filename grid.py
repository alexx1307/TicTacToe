import pyglet
import numpy as np

colors = {'empty':(30,30,30),
          'player0':(255,0,0), 
          'player1':(0,255,0), #(0,0,255),(255,255,0), (255,0,255), (0,255,255),
          'apple':  (255,255,255)}

class Cell(pyglet.shapes.Rectangle):
    def __init__(self, position, width, height, row, col):
        super().__init__(x=position[0],
                         y=position[1], width=width, height=height)
        # self.cellWidth = width
        # self.cellHeight = height
        self.row = row
        self.col = col
        self.type = 'empty'

    def draw(self):
        # self.prepareToDraw()
        self.color = colors[self.type]
        super().draw()

    def prepareToDraw(self):
        self.color = colors[self.type]
        # self.scale_x = self.cellWidth / self.image.width
        # self.scale_y = self.cellHeight / self.image.height

    def onClick(self):
        #print(row, col)
        pass


class Grid:
    def __init__(self, position, width, height, rows, cols):
        self.x, self.y = position
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.cellWidth = width//cols
        self.cellHeight = height//rows
        self.cells = np.empty((cols, rows), dtype=Cell)
        for i in range(cols):
            for j in range(rows):
                self.cells[i, j] = self.getInitialCell(
                    (self.x + self.cellWidth * i, self.y + self.cellHeight * j), self.cellWidth, self.cellHeight, i, j)

    def getInitialCell(self, position, width, height, col, row):
        return Cell(position, width, height, row, col)

    def draw(self, state):
        for row in self.cells:
            for cell in row:
                cell.type = 'empty'
        for (i, player) in enumerate(state.players):
            for segment in player.segments:
                self.cells[segment[0], segment[1]].type = 'player'+str(i)
        for type, x, y in state.items:
            self.cells[x,y].type = type
        for i in range(self.cols):
            for j in range(self.rows):
                self.cells[i, j].draw()

    def onClick(self, x, y):
        col = (x - self.x) // self.cellWidth
        row = (y - self.y) // self.cellHeight
        print(row, col, "clicked")
        if self.isInGrid(row, col):
            self.cells[row, col].onClick()
            return self.cells[row, col]

    def isInGrid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols
