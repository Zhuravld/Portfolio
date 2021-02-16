import unittest
import json

from game import Game
from game_spec_validator import GameSpecValidator

with open('test/test_spec.json') as f:
    json_spec = json.load(f)

class Test_Game_init_from_spec(unittest.TestCase):

    def test_new_instance(self):
        game = Game.__new__(Game)
        self.assertIsInstance(game, Game)

    def test_validate_spec(self):
        game = Game.__new__(Game)
        self.assertEquals(
            [], GameSpecValidator().validate_spec(json_spec)
        )

if __name__ == "__main__":
    unittest.main()