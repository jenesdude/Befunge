from typing import List
from funge98.funge98_exceptions import *


class FungeStack:
    """Class for stack of stacks.
    Every cell contains an int value from 0 to 255."""
    stack_stack: List[List[int]]
    stack: List[int]

    def __init__(self, dimension=2):
        self.stack_stack = [[]]
        self.stack = self.stack_stack[0]
        self.dimension = dimension

    def pop(self, n=0):
        """Popping a value. If negative n is popping, n elements are removed
        from the top of stack stack."""
        if n < 0:
            self.stack = self.stack[:-min(len(self.stack), n)]
        else:
            if self.stack:
                return self.stack.pop()
            else:
                return 0

    def store(self, value):
        self.stack.append(int(value, 16))

    def arithmetic(self, command):
        if command == "+":
            a = self.pop()
            b = self.pop()
            self.stack.append(a + b)
        elif command == "-":
            a = self.pop()
            b = self.pop()
            self.stack.append(a - b)
        elif command == "*":
            a = self.pop()
            b = self.pop()
            self.stack.append(a * b)
        elif command == "/":
            try:
                a = self.pop()
                b = self.pop()
                self.stack.append(a // b)
            except ZeroDivisionError:
                self.stack.append(0)
        elif command == "%":
            try:
                a = self.pop()
                b = self.pop()
                self.stack.append(a % b)
            except ZeroDivisionError:
                self.stack.append(0)
        elif command == "!":
            a = self.pop()
            if a == 0:
                self.stack.append(1)
            else:
                self.stack.append(0)
        elif command == "`":
            a = self.pop()
            b = self.pop()
            self.stack.append(1 if b > a else 0)
        else:
            raise IncorrectCommandError(command) from None

    def stack_manipulation(self):


    def stack_stack_manipulation(self, command):
        if command == "{":
            self.begin_block()
        elif command == "}":
            self.end_block()
        elif command == "u":
            self.stack_under_stack()
        else:
            raise IncorrectCommandError(command) from None

    def push(self, value):
        self.stack.append(value)

    def clear(self):
        self.stack = []

    def swap(self):
        if len(self.stack) > 1:
            self.stack[-1], self.stack[-2] = \
                self.stack[-2], self.stack[-1]
        else:
            self.stack.append(0)  # if there is one stack, push 0

    def begin_block(self):
        """Creates new stack of the top of FungeStack, then transfers n
        elements from SOSS to TOSS, then pushes ip (vector) into SOSS."""
        # TODO переписать, используя self.stack вместо self.stac[0] и self.stack_stack вместо self.stack
        ip = [self.pop() for i in range(self.dimension)]
        n = self.pop()
        self.stack.insert(0, [])
        if n > 0:
            if len(self.stack) > 1:
                if n <= len(self.stack[1]):
                    self.stack = self.stack[1][-n:]
                    self.stack[1] = self.stack[1][:-n] + ip
                else:
                    self.stack[0] = self.stack[1] +\
                                    [0] * (n - len(self.stack[1]))
                    self.stack[1] = ip
        elif n < 0:
            self.stack[1] += [0] * n
        else:
            self.stack[1] += ip

    def end_block(self):
        """Transfers n elements from TOSS to SOSS and pops entire TOSS,
        returns current ip as ip popped from SOSS"""
        # TODO переписать, используя self.stack вместо self.stac[0] и self.stack_stack вместо self.stack
        n = self.pop()
        if n > 0:
            if len(self.stack) > 1:
                ip = self.stack[1][:-self.dimension]
                self.stack[1] = self.stack[1][-self.dimension:]
                if n <= len(self.stack[0]):
                    self.stack[1] = self.stack[0][-n:]
                    self.stack = self.stack[1:]
                else:
                    self.stack[0] = self.stack[0] +\
                                    [0] * (n - len(self.stack[0]))
            else:
                return -1  # special code for reversing the flow
        elif n < 0:
            pass
        else:
            pass

    def stack_under_stack(self):
        # TODO написать
        pass

    operations = {
        r"0123456789abcdef": store,
        r"$:\n": stack_manipulation,
        r"{}u": stack_stack_manipulation,
        r"+-*/%!`:\$": arithmetic,
    }


class FungeSpace:
    """Class for Funge Space"""
    def __init__(self):
        self.stack = FungeStack(dimension=2)
        self.code_height = 0
        self.code_width = 0
        self.y = 0
        self.x = 0
        self.space = [" " * 256] * 256
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


class UnefungeSpace:
    """Class for Unefunge Space"""
    def __init__(self):
        self.stack = FungeStack(2)
        self.code_height = 0
        self.code_width = 0
        self.x = 0
        self.space = [" " * 256]
        self.move_direction = ">"
        self.string_mode = False


class TrefungeSpace:
    """Class for Trifunge Space"""
    pass
