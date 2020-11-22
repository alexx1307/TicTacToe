from grid import Grid, Cell
import pyglet
import numpy as np

circleImg = pyglet.image.load('./assets/circle.png')
crossImg = pyglet.image.load('./assets/cross.png')
emptyImg = pyglet.image.load('./assets/empty.png')

class TicTacToeCell(Cell):
    def __init__(self, position, width, height, row, col):
        super().__init__(emptyImg, position, width, height, row, col)
        self.owner = None
    def prepareToDraw(self):
        #TODO
        super().prepareToDraw()

class TicTacToeGrid(Grid):
    def getInitialCell(self, position, cellWidth, cellHeight, row, col):
        return TicTacToeCell(position, cellWidth, cellHeight, row, col)

class TicTacToe(pyglet.window.Window):
    def __init__(self, rows, cols):
        super().__init__(800, 600)
        self.grid = TicTacToeGrid((50,50), 500, 500, rows, cols)
        self.reset()

    def reset(self):
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                self.grid.cells[i, j].owner = None
        

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            cellClicked = self.grid.onClick(x, y)
            if cellClicked is not None: 
                if self.isGameFinished():
                   self.gameOver()

    def gameOver(self):
        self.canPlay = False
        print(f'Wygral {self.getCurrentPlayer().symbol}')
        pyglet.clock.schedule_once(self.resetAfterGameOver, 2.0)
    
    def resetAfterGameOver(self, dt):
        self.reset()

    def isGameFinished(self):
        pass

    def on_draw(self):
        self.grid.draw()
    
game = TicTacToe(3, 3)

pyglet.app.run()