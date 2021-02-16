import unittest
import json

from grid import Grid
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
    
    def test_initialize_pirates_casts_list_to_dict(self):
        grid = Grid.__new__(Grid)
        pirates = grid._initialize_pirates(
            [[1,1], [1,2], [2,2], [2,1]]
        )
        self.assertIsInstance(pirates, dict)

    def test_initialize_pirates_empty_dict(self):
        grid = Grid.__new__(Grid)
        pirates = grid._initialize_pirates({})
        self.assertEqual(pirates, {})

class Test_Grid(unittest.TestCase):

    def test_check_in_transit_collisions(self):
        mod_spec = json_spec
        mod_spec["pirate_routes"] = {
            "0":[[1,0], [0, 0]],
            "1":[[1,0], [0, 0]],
            "2":[[0,1], [0, 0]],
            "3":[(1, 0), (0, 0)]
        }
        grid = Grid(mod_spec)
        player_action = (
            (0, 0), (1, 0)
        )
        self.assertEquals(
            ["3"], grid.check_in_transit_collisions(player_action)
        )

    def test_check_endpoint_collisions(self):
        nrows, ncols = (2, 2)
        fields = PointIndexed([
            [Field((r, c)) for r in range(nrows)]
            for c in range(ncols)
        ])
        grid = Grid(fields)

        grid.set_player_move(
            (0, 0), (0, 1)
        )
        for pirate_id in (0, 1):
            grid.add_pirate_move(pirate_id, 
                (1, 1), (0, 1)
            )

        self.assertEquals([0, 1], grid.check_endpoint_collisions())

if __name__ == "__main__":
    unittest.main()