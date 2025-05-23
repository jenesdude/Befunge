import pytest
from pathlib import Path
from befunge import befunge_grid, exceptions


def test_raise_code_file_not_found_error():
    with pytest.raises(exceptions.CodeFileNotFoundError):
        grid = befunge_grid.BefungeGrid()
        grid.set_grid("f", "nonexistent_file.txt")


def test_raise_code_file_is_out_of_bounds_error():
    with pytest.raises(exceptions.CodeFileIsOutOfBoundsError):
        source = Path("exception_width.txt")
        with open(source, "w") as file:
            file.write(" " * 100)
        grid = befunge_grid.BefungeGrid()
        grid.set_grid("f", source)
        source.unlink()
    with pytest.raises(exceptions.CodeFileIsOutOfBoundsError):
        source = Path("exception_height.txt")
        with open(source, "w") as file:
            file.write(" \n" * 100)
        grid = befunge_grid.BefungeGrid()
        grid.set_grid("f", source)
        source.unlink()


def test_raise_code_is_not_rectangle_error():
    with pytest.raises(exceptions.CodeFileIsNotRectangleError):
        source = Path("non_rectangle_file.txt")
        with open(source, "w") as file:
            file.write("                            >\n")
            file.write(">")
        grid = befunge_grid.BefungeGrid()
        grid.set_grid("f", source)
        source.unlink()


def test_grid_is_not_defined_error():
    with pytest.raises(exceptions.GridIsNotDefinedError):
        grid = befunge_grid.BefungeGrid()
        grid.run()


def test_raise_wrong_set_grid_mode_error_nonexistent_file():
    """Testing default mode 'f' — file with nonexistent_file"""
    with pytest.raises(exceptions.WrongSetGridModeError):
        grid = befunge_grid.BefungeGrid()
        grid.set_grid("nonexistent_file.txt")


def test_raise_wrong_set_grid_error_letter():
    """Testing nonexistent mode 'z'"""
    with pytest.raises(exceptions.WrongSetGridModeError):
        grid = befunge_grid.BefungeGrid()
        grid.set_grid("z", "any_file.txt")


def test_raise_code_source_is_not_string_list_error():
    """Testing string as an argument for 's' reading source mode"""
    with pytest.raises(exceptions.CodeSourceIsNotStringListError):
        grid = befunge_grid.BefungeGrid()
        grid.set_grid("s", "string, not list of strings")


def test_raise_code_source_if_empty_error():
    """Testing empty string as an argument for 's' reading source mode"""
    with pytest.raises(exceptions.CodeSourceIsEmptyError):
        grid = befunge_grid.BefungeGrid()
        grid.set_grid("s", [""])


def test_raise_not_enough_elements_in_stack_error():
    grid = befunge_grid.BefungeGrid()
    with pytest.raises(exceptions.NotEnoughElementsInStackError):
        grid.set_grid("s", ["|"])
        grid.run()
    with pytest.raises(exceptions.NotEnoughElementsInStackError):
        grid.set_grid("s", ["_"])
        grid.run()
