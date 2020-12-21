import snakeState
import socket
import pyglet
import threading

PORT = 54321
HOST = 'localhost'
sock = socket.socket()
sock.bind((HOST, PORT))
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
        new = ()
        head = player.segments[0]
        if player.direction == 'N':
            new = (head[0], head[1]+1)
        if player.direction == 'S':
            new = (head[0], head[1]-1)
        if player.direction == 'W':
            new = (head[0]-1, head[1])
        if player.direction == 'E':
            new = (head[0]+1, head[1])
        player.segments.insert(0, new)
        player.segments.pop()
    state = snakeState.SnakeState(players)
    for clientConn in clientConns:
        msg = state.encode()
        clientConn.send(len(msg).to_bytes(4, byteorder='big'))
        clientConn.send(msg)
    # wyślij state klientom


def playerActions(index):
    while True:
        direction = conn.recv(1024).decode()
        players[index].direction = direction

thread = threading.Thread(target=playerActions, args=(0))
thread.start()

pyglet.clock.schedule_interval(update, 1/2)
pyglet.app.run()
