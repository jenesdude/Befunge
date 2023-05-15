"""Subclass for interactive befunge interpreter.
Stack contains only int numbers"""

from typing import List
from befunge.befunge_grid import BefungeGrid
from befunge.interactive_exceptions import *


class IABefungeGrid(BefungeGrid):
    """Class for interactive Befunge grid"""
    stack: List[int]

    def __init__(self):
        super().__init__()
        self.grid = []
        self.grid_complete = False

    def run(self, debug=False):
        """Endless loop of program interpretation
        If debug=True, every command prints:
         - current command,
         - coordinates,
         - string mode
         - full stack"""
        self.make_grid()
        while True:
            if self.evaluate(self.grid[self.y][self.x], debug):
                continue
            break

    def make_grid(self):
        """Method for creating and making the interactive grid.
        Every string is provided by user.
        If empty string is provided, the grid is complete."""
        row = input()
        if row:
            if not self.grid_complete:
                if self.code_width:
                    if len(row) == self.code_width:
                        self.grid.append(row)
                        self.code_height += 1
                    else:
                        raise CodeFileIsNotRectangleError
                else:
                    self.code_width = len(row)
                    self.grid.append(row)
                    self.code_height += 1
            else:
                raise CompleteIAGridAlterationError
        else:
            self.grid_complete = True
            if not self.grid:
                raise IAGridIsNotDefinedError

    def _move(self):
        """Inner method for moving over grid.
        If grid is not complete and moving over the hedge is needed,
        the program asks for user input"""
        if self.move_direction == "v":
            if not self.grid_complete:     # if grid is not complete
                self.make_grid()           # one row of code is required
            self.y = (self.y + 1) % self.code_height
        elif self.move_direction == ">":
            self.x = (self.x + 1) % self.code_width
        elif self.move_direction == "^":
            while not self.grid_complete:  # until grid is complete
                self.make_grid()           # ask for another row of code
            else:
                self.y = self.code_height - 1 if self.y == 0 else self.y - 1
        elif self.move_direction == "<":
            self.x = self.code_width - 1 if self.x == 0 else self.x - 1
        else:
            pass
