import pytest
from io import StringIO
from befunge import *
from befunge.interactive_befunge_grid import *
from befunge.interactive_exceptions import *


def test_grid_is_not_defined_error(monkeypatch):
    with pytest.raises(IAGridIsNotDefinedError):
        grid = IABefungeGrid()
        monkeypatch.setattr('sys.stdin', StringIO("\n"))
        grid.run()


def test_grid_is_not_rectangle_error(monkeypatch):
    with pytest.raises(CodeFileIsNotRectangleError):
        grid = IABefungeGrid()
        monkeypatch.setattr('sys.stdin', StringIO("123v\nv54<\n>>@\n"))
        grid.run()


def test_complete_grid_alteration_error(monkeypatch):
    with pytest.raises(CompleteIAGridAlterationError):
        grid = IABefungeGrid()
        monkeypatch.setattr('sys.stdin', StringIO(">>v@\n<<<^\n\n"))
        grid.run()
        monkeypatch.setattr('sys.stdin', StringIO("123@\n"))
        # grid.make_grid()
        grid.run()
