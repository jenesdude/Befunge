import unittest
from pathlib import Path
from befunge import befunge_grid, exceptions


class TestExceptions(unittest.TestCase):
    def test_raise_code_file_not_found_error(self):
        with self.assertRaises(exceptions.CodeFileNotFoundError):
            grid = befunge_grid.BefungeGrid()
            grid.set_grid("f", "nonexistent_file.txt")

    def test_raise_code_file_is_out_of_bounds_error(self):
        with self.assertRaises(exceptions.CodeFileIsOutOfBoundsError):
            grid = befunge_grid.BefungeGrid()
            source = Path("exception_width.txt")
            grid.set_grid("f", source)
        with self.assertRaises(exceptions.CodeFileIsOutOfBoundsError):
            grid = befunge_grid.BefungeGrid()
            source = Path("exception_height.txt")
            grid.set_grid("f", source)

    def test_raise_code_is_not_rectangle_error(self):
        with self.assertRaises(exceptions.CodeFileIsNotRectangleError):
            grid = befunge_grid.BefungeGrid()
            source = Path("non_rectangle_file.txt")
            grid.set_grid("f", source)

    def test_grid_is_not_defined_error(self):
        with self.assertRaises(exceptions.GridIsNotDefinedError):
            grid = befunge_grid.BefungeGrid()
            grid.run()

    def test_raise_wrong_set_grid_mode_error_nonexistent_file(self):
        """Testing default mode 'f' — file with nonexistent_file"""
        with self.assertRaises(exceptions.WrongSetGridModeError):
            grid = befunge_grid.BefungeGrid()
            grid.set_grid("nonexistent_file.txt")

    def test_raise_wrong_set_grid_error_letter(self):
        """Testing nonexistent mode 'z'"""
        with self.assertRaises(exceptions.WrongSetGridModeError):
            grid = befunge_grid.BefungeGrid()
            grid.set_grid("z", "any_file.txt")

    def test_raise_code_source_is_not_string_list_error(self):
        """Testing string as an argument for 's' reading source mode"""
        with self.assertRaises(exceptions.CodeSourceIsNotStringListError):
            grid = befunge_grid.BefungeGrid()
            grid.set_grid("s", "string, not list of strings")

    def test_raise_code_source_if_empty_error(self):
        """Testing empty string as an argument for 's' reading source mode"""
        with self.assertRaises(exceptions.CodeSourceIsEmptyError):
            grid = befunge_grid.BefungeGrid()
            grid.set_grid("s", [""])

    def test_raise_not_enough_elements_in_stack_error(self):
        grid = befunge_grid.BefungeGrid()
        with self.assertRaises(exceptions.NotEnoughElementsInStackError):
            grid.set_grid("s", ["|"])
            grid.run()
        with self.assertRaises(exceptions.NotEnoughElementsInStackError):
            grid.set_grid("s", ["_"])
            grid.run()
