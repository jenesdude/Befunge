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

    def begin_block(self):
        """Pop n-value from the TOSS. Create new TOSS.
        Transfer n elements from SOSS to TOSS, order is preserved.
        Push storage offset into SOSS, dimension-dependent.
        Change storage offset to the location to be executed next by IP."""
        # TODO переписать, используя self.stack вместо self.stac[0] и self.stack_stack вместо self.stack
        n = self.pop()
        # ip = [self.pop() for i in range(self.dimension)]
        self.stack_stack.insert(0, [])
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
            self.stack_stack[1] += [0] * n
        else:
            self.stack_stack[1] +=

    def end_block(self):
        """Pop n-value from the TOSS.
        Pop storage offset from SOSS, dimension-dependent.
        Change storage offset to popped vector.
        Transfer n elements from TOSS to SOSS, order is preserved.
        Pop entire TOSS."""
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
        "0123456789abcdef": store,
        "$:n\\": stack_manipulation,
        "{}u": stack_stack_manipulation,
        "+-*/%!`": arithmetic,
    }


class FungeSpace:
    """Class for Funge Space"""
    def __init__(self, dimension):
        self.stack = FungeStack(dimension)
        self.dimension = dimension  # 1, 2, 3 for a specific Funge
        self.code_dimensions = []  # known dimensions for Lahey-Space impl.
        self.coords = [0] * self.dimension  # origin
        self.motion_vector = [1] + [0] * (self.dimension - 1)
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
