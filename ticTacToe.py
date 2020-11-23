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
        if self.owner:
            self.image = self.owner.symbol

        super().prepareToDraw()


class Player:
    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name


class TicTacToeGrid(Grid):
    def getInitialCell(self, position, cellWidth, cellHeight, row, col):
        return TicTacToeCell(position, cellWidth, cellHeight, row, col)


class TicTacToe(pyglet.window.Window):
    def __init__(self, rows, cols, players, winlen):
        super().__init__(800, 600)
        self.grid = TicTacToeGrid((50, 50), 500, 500, rows, cols)
        self.reset()
        self.players = players
        self.currentPlayerIndex = 0
        self.winlen = winlen

    def getCurrentPlayer(self):
        return self.players[self.currentPlayerIndex]

    def changeCurrentPlayer(self):
        self.currentPlayerIndex = (
            self.currentPlayerIndex + 1) % len(self.players)

    def reset(self):
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                self.grid.cells[i, j].owner = None

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            cellClicked = self.grid.onClick(x, y)
            if cellClicked is not None and cellClicked.owner is None:
                cellClicked.owner = self.getCurrentPlayer()
                if self.isGameFinished(cellClicked):
                    self.gameOver()
                self.changeCurrentPlayer()

    def gameOver(self):
        self.canPlay = False
        print(f'Wygral {self.getCurrentPlayer().name}')
        pyglet.clock.schedule_once(self.resetAfterGameOver, 2.0)

    def resetAfterGameOver(self, dt):
        self.reset()

    def checkSequence(self, symbol, direction, pos):
        count = 0
        while True:
            if self.grid.isInGrid(pos[0], pos[1]) and symbol == self.grid.cells[pos[0]][pos[1]].owner:
                pos[0] += direction[0]
                pos[1] += direction[1]
                count += 1
            else:
                return count

    def isGameFinished(self, lastcell):
        symbol = lastcell.owner
        horizontalsum = self.checkSequence(symbol, [0, 1], [lastcell.col, lastcell.row]) + self.checkSequence(symbol, [0, -1], [lastcell.col, lastcell.row]) -1
        print(horizontalsum)
        if horizontalsum  >= self.winlen:
            return True
        return False
        
    def on_draw(self):
        self.grid.draw()


name1 = input("podaj imie: ")
name2 = input("podaj drugie imie: ")
players = [Player(circleImg, name1), Player(crossImg, name2)]
game = TicTacToe(3, 3, players, 3)

pyglet.app.run()
