from game_spec_validator import GameSpecValidator
from grid import Grid
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
        return self.grid.step(player_action)

class Player:
    """Controlled by user"""
    def __init__(self, start, on_grid):
        self.at = start
        self.grid = on_grid

    def request_move(self, to):
        """Tell grid to register a player move"""
        if to not in self.grid.inaccessible:
            self.grid.set_player_move(self.at, to)
        else:
            print("Destination inaccessible to player")
        
    def execute_move(self, to):
        self.at = to


class Planner:
    """GUI component that takes valid fields as argument,
    allowing user to plan a route.

    Upon final confirmation, outputs a player route.
    """
    pass