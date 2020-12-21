import socket
import pyglet
import snakeState
import grid

PORT = 54321
HOST = 'localhost'
sock = socket.socket()
sock.connect((HOST, PORT))


class Game(pyglet.window.Window):
    def __init__(self):
        super().__init__(800, 600)
        self.play_area = grid.Grid((0, 0), 500, 500, 50, 50)

    def on_draw(self):
        self.play_area.draw()

    def runUpdatingFromServer(self):
        state = snakeState.SnakeState.decode(sock.recv(1024))
        for player in state.players:
            for segment in player.segments:
                self.play_area.cells[segment[0], segment[1]].type = "player_0"

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.W:
            sock.send('N'.encode())
        elif symbol == pyglet.window.key.A:
            sock.send('W'.encode())
        elif symbol == pyglet.window.key.S:
            sock.send('S'.encode())
        elif symbol == pyglet.window.key.D:
            sock.send('E'.encode())


def update(dt):
    pass


game = Game()
game.runUpdatingFromServer()

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
