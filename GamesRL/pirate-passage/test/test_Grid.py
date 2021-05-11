import unittest

from grid import Grid, Pirate
from utils import Field, PointIndexed

test_spec = {
    "shape": [4, 4],
    "start": [0, 0],
    "goal": [3, 3],
    "inaccessible": [[2, 1], [1,2]],
    "pirate_routes": {
        "0": [[1,1], [1,2], [2,2], [2,1]]
    }
}


class Test_Grid_init_from_spec(unittest.TestCase):
    def test_new_instance(self):
        grid = Grid.__new__(Grid)
        self.assertIsInstance(grid, Grid)

    def test_grid_type_is_PointIndexed(self):
        grid = Grid.__new__(Grid)
        grid.fields = grid._initialize_fields((4, 4))
        self.assertIsInstance(grid.fields, PointIndexed)

    def test_grid_unit_is_Field(self):
        grid = Grid.__new__(Grid)
        grid.fields = grid._initialize_fields((4, 4))
        self.assertIsInstance(grid.fields[(0, 0)], Field)

    # def test_mark_inaccessible_fields(self):
    #     pass

    # def test_set_start_and_goal_fields(self):
    #     pass

    def test_initialize_pirates_empty_dict_returns_list(self):
        grid = Grid.__new__(Grid)
        pirates = grid._initialize_pirates({})
        self.assertEqual(pirates, [])

    def test_shape(self):
        grid = Grid.__new__(Grid)
        grid.fields = grid._initialize_fields((2, 2))
        self.assertIs(grid.shape, grid.fields.shape)

    def test_init_params_match(self):
        grid = Grid(test_spec)
        self.assertEqual(grid.shape, tuple(test_spec["shape"]))
        self.assertEqual(grid.inaccessible, test_spec["inaccessible"])
        self.assertEqual(grid.start_field.point, tuple(test_spec["start"]))
        self.assertEqual(grid.goal_field.point, tuple(test_spec["goal"]))

        for p in grid.pirates:
            self.assertEqual(
                p.route, [tuple(wp) for wp in test_spec["pirate_routes"][p.id]]
            )


class Test_Grid(unittest.TestCase):
    def test_check_in_transit_collisions(self):
        mod_spec = test_spec
        mod_spec["pirate_routes"] = {
            "0": [(1, 0), (0, 0)],
            "1": [(1, 0), (0, 0)],
            "2": [(1, 0), (1, 1)],
        }
        grid = Grid(mod_spec)
        player_action = ((0, 0), (1, 0))
        self.assertEqual(["0", "1"], grid.check_in_transit_collisions(player_action))

    def test_check_endpoint_collisions(self):
        mod_spec = test_spec
        mod_spec["pirate_routes"] = {
            "0": [(2, 0), (1, 0)],
            "1": [(1, 1), (1, 0)],
            "2": [(0, 1), (0, 0)],
        }
        grid = Grid(mod_spec)
        player_action = ((0, 0), (1, 0))

        self.assertEqual(["0", "1"], grid.check_endpoint_collisions(player_action))


if __name__ == "__main__":
    unittest.main()
