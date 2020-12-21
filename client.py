import socket
import pyglet
import snakeState
PORT = 54321
HOST = 'localhost'
sock = socket.socket()
sock.connect((HOST, PORT))

class Game(pyglet.window.window):
    def __init__(self):
        super().__init__(800, 600)
    def on_draw(self):
        pass
    def runUpdatingFromServer(self):
        state = snakeState.SnakeState.decode(sock.recv(1024))

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.W:
            sock.send('N'.encode())
        elif symbol == pyglet.window.key.A:
            sock.send('W'.encode())        
        elif symbol == pyglet.window.key.S:
            sock.send('S'.encode())
        elif symbol == pyglet.window.key.D:
            sock.send('E'.encode())

def update():
    pass
game = Game()
game.runUpdatingFromServer()

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
