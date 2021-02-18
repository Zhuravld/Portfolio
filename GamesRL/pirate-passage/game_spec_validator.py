from utils import AdjacencyList, points_adjacent


class ValidationSummary:
    """Not yet used. Summarizes all diagnostic strings from GameSpecValidator
    into a single object.

    Access overall severity with `self.severity_code`.
    Add warnings and errors with `self.add_failure_condition`.
    """

    def __init__(self, failure_conditions=[]):
        self.failure_conditions = failure_conditions
        self._severity_to_code_map = {"OK": 0, "warning": 1, "error": 2}

        self.severity_code = self._severity_to_code_map["OK"]
        for unique_severity in set([cond[0] for cond in failure_conditions]):
            self._update_severity(unique_severity)

    def __repr__(self):
        severity_code_to_string_map = {
            code: string for string, code in self._severity_to_code_map.items()
        }
        severity_string = severity_code_to_string_map[self.severity_code].upper()

        return "{}\n{}".format(severity_string, ",\n".join(self.failure_conditions))

    def add_failure_condition(self, condition):
        """Add failure condition to the list of conditions.
        Elevate severity where needed."""
        severity, diagnosis_string = condition
        self.failure_conditions.append(diagnosis_string)
        self._update_severity(incoming_severity=severity)

    def _update_severity(self, incoming_severity):
        """Set severity to maximum of current and incoming severities."""
        current_code = self.severity_code
        incoming_code = self._severity_to_code_map[incoming_severity]
        self.severity_code = max([current_code, incoming_code])

        return self.severity_code

