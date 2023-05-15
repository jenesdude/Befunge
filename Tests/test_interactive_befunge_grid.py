import pytest
from io import StringIO
from befunge import interactive_befunge_grid


def test_grid_from_user_input_one_row(monkeypatch):
    grid = interactive_befunge_grid.IABefungeGrid()
    monkeypatch.setattr('builtins.input', lambda: "123@\n")
    grid.run()
    assert grid.stack == [1, 2, 3]


def test_grid_many_rows(monkeypatch):
    grid = interactive_befunge_grid.IABefungeGrid()
    monkeypatch.setattr('sys.stdin', StringIO("123v\n @4<\n"))
    grid.run()
    assert grid.stack == [1, 2, 3, 4]
