import unittest
import json

from game_spec_validator import GameSpecValidator

with open('test/test_spec.json') as f:
    json_spec = json.load(f)

class Test_GameSpecValidator(unittest.TestCase):

    def test_value_is_integer(self):
        is_int = GameSpecValidator._value_is_integer
        self.assertFalse(is_int("one"))
        self.assertFalse(is_int("2.1"))
        self.assertTrue(is_int("3.0"))
        self.assertTrue(is_int("4"))
        self.assertTrue(is_int(5))
        self.assertTrue(is_int(6.0))

    def test_point_in_grid(self):
        in_grid = GameSpecValidator()._point_in_grid
        kwargs = {
            "point": None,
            "grid_shape": (3, 3)
        }

        row_out_of_bounds = (4, 1)
        kwargs["point"] = row_out_of_bounds
        self.assertFalse(in_grid(**kwargs))

        col_out_of_bounds = (2, 3)
        kwargs["point"] = col_out_of_bounds
        self.assertFalse(in_grid(**kwargs))

        negative_coord = (-1, 1)
        kwargs["point"] = negative_coord
        self.assertFalse(in_grid(**kwargs))

        point_in_bounds = (2, 2)
        kwargs["point"] = point_in_bounds
        self.assertTrue(in_grid(**kwargs))

    def test_input_types_point_in_integer_space(self):
        in_int_space = GameSpecValidator()._point_in_integer_space        

        self.assertTrue(in_int_space((1, 4)))
        self.assertTrue(in_int_space([1, 4]))
        self.assertTrue(in_int_space(range(1, 5)))
        self.assertTrue(in_int_space(("1", "4")))
    
    def test_input_values_point_in_integer_space(self):
        in_int_space = GameSpecValidator()._point_in_integer_space        

        self.assertTrue(in_int_space((0, 4)))
        self.assertTrue(in_int_space(("0", "4")))
        self.assertFalse(in_int_space((1.5, 4)))
        self.assertFalse(in_int_space(("one", "four")))

    def test_points_adjacent(self):
        adj = GameSpecValidator()._points_adjacent

        self.assertTrue(adj(a=(0, 1), b=(1, 1)))
        self.assertTrue(adj(a=(2, 1), b=(2, 0)))
        self.assertFalse(adj(a=(0, 1), b=(1, 0)))
        self.assertFalse(adj(a=(1, 0), b=(1, 0)))

    def test_route_is_circular(self):
        is_circular = GameSpecValidator()._route_is_circular

        self.assertTrue(is_circular(
            [[1,1], [1,2], [2,2], [2,1]]
        ))
        self.assertFalse(is_circular(
            [[1,1], [1,2], [1,3], [1, 4]]
        ))
        self.assertFalse(is_circular(
            [[1,1], [2,2], [2,1]]
        ))

    def test_validate_empty_pirates_returns_empty(self):
        self.assertEquals([], GameSpecValidator()._validate_pirates(
            shape=(2, 2), pirates_dict={})
        )

    def test_validate_spec(self):
        self.assertEquals([], GameSpecValidator().validate_spec(json_spec))


if __name__ == "__main__":
    unittest.main()
    