class GameSpecValidator:
    def validate_spec(self, spec):
        """Assert that `spec` creates a valid game instance.
        
        Return a list of conditions of format:
            ("error_severity_string", "descriptor_string")
        for every condition that invalidates provided specification `spec`
        """
        shape = tuple(spec["shape"])
        start = tuple(spec["start"])
        goal = tuple(spec["goal"])
        inaccessible = spec["inaccessible"]
        pirate_routes = spec["pirate_routes"]

        shape_conditions = self._validate_shape(shape)
        inaccessible_conditions = self._validate_inaccessible(
            shape=shape, inaccessible=inaccessible
        )

        start_field_conditions = self._validate_start(
            start_point=start, shape=shape, inaccessible=inaccessible
        )
        goal_field_conditions = self._validate_goal(
            start_point=start, goal_point=goal, shape=shape, inaccessible=inaccessible
        )
        pirate_conditions = self._validate_pirates(
            shape=shape, pirates_dict=pirate_routes)

        # Flatten
        all_conditions = sum(
            [shape_conditions, inaccessible_conditions, start_field_conditions,
                goal_field_conditions, pirate_conditions],
            []
        )

        return all_conditions

    def _validate_shape(self, shape):
        """Asserts input shape is valid.

        For each prerequisite failed, adds a condition to output list:
            (error_severity_string, descriptor_string)
        """
        failure_conditions = []

        components_are_nonnegative = (shape[0] >= 0) and (shape[1] >= 0)
        if not components_are_nonnegative:
            failure_conditions.append(
                ("error", "Shape must be non-negative")
            )

        is_integer = self._point_in_integer_space(point=shape)
        if not is_integer:
            failure_conditions.append
            (("error", "Shape must be integer")
             )

        return failure_conditions

    def _validate_start(self, start_point, shape, inaccessible):
        """Asserts input start_point is valid.

        For each prerequisite failed, adds a condition to output list:
            (error_severity_string, descriptor_string)
        """
        failure_conditions = []

        is_int = self._point_in_integer_space(point=start_point)
        if not is_int:
            failure_conditions.append(
                ("error", "Start coordinates must be integer")
            )

        in_grid = self._point_in_grid(point=start_point, grid_shape=shape)
        if not in_grid:
            failure_conditions.append(
                ("error", "Start point must be located within input grid")
            )

        is_accessible = self._point_accessible(
            point=start_point, inaccessible=inaccessible
        )
        if not is_accessible:
            failure_conditions.append(
                ("error", "Start point must not be in list of inaccessible fields")
            )

        return failure_conditions

    def _validate_goal(self, start_point, goal_point, shape, inaccessible):
        """Asserts input goal_point is valid and reachable.

        For each prerequisite failed, adds a condition to output list:
            (error_severity_string, descriptor_string)
        """
        failure_conditions = []

        is_int = self._point_in_integer_space(point=goal_point)
        if not is_int:
            failure_conditions.append(
                ("error", "Goal coordinates must be integer")
            )
        in_grid = self._point_in_grid(point=goal_point, grid_shape=shape)
        if not in_grid:
            failure_conditions.append(
                ("error", "Goal point must be located within input grid")
            )
        is_accessible = self._point_accessible(
            point=goal_point, inaccessible=inaccessible
        )
        if not is_accessible:
            failure_conditions.append(
                ("error", "Goal point must not be in list of inaccessible fields")
            )

        accessible_from_start = self._goal_reachable_from_start(
            start_point=start_point,
            goal_point=goal_point,
            grid_shape=shape,
            inaccessible=inaccessible,
        )
        if not accessible_from_start:
            failure_conditions.append(
                ("error", "No path between start and goal")
            )

        return failure_conditions

    def _validate_inaccessible(self, shape, inaccessible):
        """Assert all inaccessible points are valid.
        Return list of failed prerequisites."""
        in_grid = [
            self._point_in_grid(point, grid_shape=shape) for point in inaccessible
        ]
        if sum(in_grid) == len(inaccessible) - 1:
            point_outside_grid = inaccessible[in_grid.index(False)]
            return [("error",
                     f"Point {point_outside_grid} marked inaccessible, but is outside grid"
                     )]
        elif sum(in_grid) < len(inaccessible) - 1:
            return [("error",
                     "Multiple points marked inaccessible, but are outside grid"
                     )]
        else:
            return []

    def _validate_pirates(self, shape, pirates_dict):
        """Assert that all pirate routes are valid.

        For each prerequisite failed, adds a condition to output list:
            (error_severity_string, descriptor_string)
        """
        failure_conditions = []
        is_integer = {}
        in_grid = {}
        is_circular = {}

        for id, route in pirates_dict.items():
            is_integer[id] = all(
                [self._point_in_integer_space(point) for point in route]
            )
            if not is_integer[id]:
                failure_conditions.append(
                    ("error", f"Pirate: {id} has points not in integer space")
                )

            in_grid[id] = all(
                [self._point_in_grid(point, grid_shape=shape)
                 for point in route]
            )
            if not in_grid[id]:
                failure_conditions.append(
                    ("error", f"Pirate: {id} has points outside grid")
                )

            is_circular[id] = self._route_is_circular(route)
            if not is_circular[id]:
                failure_conditions.append(
                    ("error", f"Pirate: {id} route is not circular")
                )

        return failure_conditions

    def _point_in_integer_space(self, point):
        """Assert that all components in `point` are integer-valued.
        Warning: Does not raise errors for nonsense inputs; simply returns False.
        """
        return all([self._value_is_integer(comp) for comp in point])

    def _point_in_grid(self, point, grid_shape):
        """Assert that point exists in grid"""
        row_coord_valid = (point[0] < grid_shape[0]) and (point[0] >= 0)
        col_coord_valid = (point[1] < grid_shape[1]) and (point[0] >= 0)

        return row_coord_valid and col_coord_valid

    def _point_accessible(self, point, inaccessible):
        return point not in inaccessible

    def _goal_reachable_from_start(
        self, start_point, goal_point, grid_shape, inaccessible
    ):
        """Depth-first search to validate inaccessible fields"""
        graph = AdjacencyList(grid_shape=grid_shape, inaccessible=inaccessible)

        return graph.depth_first_search(start=start_point, end=goal_point)

    def _route_is_circular(self, route):
        """Check that points in `route` form a continuous loop.

        Each point must differ from the next
        by exactly -1/1 in row or column direction.
        """
        adjacent_to_previous = [
            self._points_adjacent(a=point, b=route[i - 1])
            for i, point in enumerate(route)
        ]
        return all(adjacent_to_previous)

    @staticmethod
    def _points_adjacent(a, b):
        return points_adjacent(a, b)

    @staticmethod
    def _value_is_integer(n):
        try:
            f = float(n)
            return f.is_integer()
        except:
            return False
