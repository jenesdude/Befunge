from typing import List
from funge98_exceptions import *


class FungeStack:
    """Class for stack of stacks.
    Every cell contains an int value from 0 to 255."""
    stack_stack: List[List[int]]
    stack: List[int]

    def __init__(self, dimension=2):
        self.stack_stack = [[]]
        self.stack = self.stack_stack[0]
        self.dimension = dimension

    def pop(self):
        """Pop a value from TOSS (top of stack stack).
        If there is no value to return, then return 0."""
        if self.stack:
            return self.stack.pop()
        return 0

    def pop_n(self, n, reversed=False):
        """Pop n values from stack"""
        values = [self.stack.pop() for _ in range(n)]
        if reversed:
            return values[::-1]
        else:
            return values

    def pop_soss(self):
        """Pop a value from SOSS (second on stack stack).
        If there is no SOSS, pop 0."""
        if len(self.stack_stack) > 1:
            if self.stack_stack[1]:
                return self.stack_stack[1].pop()
        raise NoSOSSError from None

    def push(self, *values):
        for value in values:
            self.stack.append(value)

    def store(self, value):
        self.push(int(value, 16))

    def arithmetic(self, command):
        if command == "+":
            a = self.pop()
            b = self.pop()
            self.push(a + b)
        elif command == "-":
            a = self.pop()
            b = self.pop()
            self.push(a - b)
        elif command == "*":
            a = self.pop()
            b = self.pop()
            self.push(a * b)
        elif command == "/":
            try:
                a = self.pop()
                b = self.pop()
                self.push(a // b)
            except ZeroDivisionError:
                self.push(0)
        elif command == "%":
            try:
                a = self.pop()
                b = self.pop()
                self.push(a % b)
            except ZeroDivisionError:
                self.push(0)
        elif command == "!":
            a = self.pop()
            if a == 0:
                self.push(1)
            else:
                self.push(0)
        elif command == "`":
            a = self.pop()
            b = self.pop()
            self.push(1 if b > a else 0)
        else:
            raise IncorrectCommandError(command) from None

    def stack_manipulation(self, command):
        if command == "$":
            self.pop()
        elif command == ":":
            a = self.pop()
            self.push(a)
            self.push(a)
        elif command == "\\":
            a = self.pop()
            b = self.pop()
            self.push(a)
            self.push(b)
        elif command == "n":
            self.stack = []
        else:
            raise IncorrectCommandError(command) from None

    def stack_under_stack(self):
        count = self.pop()
        if len(self.stack_stack) < 2:
            raise NoSOSSError from None
        soss_elements = [self.pop_soss() for _ in range(count)]
        self.push(*soss_elements)

    operations = {
        "0123456789abcdef": store,
        "$:n\\": stack_manipulation,
        "u": stack_under_stack,
        "+-*/%!`": arithmetic,
    }


class FungeSpace:
    """Class for Funge Space"""
    def __init__(self, dimension):
        self.stack = FungeStack(dimension)
        self.dimension = dimension  # 1, 2, 3 for a specific Funge
        self.code_dimensions = []  # known dimensions for Lahey-Space impl.
        self.ip_pos = [0] * self.dimension  # origin
        self.delta = [1] + [0] * (self.dimension - 1)
        self.storage_offset = [0] * self.dimension
        self.space = None
        self.string_mode = False
        self.comment_mode = False

    @staticmethod
    def _read_source(mode="f", dimension=2, source=None):
        """Inner method for reading source. Either file in "f" mode
        or string, list of strings or list of lists of strings in "s" mode.
        Returns space and list of dimensions length according to dimenions"""
        if mode == "f":
            try:
                with open(source, "r", encoding="utf-8") as file:
                    if dimension == 1:
                        space = file.read().replace("\n", "")
                        return space, [len(space)]
                    elif dimension == 2:
                        space = file.read().split("\n")
                        max_x = max(map(lambda a: len(a), space))
                        return space, [max_x, len(space)]
                    elif dimension == 3:
                        pass
                        # TODO
                    else:
                        raise DimensionNotImplementedError(dimension) from None
            except FileNotFoundError:
                raise CodeFileNotFoundError from None
        elif mode == "s":
            if dimension == 1:
                if not isinstance(source, str):
                    raise CodeSourceInappropriateFormatError from None
                space = None
                # TODO
                pass
            elif dimension == 2:
                if not isinstance(source, list):
                    pass

    def stack_stack_manipulation(self, command):
        if command == "{":
            self.begin_block()
        elif command == "}":
            self.end_block()
        elif command == "u":
            self.stack.stack_under_stack()
        else:
            raise IncorrectCommandError(command) from None

    def begin_block(self):
        """Pop n-value from the TOSS. Create new TOSS.
        Transfer n elements from SOSS to TOSS, order is preserved.
        Push storage offset into SOSS, dimension-dependent.
        Change storage offset to the location to be executed next by IP."""
        n = self.stack.pop()
        if n > 0:
            toss = self.stack.pop_n(n, reversed=True)
        elif n < 0:
            toss = [0] * n
        else:
            toss = []
        self.stack.push(*self.storage_offset)
        self.storage_offset = list(
            map(lambda a, b: a + b, self.ip_pos, self.delta)
        )
        self.stack.stack_stack.insert(0, toss)

    def end_block(self):
        """Pop n-value from the TOSS.
        Pop storage offset from SOSS, dimension-dependent.
        Change storage offset to popped vector.
        Transfer n elements from TOSS to SOSS, order is preserved.
        Pop entire TOSS."""
        n = self.stack.pop()
        storage_offset = self.stack.pop_n(n, reversed=True)
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


class UnefungeSpace:
    """Class for Unefunge Space with Funge98 specification"""
    def __init__(self):
        super().__init__(1)
        self.space = [" " * 256]
        self.delta = [1]
        self.string_mode = False


class BefungeSpace(FungeSpace):
    """Class for Befunge Space with Funge98 specification"""
    def __init__(self):
        super().__init__(2)


class TrefungeSpace:
    """Class for Trefunge Space with Funge98 specification"""
    def __init__(self):
        super().__init__(3)

