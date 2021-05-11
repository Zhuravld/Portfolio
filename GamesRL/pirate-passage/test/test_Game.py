import unittest

from game import Game
from game_spec_validator import GameSpecValidator

test_spec = {
    "shape": [4, 4],
    "start": [0, 0],
    "goal": [3, 3],
    "inaccessible": [[2, 1], [1,2]],
    "pirate_routes": {
        "0": [[1,1], [1,2], [2,2], [2,1]]
    }
}
class Test_Game_init_from_spec(unittest.TestCase):
    def test_new_instance(self):
        game = Game.__new__(Game)
        self.assertIsInstance(game, Game)

    def test_validate_spec(self):
        game = Game.__new__(Game)
        self.assertEqual([], GameSpecValidator().validate_spec(test_spec))


if __name__ == "__main__":
    unittest.main()
