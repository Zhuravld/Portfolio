from utils import PointIndexed, Field

Point = tuple([int, int])


class Pirate:
    """Enemy. Occupies a single Field, travels along a route.

    at: current location (field ref or point coords)
    id: identifier
    route: list of waypoints
    """

    _count = 0

    def __init__(self, route_waypoints: list, id=None):
        self.route = [tuple(wp) for wp in route_waypoints]
        self.i = 0

        Pirate._count += 1
        if id is None:
            id = Pirate._count

        self.id = id

    def execute_move(self):
        self.i = (self.i + 1) % len(self.route)

    def _next(self):
        return self.route[(self.i + 1) % len(self.route)]

    @property
    def at(self):
        return self.route[self.i]


class Grid:
    """Gridworld. Handles interaction of pirate and player objects
    on a `PointIndexed` collection of `Field`s.

    Agents on the grid communicate an intended move
    by passing the `Grid` obj as parameter.
    """

    # TODO: Test Grid class
    def __init__(self, spec: dict):
        shape, start, goal, inaccessible, pirate_routes = map(
            lambda k: spec[k],
            ["shape", "start", "goal", "inaccessible", "pirate_routes"],
        )

        self.fields = self._initialize_fields(shape)
        self._mark_inaccessible_fields(inaccessible)
        self._set_start_and_goal_fields(start, goal)
        self.pirates = self._initialize_pirates(pirate_routes)

    @property
    def shape(self) -> tuple([int, int]):
        return self.fields.shape

    def _initialize_fields(self, shape):
        """Generate grid of Fields from `shape` (2-tuple)"""
        nrows, ncols = shape
        return PointIndexed(
            [  # 2D collection of Fields, indexed by (r,c)
                [Field((row_idx, col_idx)) for row_idx in range(nrows)]
                for col_idx in range(ncols)
            ]
        )

    def _mark_inaccessible_fields(self, inaccessible: list(Point)):
        """Modify `self.grid` inplace to mark inaccessible fields."""
        self.inaccessible = inaccessible
        for point in inaccessible:
            self.fields[point].player_can_access = False

    def _set_start_and_goal_fields(self, start_point: Point, goal_point: Point):
        """Init references to start and goal fields."""
        self.start_field = self.fields[start_point]
        self.goal_field = self.fields[goal_point]

    def _initialize_pirates(self, pirate_routes: dict) -> list([Pirate]):
        pirates = [Pirate(route, id=i) for i, route in pirate_routes.items()]
        return pirates

    def step(self, player_action: tuple([Point, Point])) -> list:
        """Increment grid state given `player_action`.
        Return IDs of all collided pirates"""
        in_transit_collisions = self.check_in_transit_collisions(player_action)
        endpoint_collisions = self.check_endpoint_collisions(player_action)

        if in_transit_collisions:
            self._message(
                f"Collided with pirates in transit: {', '.join(in_transit_collisions)}"
            )
        elif endpoint_collisions:
            self._message(
                f"Collided with pirates at endpoint: {', '.join(endpoint_collisions)}"
            )
        self._execute_movements()

        if in_transit_collisions:
            return in_transit_collisions
        else:
            return endpoint_collisions

    def get_pirate_moves(self) -> dict:
        return {p.id: (p.at, p._next()) for p in self.pirates}

    def _execute_movements(self):
        # self._message("Sending all movements commands")
        for p in self.pirates:
            p.execute_move()

    def _message(self, msg):
        """Placeholder for sending data to the UI"""
        print(msg)

    def check_in_transit_collisions(self, player_action: tuple([Point, Point])) -> list:
        player_from, player_to = player_action
        pirates_collided = []

        for pirate_id, from_to in self.get_pirate_moves().items():
            pirate_from, pirate_to = from_to
            if (pirate_from == player_to) and (pirate_to == player_from):
                pirates_collided.append(pirate_id)

        return pirates_collided

    def check_endpoint_collisions(self, player_action: tuple([Point, Point])) -> list:
        _, player_to = player_action
        pirates_collided = []

        for pirate_id, (pirate_from, pirate_to) in self.get_pirate_moves().items():
            if pirate_to == player_to:
                pirates_collided.append(pirate_id)

        return pirates_collided
