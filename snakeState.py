from marshmallow import fields, Schema, post_load
import json

class SnakeState:
    def __init__(self, players, items):
        self.players = players
        self.items = items
    def encode(self):
        return json.dumps(SnakeStateSchema().dump(self)).encode()

    @staticmethod
    def decode(encodedState):
        encodedState = encodedState.decode()
        print(encodedState)
        return SnakeStateSchema().load(json.loads(encodedState.strip()))


class SnakePlayer:
    def __init__(self, segments, direction):
        self.segments = segments
        self.direction = direction

class SnakePlayerSchema(Schema):
    direction = fields.Str()
    segments = fields.List(fields.Tuple((fields.Int(), fields.Int()) ))

    @post_load
    def make_snakeplayer(self, data, **kwargs):
        return SnakePlayer(**data)

class SnakeStateSchema(Schema):
    players = fields.List(fields.Nested(SnakePlayerSchema))
    items = fields.List(fields.Tuple((fields.Str, fields.Int, fields.Int)))
    @post_load
    def make_snakestate(self, data, **kwargs):
        return SnakeState(**data)


# players = [SnakePlayer([(5,5), (4,5)], 'E'), SnakePlayer([(35,5), (36,5)], 'W')]
# state = SnakeState(players)
# encodedState = state.encode()
# print(encodedState, type(encodedState))

# statePrim = SnakeState.decode(encodedState)
# print(statePrim)