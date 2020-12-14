from snakeState import *
import pyglet

players = [SnakePlayer([(5,5), (4,5)], 'E'), SnakePlayer([(35,5), (36,5)], 'W')]


def update(dt):
    for player in players:
        player.updateStep()
    state = SnakeState(players)
    #clientConn.send(state.encode())
    #wyślij state klientom

def playerActions():
    pass

pyglet.clock.schedule_interval(update, 1/2)