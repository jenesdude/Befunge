"""Interpreter for esoteric stack language befunge.
Stack contains only int numbers"""

from random import choice
from typing import List
from befunge.exceptions import *


class BefungeGrid:
    """Class for befunge grid"""
    stack: List[int]

    def __init__(self):
        self.code_height = 0
        self.code_width = 0
        self.y = 0
        self.x = 0
        self.grid = None
        self.stack = []
        self.move_direction = ">"
        self.string_mode = False

    @staticmethod
    def _read_source(mode="f", source=None):
        """Inner method for reading source. Either file or list of strings"""
        if mode == "f":
            try:
                with open(source, "r", encoding="utf-8") as file:
                    rows = file.read().split("\n")
                    height = len(rows)
                    width = len(rows[0])
            except FileNotFoundError:
                raise CodeFileNotFoundError from None
        elif mode == "s":
            if not isinstance(source, list):
                raise CodeSourceIsNotStringListError from None
            rows = source
            height = len(rows)
            width = len(rows[0])
        else:
            raise WrongSetGridModeError
        return rows, height, width

    def set_grid(self, mode="f", source=None):
        """Method for setting the grid.
        Mode 'f' is for reading file. Mode 's' is for list of strings.
        Method also resets y and x variables to zero.
        Code is any rectangular less or equal to 25×80 text block,
        looped in the shape of a torus."""
        rows, height, width = self._read_source(mode, source)
        if not width:
            raise CodeSourceIsEmptyError
        if height > 25 or width > 80:
            raise CodeFileIsOutOfBoundsError
        for row in rows:
            if len(row) != width:
                raise CodeFileIsNotRectangleError
        self.code_height = height
        self.code_width = width
        self.y = 0
        self.x = 0
        self.grid = rows
        self.stack = []

    def evaluate(self, command, debug):
        """Main method for evaluation code of befunge."""
        if debug:
            print("evaluate command [ {} ] at Y: {} X: {},"
                  " string mode: {}, stack: [ {} ]".format
                  (command,
                   str(self.y + 1),
                   str(self.x + 1),
                   str(self.string_mode),
                   ",".join(str(int(e)) for e in self.stack)))
        if self.string_mode:
            if command == '"':
                self.string_mode = False
            else:
                self.stack.append(ord(self.grid[self.y][self.x]))
        elif command in ">^<v|?#_| ":
            self._change_direction(command)
        elif command in r"0123456789+-*/%!`:\$":
            self._stack_operations(command)
        elif command == '"':
            self.string_mode = True
        elif command in ".,~&":
            self._input_output(command)
        elif command == "p":
            self._put()
        elif command == "g":
            self._get()
        elif command == "@":
            return False
        else:
            print(f"Invalid operand [ {command} ] "
                  f"at {self.y + 1} row, {self.x + 1} column")
            return False
        self._move()
        return True

    def run(self, debug=False):
        """Endless loop of program interpretation
        If debug=True, every command prints:
         - current command,
         - coordinates,
         - string mode
         - full stack"""
        if self.grid is None:
            raise GridIsNotDefinedError
        while True:
            if self.evaluate(self.grid[self.y][self.x], debug):
                continue
            break

    def _input_output(self, command):
        """Inner method for I/O operations"""
        if command == ".":
            print(str(self.stack.pop()) + " ", end='')
        elif command == ",":
            print(chr(self.stack.pop()), end='')
        elif command == "&":
            self.stack.append(int(input()))
        else:
            input_string = ""
            while not input_string:
                input_string = input()
            self.stack.append(ord(input_string[0]))

    def _put(self):
        """Inner method for stack 'put' command.
        Popping y, x and value from stack, changing the character at y, x
        to the character with ASCII value v, taking numeration start on 1."""
        try:
            get_y = int(self.stack.pop())
            get_x = int(self.stack.pop())
            value = int(self.stack.pop())
            left_part = self.grid[get_y - 1][:get_x - 1]
            right_part = self.grid[get_y - 1][get_x:]
            self.grid[get_y - 1] = left_part + chr(value) + right_part
        except IndexError:
            self.grid[0] = "0" + self.grid[0][1:]

    def _get(self):
        """Inner method for stack 'get' command.
        Get value by top two coordinates from stack"""
        try:
            get_y = self.stack.pop()
            get_x = self.stack.pop()
            self.stack.append(ord(self.grid[get_y][get_x]))
        except IndexError:
            self.stack.append(0)

    def _stack_operations(self, command):
        """Inner method for any stack operations"""
        if command in "0123456789":
            self.stack.append(int(command))
        elif command == "+":
            try:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(a + b)
            except IndexError:
                self.stack.append(0)
        elif command == "-":
            try:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(a - b)
            except IndexError:
                self.stack.append(0)
        elif command == "*":
            try:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(a * b)
            except IndexError:
                self.stack.append(0)
        elif command == "/":
            try:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(a // b)
            except IndexError:
                self.stack.append(0)
            except ZeroDivisionError:
                self.stack.append(0)
        elif command == "%":
            try:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(a % b)
            except IndexError:
                self.stack.append(0)
            except ZeroDivisionError:
                self.stack.append(0)
        elif command == "!":
            try:
                a = self.stack.pop()
                self.stack.append(0 if a else 1)
            except IndexError:
                self.stack.append(0)
        elif command == "`":
            try:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(1 if b > a else 0)
            except IndexError:
                self.stack.append(0)
        elif command == ":":
            try:
                self.stack.append(self.stack[-1])
            except IndexError:
                self.stack.append(0)
                self.stack.append(0)
        elif command == "\\":
            try:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(a)
                self.stack.append(b)
            except IndexError:
                self.stack.append(0)
                self.stack.append(0)
        elif command == "$":
            try:
                self.stack.pop()
            except IndexError:
                pass

    def _change_direction(self, command):
        """Inner method for changing move direction"""
        if command in ">v<^":
            self.move_direction = command
        elif command == "?":
            self.move_direction = choice(">v<^")
        elif command == "|":
            try:
                value = self.stack.pop()
                self.move_direction = "^" if value else "v"
            except IndexError:
                raise NotEnoughElementsInStackError(self) from None
        elif command == "_":
            try:
                value = self.stack.pop()
                self.move_direction = "<" if value else ">"
            except IndexError:
                raise NotEnoughElementsInStackError(self) from None
        elif command == "#":
            self._move()
        else:
            pass

    def _move(self):
        """Inner method for moving over grid"""
        if self.move_direction == "v":
            self.y = (self.y + 1) % self.code_height
        elif self.move_direction == ">":
            self.x = (self.x + 1) % self.code_width
        elif self.move_direction == "^":
            self.y = self.code_height - 1 if self.y == 0 else self.y - 1
        elif self.move_direction == "<":
            self.x = self.code_width - 1 if self.x == 0 else self.x - 1
        else:
            pass
