import unittest

from game import PointIndexed

class Test_PointIndexed(unittest.TestCase):
    two_dim = PointIndexed([
        [1, 3, 5],
        [2, 4, 6]
    ])
    three_dim = PointIndexed([
        [
            [1, 2],
            [3, 4]
        ],
        [
            [5, 6],
            [7, 8]
        ]
    ])

    def test_tuple_indexer(self):
        self.assertEqual(
            self.two_dim[(1, 2)], 6
        )

    def test_list_indexer(self):
        self.assertEqual(
            self.two_dim[[1, 2]], 6
        )

    def test_range_indexer(self):
        self.assertEqual(
            self.two_dim[range(1, 3)], 6
        )

    def test_three_dim(self):
        self.assertEqual(
            self.three_dim[(1, 1, 0)], 7
        )

if __name__ == "__main__":
    unittest.main()