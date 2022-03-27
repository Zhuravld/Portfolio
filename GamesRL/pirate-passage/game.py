from game_spec_validator import GameSpecValidator, ValidationSummary
from grid import Grid
from utils import points_adjacent, value_is_integer

Point = tuple([int, int])


class Game:
    """Game environment.

    Should take as input a level design specification.
    Should implement methods `step`, `reset` etc,
    as expected for dynamic programming and reinforcement learning.
    """

    def __init__(self, grid_spec: dict):
        errors = GameSpecValidator().validate_spec(grid_spec)
        if errors:
            summ = ValidationSummary(errors)
            print(summ)
            if summ.severity_code >= 2:
                exit()
        self.grid = Grid(grid_spec)

    def step(self, player_action: tuple([Point, Point])) -> bool:
        collisions = self.grid.step(player_action)

        return True if collisions else False

    def validate_action(self, player_action: tuple([Point, Point])) -> str:
        """Validate player action, returning an error string."""
        msg = ""

        if not points_adjacent(*player_action):
            msg = "Can only move to an adjacent field"

        elif to in self.grid.inaccessible:
            msg = "Destination inaccessible to player"

        return msg


class Player:
    """Controlled by user"""

    def __init__(self, game: Game):
        self.game = game
        self.start_field = self.game.grid.start_field
        self.at = self.game.grid.start_field.point
        self.done = False

    def move(self, to: Point) -> bool:
        """Tell grid to register a player move"""
        action = (self.at, to)
        msg = self.game.validate_action(action)
        if not msg:
            self.done = self.game.step(action)
            self.execute_move(to)
        else:
            print(msg)
            self.done = False

        return self.done

    def execute_move(self, to: Point):
        self.at = to


if __name__ == "__main__":
    def input_to_tuple(inp):
        """Parse user input string into coords tuple."""
        for char_to_remove in ["(", ")"]:
            inp = inp.replace(char_to_remove, "")
        return tuple(map(int, inp.strip().split(",")))

    inp = ""
    while inp.lower() not in ("y", "yes", "n", "no"):
        inp = input("Use default spec? (y/n): ")
    if inp[0] == "y":
        from test.test_Grid import test_spec as spec

    else:
        print("Enter custom spec below")
        spec = {}

        shape = input_to_tuple(input("Grid shape: "))
        start = input_to_tuple(input("Start coords: "))
        goal = input_to_tuple(input("Goal coords: "))

        inaccessible = []
        inp = "None"
        print("Enter coords of fields inaccessible to player.")
        print("Hit enter when done.")
        while inp.lower() != "":
            inp = input("New inaccessible field: ")
            if inp:
                inaccessible.append(input_to_tuple(inp))

        pirate_routes = {}
        inp = "None"
        while not value_is_integer(inp.lower()):
            inp = input("Enter number of pirate routes: ")
        n_pirates = int(inp)
        for i in range(n_pirates):
            route = []
            print(f"Enter route waypoints for pirate {i}.")
            print("Hit enter when done")
            inp = "None"
            while inp.lower() != "":
                inp = input("New waypoint coords: ")
                if inp:
                    route.append(input_to_tuple(inp))
            pirate_routes[i] = route

        for param, s in zip(
            [shape, start, goal, inaccessible, pirate_routes],
            ["shape", "start", "goal", "inaccessible", "pirate_routes"],
        ):
            spec[s] = param

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
        try:
            to = input_to_tuple(inp)
            done = p.move(to)
            print(state())
        except:
            pass
