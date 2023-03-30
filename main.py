"""Interpreter for esoteric stack language Befunge.
Stack contains only int numbers"""

from random import choice
from typing import List


class BefungeGrid:
    """Class for Befunge grid"""
    stack: List[int]

    def __init__(self, height, width, grid):
        self.code_height = height
        self.code_width = width
        self.x = 0
        self.y = 0
        self.grid = grid
        self.stack = []
        self.move_direction = ">"
        self.string_mode = False

    def evaluate(self, command, debug):
        """Main method for evaluation code of Befunge.
        Code is any rectangular less or equal to 25×80 text block"""
        if debug:
            print("evaluate command [", command, "] Y:", self.y + 1, "X:", self.x + 1,
                  "string mode:", self.string_mode,
                  "stack: [", ",".join(chr(e) for e in self.stack), "]")
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
            print("Invalid operand [", command, "] at", self.y + 1, "row,", self.x + 1, "column")
            return False
        self._move()
        return True

    def run(self, debug=False):
        """Endless loop of program interpretation
        If debug=True, every command prints current command, coordinates, string mode and full stack"""
        while True:
            if self.evaluate(self.grid[self.y][self.x], debug):
                continue
            else:
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
        """Inner method for putting value from top two coordinates from stack and a value"""
        try:
            get_y = self.stack.pop()
            get_x = self.stack.pop()
            value = self.stack.pop()
            self.grid[get_y - 1][get_x - 1] = chr(value)
        except IndexError:
            self.grid[0][0] = chr(0)

    def _get(self):
        """Inner method for getting value from top two coordinates from stack"""
        try:
            get_y = self.stack.pop()
            get_x = self.stack.pop()
            self.stack.append(self.grid[get_y - 1][get_x - 1])
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
                print("The stack doesn't have enough elements for |")
        elif command == "_":
            try:
                value = self.stack.pop()
                self.move_direction = "<" if value else ">"
            except IndexError:
                print("The stack doesn't have enough elements for _")
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


def read_program(file_name):
    """Function for reading Befunge source file
    Problems indicated with 0 return code"""
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            rows = file.read().split("\n")
            height = len(rows)
            if height > 25:
                return 3, "Количество строк кода больше 25"
            width = len(rows[0])
            if width > 80:
                return 4, "Количество столбцов кода больше 80"
            for row in rows:
                if len(row) != width:
                    return 2, "Код не является прямоугольным полем"
            return 0, height, width, rows
    except FileNotFoundError:
        return 1, "Файл кода отсутствует"


def main():
    program_text = read_program(r"Scripts\hello_world.txt")
    # program_text = read_program(r"Scripts\loop.txt")
    # program_text = read_program(r"Scripts\cat.txt")
    # program_text = read_program(r"Scripts\exception_width.txt")
    # program_text = read_program(r"Scripts\exception_height.txt")
    if program_text[0]:
        print(program_text[1])
    else:
        grid = BefungeGrid(*program_text[1:])
        grid.run()
        # grid.run(True)


if __name__ == "__main__":
    main()
