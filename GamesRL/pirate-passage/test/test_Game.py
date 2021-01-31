import unittest
import json

from game import Game, PointIndexed, Field
from game_spec_validator import GameSpecValidator

with open('test/test_spec.json') as f:
    json_spec = json.load(f)

class Test_Game_init_from_spec(unittest.TestCase):

    def test_new_instance(self):
        game = Game.__new__(Game)
        self.assertIsInstance(game, Game)

    def test_grid_type_is_PointIndexed(self):
        game = Game.__new__(Game)
        game.grid = game._initialize_grid((4, 4))
        self.assertIsInstance(game.grid, PointIndexed)

    def test_grid_unit_is_Field(self):
        game = Game.__new__(Game)
        game.grid = game._initialize_grid((4, 4))
        self.assertIsInstance(game.grid[(0, 0)], Field)
    
    def test_initialize_pirates_casts_list_to_dict(self):
        game = Game.__new__(Game)
        pirates = game._initialize_pirates(
            [[1,1], [1,2], [2,2], [2,1]]
        )
        self.assertIsInstance(pirates, dict)

    def test_initialize_pirates_empty_dict(self):
        game = Game.__new__(Game)
        pirates = game._initialize_pirates({})
        self.assertEqual(pirates, {})

if __name__ == "__main__":
    unittest.main()