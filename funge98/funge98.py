from typing import List
from funge98.funge98_exceptions import *


class FungeStack:
    """Class for stack of stacks.
    Every cell contains an int value from 0 to 255."""
    stack: List[List[int]]

    def __init__(self, dimension=2):
        self.stack = [[]]
        self.dimension = dimension

    def pop(self, n=0):
        """Popping a value. If negative n is popping, n elements are removed
        from the top of stack stack."""
        if n < 0:
            self.stack[0] = self.stack[0][:-min(len(self.stack[0]), n)]
        else:
            if self.stack[0]:
                return self.stack[0].pop()
            else:
                return 0

    def push(self, value):
        self.stack[0].append(value)

    def clear(self):
        self.stack[0] = []

    def swap(self):
        if len(self.stack[0]) > 1:
            self.stack[0][-1], self.stack[0][-2] = \
                self.stack[0][-2], self.stack[0][-1]
        else:
            self.stack[0].append(0)  # if there is one stack, push 0

    def begin_block(self, space, ip):
        """Creates new stack of the top of FungeStack, then transfers n
        elements from SOSS to TOSS, then pushes ip (vector) into SOSS."""
        if len(ip) != self.dimension:
            raise IPHasInWrongDimensionError(space)
        n = self.pop()
        self.stack.insert(0, [])
        if n > 0:
            if len(self.stack) > 1:
                if n <= len(self.stack[1]):
                    self.stack[0] = self.stack[1][-n:]
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
