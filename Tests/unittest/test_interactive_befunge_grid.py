import unittest

from io import StringIO
from unittest.mock import patch
from befunge import interactive_befunge_grid


class TestIABefungeGrid(unittest.TestCase):
    @patch('sys.stdin', StringIO("123@\n"))
    def test_grid_from_user_input_one_row(self):
        grid = interactive_befunge_grid.IABefungeGrid()
        grid.run()
        assert grid.stack == [1, 2, 3]

    @patch('sys.stdin', StringIO("123v\n @4<\n"))
    def test_grid_many_rows(self):
        grid = interactive_befunge_grid.IABefungeGrid()
        grid.run()
        assert grid.stack == [1, 2, 3, 4]
