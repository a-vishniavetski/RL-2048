# NOT UPDATED TO THE CURRENT API

import unittest
import numpy as np

from engine import move_left, move_right, move_up, move_down


class TestMoves(unittest.TestCase):

    def setUp(self):
        self.board = np.array(
            [
                [2, 2, 4, 4],
                [2, 0, 4, 4],
                [0, 2, 4, 2],
                [2, 2, 4, 4],
            ]
        )
        return super().setUp()

    def tearDown(self):
        self.board = np.array(
            [
                [2, 2, 4, 4],
                [2, 0, 4, 4],
                [0, 2, 4, 2],
                [2, 2, 4, 4],
            ]
        )
        return super().tearDown()

    def test_move_left(self):
        move_left(self.board)

        expected = np.array(
            [
                [4, 8, 0, 0],
                [2, 8, 0, 0],
                [2, 4, 2, 0],
                [4, 8, 0, 0],
            ]
        )

        np.testing.assert_array_equal(self.board, expected)

    def test_move_right(self):
        move_right(self.board)

        expected = np.array(
            [
                [0, 0, 4, 8],
                [0, 0, 2, 8],
                [0, 2, 4, 2],
                [0, 0, 4, 8],
            ]
        )

        np.testing.assert_array_equal(self.board, expected)

    def test_move_down(self):
        move_down(self.board)

        expected = np.array(
            [
                [0, 0, 0, 0],
                [0, 0, 0, 8],
                [2, 2, 8, 2],
                [4, 4, 8, 4],
            ]
        )

        np.testing.assert_array_equal(self.board, expected)

    def test_move_up(self):
        move_up(self.board)

        expected = np.array(
            [
                [4, 4, 8, 8],
                [2, 2, 8, 2],
                [0, 0, 0, 4],
                [0, 0, 0, 0],
            ]
        )

        np.testing.assert_array_equal(self.board, expected)


if __name__ == "__main__":
    unittest.main()
