import socket
import pyglet
import threading
import grid
from snakeState import SnakeState
HOST = 'localhost'
PORT = 54321

print("start gry")
sock = socket.socket()
sock.connect((HOST, PORT))
print("połączono z serwerem")


class Game(pyglet.window.Window):
    def __init__(self):
        super().__init__(800, 600)
        self.grid = grid.Grid((0,0), 500, 500, 50, 50)
        self.ready = False
    def on_draw(self):
        if self.ready:
            self.grid.draw(self.state)
    def run(self):
        threading.Thread(target = self.updatingFromServer, daemon=True).start()
    def updatingFromServer(self):
        while True:
            len = int.from_bytes(sock.recv(4), byteorder='big')
            data = sock.recv(len)
            self.state = SnakeState.decode(data)
            self.ready = True
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.W:
            sock.send('N'.encode())
        elif symbol == pyglet.window.key.A:
            sock.send('W'.encode())        
        elif symbol == pyglet.window.key.S:
            sock.send('S'.encode())
        elif symbol == pyglet.window.key.D:
            sock.send('E'.encode())
        print(symbol)
def update(dt):
    pass    
game = Game()
game.run()
pyglet.clock.schedule_interval(update, 1/5)
pyglet.app.run()
