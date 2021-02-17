import unittest
import json

from grid import Grid, Pirate
from utils import Field, PointIndexed

with open('test/test_spec.json') as f:
    json_spec = json.load(f)

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
        self.assertIs(
            grid.shape, grid.fields.shape
        )

    def test_init_params_match(self):
        grid = Grid(json_spec)
        self.assertEquals(
            grid.shape, tuple(json_spec["shape"])
        )
        self.assertEquals(
            grid.inaccessible, json_spec["inaccessible"]
        )
        self.assertEquals(
            grid.start_field.point, tuple(json_spec["start"])
        )
        self.assertEquals(
            grid.goal_field.point, tuple(json_spec["goal"])
        )

        for p in grid.pirates:
            self.assertEquals(
                p.route,
                [tuple(wp) for wp in json_spec["pirate_routes"][p.id]]
            )
class Test_Grid(unittest.TestCase):

    def test_check_in_transit_collisions(self):
        mod_spec = json_spec
        mod_spec["pirate_routes"] = {
            "0":[(1, 0), (0, 0)],
            "1":[(1, 0), (0, 0)],
            "2":[(1, 0), (1, 1)]
        }
        grid = Grid(mod_spec)
        player_action = (
            (0, 0), (1, 0)
        )
        self.assertEquals(
            ["0", "1"], grid.check_in_transit_collisions(player_action)
        )

    def test_check_endpoint_collisions(self):
        mod_spec = json_spec
        mod_spec["pirate_routes"] = {
            "0":[(2, 0), (1, 0)],
            "1":[(1, 1), (1, 0)],
            "2":[(0, 1), (0, 0)]
        }
        grid = Grid(mod_spec)
        player_action = (
            (0, 0), (1, 0)
        )

        self.assertEquals(
            ["0", "1"], grid.check_endpoint_collisions(player_action)
        )

if __name__ == "__main__":
    unittest.main()