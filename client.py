
data = ..recv(1024)
state = SnakeState.decode(data)
for segment in state.players[0].segemnts
    grid