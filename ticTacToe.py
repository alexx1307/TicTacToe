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
        if self.owner is not None:   
            self.image = self.owner.img
        else:
            self.image = emptyImg
        super().prepareToDraw()

class Player:
    def __init__(self, img, symbol):
        self.img = img
        self.symbol = symbol


class TicTacToeGrid(Grid):
    def getInitialCell(self, position, cellWidth, cellHeight, row, col):
        return TicTacToeCell(position, cellWidth, cellHeight, row, col)

class TicTacToe(pyglet.window.Window):
    def __init__(self, rows, cols, reqLength):
        super().__init__(800, 600)
        self.grid = TicTacToeGrid((50,50), 500, 500, rows, cols)
        self.players = [Player(circleImg, 'CIRCLE'), Player(crossImg, 'CROSS')]
        self.reqLength = reqLength
        self.reset()

    def getCurrentPlayer(self):
        return self.players[self.currentPlayerIndex]

    def changeCurrentPlayerSymbol(self):
        self.currentPlayerIndex = (self.currentPlayerIndex + 1) %2

    def reset(self):
        self.currentPlayerIndex = 0
        self.canPlay = True
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                self.grid.cells[i, j].owner = None
        

    def on_mouse_press(self, x, y, button, modifiers):
        if self.canPlay and button == pyglet.window.mouse.LEFT:
            cellClicked = self.grid.onClick(x, y)
            if cellClicked is not None and cellClicked.owner is None:
                cellClicked.owner = self.getCurrentPlayer()
                if self.isGameFinished():
                   self.gameOver()
                else:
                    self.changeCurrentPlayerSymbol()

    def gameOver(self):
        self.canPlay = False
        print(f'Wygral {self.getCurrentPlayer().symbol}')
        pyglet.clock.schedule_once(self.resetAfterGameOver, 2.0)
    
    def resetAfterGameOver(self, dt):
        self.reset()

    def isGameFinished(self):
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                if self.grid.cells[i,j].owner is not None:
                    res = self.checkSeq((i, j), (1, 0), self.grid.cells[i,j].owner, self.reqLength)
                    res |= self.checkSeq((i, j), (1, 1), self.grid.cells[i,j].owner, self.reqLength)
                    res |= self.checkSeq((i, j), (0, 1), self.grid.cells[i,j].owner, self.reqLength)
                    if res == True:
                        return True
        return False
    
    def checkSeq(self, startPos, offset, value, left):
        if left == 0:
            return True
        if self.grid.isInGrid(*startPos) and self.grid.cells[startPos[0], startPos[1]].owner == value:
            return self.checkSeq(np.add(startPos,offset), offset, value, left -1)
        else: 
            return False

    def on_draw(self):
        self.grid.draw()
    


game = TicTacToe(10, 10, 5)

pyglet.app.run()