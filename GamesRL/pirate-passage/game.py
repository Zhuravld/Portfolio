from game_spec_validator import GameSpecValidator

# from dataclasses import dataclass
# 
# @dataclass
class Field:
    """Placeholder object for a single field in the grid.
    It can empty, inaccessible, etc.

    Object should fully describe what's at `self.point`,
    but implement no mechanism for change."""
    def __init__(self, point):
        self.point = point
        self.pirates = []
        self.contains_player = False
        self.player_can_access = True
    
    def __repr__(self):
        return f"<Field: {self.point}>"

class PointIndexed:
    """Wrapper for multi-dimensional list-like, L.
    Replaces indexing by L[x][y] with L[x, y] instead."""
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def __repr__(self):
        type_ = type(self)
        module = type_.__module__
        qualname = type_.__qualname__

        return "<{}.{} object at {}\n{}".format(
            module,
            qualname,
            hex(id(self)),
            repr(self._wrapped)
        )

    def __getitem__(self, indices):
        current = self._wrapped
        for index in indices:
            current = current[index]
        return current

class Pirate:
    """Enemy. Occupies a single Field, travels along a route.
    
    at: current location (field ref or point coords)
    id: identifier
    route: list of waypoints
    """
    _count = 0
    def __init__(self, route_waypoints, id=None):
        self.route = route_waypoints
        self.at = self.route[0]

        Pirate._count += 1
        if id is None:
            id = Pirate._count

        self.id = id

    def point_to_new_field(self, to_field):
        pass
        # self.at = to_field

class Grid:
    """Gridworld. Handles interaction of pirate and player objects
    on a PointIndexed collection of Fields.
    
    Not yet tested.
    """
    def __init__(self, fields):
        self.fields = fields
        self.pirate_moves = {}
        self.player_move = None

    # Game.step():
    #   Collect all from-to's for pirates and player
    #   Check for in-transit collisions
    #   Send all movement commands,
    #       along with in-transit collision flag, to the UI
    #   Check for endpoint collisions
    #   Check if done
    
    # Let's write assuming that each agent will call the method:
    #   def move(to, on_grid):
    #       on_grid.add_pirate_move(to)
    #       # or
    #       on_grid.set_player_move(to)

    def add_pirate_move(self, pirate_id, move_from, move_to):
        self.pirate_moves[pirate_id] = (move_from, move_to)
    
    def set_player_move(self, move_from, move_to):
        self.player_move = (move_from, move_to)
    
    def check_in_transit_collisions(self):
        player_from, player_to = self.player_move
        pirates_collided = []

        for pirate_id, from_to in self.pirate_moves.items():
            pirate_from, pirate_to = from_to
            if (pirate_from == player_to) \
            and (pirate_to == player_from):
                pirates_collided.append(pirate_id)
                
        return pirates_collided
        
    def check_endpoint_collisions(self):
        _, player_to = self.player_move
        pirates_collided = []

        # test unpacking syntax
        for pirate_id, (_, pirate_to) in self.pirate_moves.items():
            if pirate_to == player_to:
                pirates_collided.append(pirate_id)
        
        return pirates_collided


class Game:
    """Game environment.
    
    Should take as input a level design specification.
    Should implement methods `step`, `reset` etc,
    as expected for dynamic programming and reinforcement learning.
    """
    def __init__(self, spec):
        _ = GameSpecValidator().validate_spec(spec)
        self.grid = self._initialize_grid(spec["shape"])
        self._set_start_and_goal_fields(start_point=spec["start"],
                                        goal_point=spec["goal"])
        self._mark_inaccessible_fields(spec["inaccessible"])
        self.pirates = self._initialize_pirates(spec["pirate_routes"])

    def _initialize_grid(self, shape):
        """Generate grid of Fields from `shape` (2-tuple)"""
        nrows, ncols = shape
        return PointIndexed([ # 2D collection of Fields, indexed by (r,c)
            [Field((row_idx, col_idx)) for row_idx in range(nrows)]
            for col_idx in range(ncols)
        ])

    def _set_start_and_goal_fields(self, start_point, goal_point):
        """Init references to start and goal fields."""
        self.start_field = self.grid[start_point]
        self.goal_field = self.grid[goal_point]
    
    def _mark_inaccessible_fields(self, inaccessible_points):
        """Modify `self.grid` inplace to mark inaccessible fields."""
        for point in inaccessible_points:
            self.grid[point].player_can_access = False

    def _initialize_pirates(self, pirate_routes):
        """Collect and initialize pirates based on spec.
        
        If `list` of lists is provided instead of `dict` of lists,
        cast input to `dict` with `enumerate`.
        """
        try:
            getattr(pirate_routes, "items")
        except AttributeError:
            pirate_routes = dict(enumerate(pirate_routes))

        pirates = {
            custom_id: Pirate(route_waypoints=route, id=custom_id)
            for custom_id, route in pirate_routes.items()
        }
        return pirates

    def step(self, action):
        """Conceptual structure to outline all stages."""
        pass
        # Collect all from-to's for pirates and player
        # Check for in-transit collisions
        # Send all movement commands,
        #   along with in-transit collision flag, to the UI
        # Check for endpoint collisions
        # Check if done

    def move_vessel_to(self, vessel, to_field):
        """Vessel points to a new Field;
        Start and end fields register the move"""
        pass
        # from_field = vessel.at
        ## TODO:
        # vessel.point_to_new_field(to_field)

        # from_field.register_move("-vessel")
        # to_field.register_move("+vessel")
    
class Player:
    """Controlled by user"""
    pass

class Planner:
    """GUI component that takes valid fields as argument,
    allowing user to plan a route.

    Upon final confirmation, outputs a player route.
    """
    pass