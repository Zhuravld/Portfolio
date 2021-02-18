from game_spec_validator import GameSpecValidator
from grid import Grid
from utils import points_adjacent

class Game:
    """Game environment.
    
    Should take as input a level design specification.
    Should implement methods `step`, `reset` etc,
    as expected for dynamic programming and reinforcement learning.
    """
    def __init__(self, grid_spec):
        GameSpecValidator().validate_spec(grid_spec)
        self.grid = Grid(grid_spec)

    def step(self, player_action):
        collisions = self.grid.step(player_action)

        return True if collisions else False

    def validate_action(self, player_action):
        """Validate player action, returning an error string if any."""
        msg = None

        if not points_adjacent(*player_action):
            msg = "Can only move to an adjacent field"

        elif (to in self.grid.inaccessible):
            msg = "Destination inaccessible to player"

        return msg

class Player:
    """Controlled by user"""
    def __init__(self, game):
        self.game = game
        self.start_field = self.game.grid.start_field
        self.at = self.game.grid.start_field.point
        self.done = False

    def move(self, to):
        """Tell grid to register a player move"""
        action = (self.at, to)
        msg = self.game.validate_action(action)
        if not msg:
            self.done = self.game.step(action)
            self.execute_move(to)
        else:
            print(msg)
        
        return self.done

    def execute_move(self, to):
        self.at = to

if __name__ == '__main__':
    import json

    with open("test/test_spec.json", "r") as f:
        spec = json.load(f)
    
    game = Game(spec)
    p = Player(game)
    
    def enemies():
        return [p.at for p in game.grid.pirates]
    
    def state():
        return p.at, enemies()
    
    print("Initial state:")
    print(state())

    done = False
    while not done:
        inp = input("Enter move here: ")
        to = tuple(map(int, inp.replace('()','').strip().split(',')))
        done = p.move(to)
        print(state())