import pytest
from io import StringIO
from befunge import interactive_befunge_grid, interactive_exceptions
from befunge import exceptions


def test_grid_is_not_defined_error(monkeypatch):
    with pytest.raises(interactive_exceptions.IAGridIsNotDefinedError):
        grid = interactive_befunge_grid.IABefungeGrid()
        monkeypatch.setattr('sys.stdin', StringIO("\n"))
        grid.run()


def test_grid_is_not_rectangle_error(monkeypatch):
    with pytest.raises(exceptions.CodeFileIsNotRectangleError):
        grid = interactive_befunge_grid.IABefungeGrid()
        monkeypatch.setattr('sys.stdin', StringIO("123v\nv54<\n>>@\n"))
        grid.run()


def test_complete_grid_alteration_run_error(monkeypatch):
    with pytest.raises(interactive_exceptions.CompleteIAGridAlterationError):
        grid = interactive_befunge_grid.IABefungeGrid()
        monkeypatch.setattr('sys.stdin', StringIO(">>v@\n<<<^\n\n"))
        grid.run()
        monkeypatch.setattr('sys.stdin', StringIO("123@\n"))
        grid.run()


def test_complete_grid_alteration_make_error(monkeypatch):
    with pytest.raises(interactive_exceptions.CompleteIAGridAlterationError):
        grid = interactive_befunge_grid.IABefungeGrid()
        monkeypatch.setattr('sys.stdin', StringIO(">>v@\n<<<^\n\n"))
        grid.run()
        monkeypatch.setattr('sys.stdin', StringIO("123@\n"))
        grid.make_grid()
