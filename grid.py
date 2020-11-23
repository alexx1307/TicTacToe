import pyglet
import numpy as np

class Cell(pyglet.sprite.Sprite):
    def __init__(self, image, position, width, height, row, col):
        super().__init__(image, *position)
        self.cellWidth = width
        self.cellHeight = height
        self.row = row
        self.col = col

    def draw(self):
        self.prepareToDraw()
        super().draw()
    
    def prepareToDraw(self):
        self.scale_x = self.cellWidth / self.image.width
        self.scale_y = self.cellHeight / self.image.height

    def onClick(self):
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
        self.cells = np.empty( (rows,cols), dtype=Cell)
        for i in range(rows):
            for j in range(cols):
                self.cells[i, j] = self.getInitialCell((self.x + self.cellWidth * j, self.y + self.cellHeight * i ), self.cellWidth, self.cellHeight, i, j)
    


    def draw(self):
        for i in range(self.rows):
            for j in range(self.cols):  
                self.cells[i,j].draw()
    
    def onClick(self, x, y):
        col = (x - self.x) // self.cellWidth
        row = (y - self.y) // self.cellHeight
        print(row, col, "clicked")
        if self.isInGrid(row, col):
            self.cells[row, col].onClick()
            return self.cells[row, col]

    def isInGrid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols