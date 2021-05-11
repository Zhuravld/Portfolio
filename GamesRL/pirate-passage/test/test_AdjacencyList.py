import unittest
from utils import AdjacencyList, PointIndexed, Field


class Test_AdjacencyList(unittest.TestCase):
    def test_get_neighbours_returns_empty_list(self):
        self.AL_one_dim = AdjacencyList()

        self.assertEquals(self.AL_one_dim.get_neighbours(0), [])

    def test_insert_edge(self):
        self.AL = AdjacencyList()
        v1 = (0, 3, 2)
        v2 = (1, 3, 2)

        self.assertFalse(v1 in self.AL.get_neighbours(v2))
        self.assertFalse(v2 in self.AL.get_neighbours(v1))

        self.AL.insert_edge(e=(v1, v2))

        self.assertTrue(v1 in self.AL.get_neighbours(v2))
        self.assertTrue(v2 in self.AL.get_neighbours(v1))

    def test_are_adjacent(self):
        self.AL = AdjacencyList()
        v1 = (0, 3, 2)
        v2 = (1, 3, 2)
        self.AL.insert_edge(e=(v1, v2))

        self.assertTrue(self.AL.are_adjacent(v1, v2))
        self.assertTrue(self.AL.are_adjacent(v2, v1))

    def test_depth_first_search(self):
        self.AL = AdjacencyList()

        v1 = (0, 0)
        v2 = (0, 1)
        v3 = (0, 2)
        v4 = (1, 1)
        v5 = (2, 1)
        v6 = (3, 3)

        self.AL.insert_edge(e=(v1, v2))
        self.AL.insert_edge(e=(v2, v3))
        self.AL.insert_edge(e=(v2, v4))
        self.AL.insert_edge(e=(v3, v4))
        self.AL.insert_edge(e=(v4, v5))

        self.assertTrue(self.AL.depth_first_search(end=v5, start=v1))
        self.assertFalse(self.AL.depth_first_search(end=v6, start=v1))

    def test_init_from_grid_shape(self):
        self.AL = AdjacencyList(grid_shape=(2, 3), inaccessible=((0, 2), (1, 0)))

        self.assertEquals(
            self.AL.neighbours,
            {
                (0, 0): [(0, 1)],
                (0, 1): [(0, 0), (1, 1)],
                (1, 1): [(0, 1), (1, 2)],
                (1, 2): [(1, 1)],
            },
        )


if __name__ == "__main__":
    unittest.main()
