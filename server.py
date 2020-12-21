import snakeState
import socket
import pyglet

PORT = 54321
HOST = 'localhost'
sock = socket.socket()
sock.bind((HOST, PORT))
# , SnakePlayer([(35,5), (36,5)], 'W')
players = [snakeState.SnakePlayer([(5, 5), (4, 5)], 'E')]

clientConns = []

sock.listen(len(players))
print('waiting for players')
for player in players:
    conn, addr = sock.accept()
    print(f'{addr} connected')
    clientConns.append(conn)

print('starting game')


def update(dt):
    for player in players:
        player.updateStep()
    state = snakeState.SnakeState(players)
    for clientConn in clientConns:
        clientConn.send(state.encode())
    # wyślij state klientom


def playerActions(index):
    while True:
        direction = conn.recv(1024).decode()
        players[index].direction = direction


pyglet.clock.schedule_interval(update, 1/2)
pyglet.app.run()
