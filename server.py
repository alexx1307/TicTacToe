from snakeState import SnakePlayer, SnakeState
import socket
import pyglet
import socket
import threading
import random



playersNumber = 1
HOST = 'localhost'
PORT = 54321
serverSock = socket.socket()
serverSock.bind((HOST, PORT))
serverSock.listen(playersNumber)

width = 50
height = 50

players = [SnakePlayer([(5,5), (4,5)], 'E')] #, SnakePlayer([(35,5), (36,5)], 'W')
items = []
def handlePlayerAction(index,conn):
    while True:
        direction = conn.recv(1024).decode()
        players[index].direction = direction

print('Waiting for players')
for i, player in enumerate(players):
    conn, attr = serverSock.accept()
    threading.Thread(target=handlePlayerAction, args = (i, conn)).start()
print('Starting game')
def update(dt):    
    for player in players:
        head = player.segments[0]
        new = None
        eat = False
        if player.direction == 'N':
            new = (head[0], head[1]+1)
        if player.direction == 'S':
            new = (head[0], head[1]-1)
        if player.direction == 'W':
            new = (head[0]-1, head[1])
        if player.direction == 'E':
            new = (head[0]+1, head[1])
        new[0] %= width
        new[1] %= height
        for item in items:
            type, x, y = item
            if x == new[0] and y == new[1]:
                eat = True
                items.remove(item)
                break
        player.segments.insert(0, new)
        if eat == False:
            player.segments.pop()
    if items == []:
        x = random.randint(0,49)
        y = random.randint(0,49)
        items.append(('apple', x, y))

    state = SnakeState(players, items).encode()
    print(f'{dt} sending state {state}')
    conn.send(len(state).to_bytes(4, byteorder='big'))
    conn.send(state)
    #wyślij state klientom

pyglet.clock.schedule_interval(update, 1/5)
pyglet.app.run()
