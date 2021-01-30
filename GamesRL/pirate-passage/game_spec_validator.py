
class ValidationSummary:
    """Not yet used. Summarizes all diagnostic strings from GameSpecValidator
    into a single object. 
    
    Access overall severity with `self.severity_code`.
    Add warnings and errors with `self.add_failure_condition`.

    Warning: No unit tests yet for this class.
    """
    def __init__(self):
        self.failure_conditions = []
        self._severity_to_code_map = {
            "OK": 0,
            "warning": 1,
            "error": 2
        }
        self.severity_code = self._severity_to_code_map["OK"]
    
    def __repr__(self):
        severity_code_to_string_map = {
            code:string for string, code in self._severity_to_code_map.items()
        }
        severity_string = \
            severity_code_to_string_map[self.severity_code].upper()

        return "{}\n{}".format(
            severity_string,
            ",\n".join(self.failure_conditions)
        )

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
        """Assert that spec creates a valid game instance."""
        shape = spec["shape"]
        start = spec["start"]
        goal = spec["goal"]
        inaccessible = spec["inaccessible"]
        pirate_routes = spec["pirate_routes"]
        

        valid_shape = self._validate_shape(shape)
        valid_inaccessible = self._validate_inaccessible(shape=shape,
                                                        inaccessible=inaccessible)

        valid_start = self._validate_start(start_point=start,
                                                shape=shape,
                                                inaccessible=inaccessible)
        valid_goal = self._validate_goal(goal_point=goal,
                                                shape=shape,
                                                inaccessible=inaccessible)
        valid_pirates = self._validate_pirates(shape=shape,
                                            pirates_dict=pirate_routes)

        all_valid = all([
            valid_shape,
            valid_start,
            valid_goal,
            valid_inaccessible,
            valid_pirates
        ])
        return all_valid

    def _validate_shape(self, shape):
        """Asserts input shape is valid."""
        components_are_positive = (shape[0] >= 0) and (shape[1] >= 0)
        is_integer = self._point_in_integer_space(point=shape)

        return components_are_positive and is_integer

    def _validate_start(self, start_point, shape, inaccessible):
        """Asserts input start_point is valid"""
        is_int = self._point_in_integer_space(point=start_point)
        in_grid = self._point_in_grid(point=start_point,
                                        grid_shape=shape)
        is_accessible = self._point_accessible(point=start_point,
                                            inaccessible=inaccessible)
        
        return is_int and in_grid and is_accessible

    def _validate_goal(self, goal_point, shape, inaccessible):
        """Asserts input goal_point is valid.
        Return 0 if valid, else 1."""
        is_int = self._point_in_integer_space(point=goal_point)
        in_grid = self._point_in_grid(point=goal_point,
                                        grid_shape=shape)
        is_accessible = self._point_accessible(point=goal_point,
                                            inaccessible=inaccessible)

        # not yet implemented:
        # accessible_from_start = self._goal_accessible_from_start()
        
        return is_int and in_grid and is_accessible# and accessible_from_start

    def _validate_inaccessible(self, shape, inaccessible):
        """Assert all inaccessible points are valid."""
        in_grid = [self._point_in_grid(point, grid_shape=shape) for point in inaccessible]
        return all(in_grid)

    def _validate_pirates(self, shape, pirates_dict):
        """Assert that all pirate routes are valid."""
        is_integer = dict()
        in_grid = dict()
        is_circular = dict()

        for id, route in pirates_dict.items():
            is_integer[id] = all([
                self._point_in_integer_space(point)
                for point in route
            ])
            in_grid[id] = all([
                self._point_in_grid(point, grid_shape=shape)
                for point in route
            ])
            is_circular[id] = self._route_is_circular(route)

        is_valid = {
            id: is_integer[id] and in_grid[id] and is_circular[id]
            for id in pirates_dict.keys()
        }
        return all(is_valid.values())
        
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
        return (point not in inaccessible)

    def _goal_reachable_from_start(self):
        """Depth-first search to validate inaccessible fields"""
        print("Not yet implemented")

    def _route_is_circular(self, route):
        """Check that points in `route` form a continuous loop.
        
        Each point must differ from the next
        by exactly -1/1 in row or column direction.
        """
        adjacent_to_previous = [
            self._points_adjacent(a=point, b=route[i-1])
            for i, point in enumerate(route)
        ]
        return all(adjacent_to_previous)

    @staticmethod
    def _points_adjacent(a, b):
        """Assert that point `a` differs from point `b`
        by -1/1 in row or column direction."""
        row_delta_is_one = (a[0] - b[0]) in (-1, 1)
        col_delta_is_one = (a[1] - b[1]) in (-1, 1)
        xor = row_delta_is_one ^ col_delta_is_one
        return xor

    @staticmethod
    def _value_is_integer(n):
        try:
            f = float(n)
            return f.is_integer()
        except:
            return False
