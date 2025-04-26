import unittest

from io import StringIO
from unittest.mock import patch
from befunge import interactive_befunge_grid, interactive_exceptions
from befunge import exceptions


class TestIAExceptions(unittest.TestCase):
    @patch('sys.stdin', StringIO("\n"))
    def test_grid_is_not_defined_error(self):
        with self.assertRaises(interactive_exceptions.IAGridIsNotDefinedError):
            grid = interactive_befunge_grid.IABefungeGrid()
            grid.run()

    @patch('sys.stdin', StringIO("123v\nv54<\n>>@\n"))
    def test_grid_is_not_rectangle_error(self):
        with self.assertRaises(exceptions.CodeFileIsNotRectangleError):
            grid = interactive_befunge_grid.IABefungeGrid()
            grid.run()

    def test_complete_grid_alteration_run_error(self):
        with self.assertRaises(
                interactive_exceptions.CompleteIAGridAlterationError
        ):
            grid = interactive_befunge_grid.IABefungeGrid()
            with patch('sys.stdin', new=StringIO(">>v@\n<<<^\n\n")):
                grid.run()
            with patch('sys.stdin', new=StringIO("123@\n")):
                grid.run()

    def test_complete_grid_alteration_make_error(self):
        with self.assertRaises(
                interactive_exceptions.CompleteIAGridAlterationError
        ):
            grid = interactive_befunge_grid.IABefungeGrid()
            with patch('sys.stdin', new=StringIO(">>v@\n<<<^\n\n")):
                grid.run()
            with patch('sys.stdin', new=StringIO("123@\n")):
                grid.make_grid()
