"""Interpreter for esoteric stack language Funge-98"""

from abc import ABC, abstractmethod
from typing import List
from funge98.exceptions import *


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
        else:
            raise NoTOSSError from None

    def pop_n(self, n, reverse=False):
        """Pop n values from stack"""
        values = [self.stack.pop() for _ in range(n)]
        if reverse:
            return values[::-1]
        else:
            return values

    def pop_stack(self):
        """Pop entire TOSS."""
        if self.stack_stack:
            self.stack_stack.pop()
        else:
            raise NoTOSSError from None

    def pop_soss(self):
        """Pop a value from SOSS (second on stack stack).
        If there is no SOSS, pop 0."""
        if len(self.stack_stack) > 1:
            if self.stack_stack[1]:
                return self.stack_stack[1].pop()
        raise NoSOSSError from None

    def push(self, *values):
        if self.stack:
            for value in values:
                self.stack.append(value)
        else:
            raise NoTOSSError from None

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
            raise IncorrectCommandError(command, self) from None

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
            raise IncorrectCommandError(command, self) from None

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


class FungeSpace(ABC):
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

    @abstractmethod
    def __getitem__(self, key: int | tuple):
        pass

    def getitem(self, key: int | tuple):
        # TODO may be check_getitem
        if not self.space:
            raise SpaceIsNotDefinedError from None
        if isinstance(key, tuple):
            if len(key) != self.dimension:
                raise IncorrectPositionError(key, self.space) from None
        elif isinstance(key, int):
            if key < 0:
                raise IncorrectPositionError(key, self.space) from None
        else:
            raise IncorrectPositionError(key, self.space) from None
        self.__getitem__(key)

    @staticmethod
    @abstractmethod
    def _read_source(mode="f", source=None) -> (str, int):
        """Inner method for reading source. Either file in "f" mode
        or string, list of strings or list of lists of strings in "s" mode.
        Returns space and list of dimensions length according to dimenions"""

    def set_space(self, mode="f", source=None):
        """Method for setting the space."""
        source_code, dimensions = self._read_source(mode, source)
        if 0 in dimensions:
            raise CodeSourceIsEmptyError from None
        if max(dimensions) > 256:
            raise CodeFileIsOutOfBoundsError from None
        self.space = source_code
        self.code_dimensions = dimensions

    @abstractmethod
    def _move(self):
        """Inner method for moving over space"""

    @abstractmethod
    def _change_direction(self, command):
        """Inner method for changing move direction"""

    def reflect(self):
        self.delta = list(map(lambda a: a * -1, self.delta))

    def _stack_stack_manipulation(self, command):
        try:
            if command == "{":
                self.begin_block()
            elif command == "}":
                self.end_block()
            elif command == "u":
                self.stack.stack_under_stack()
        except NoTOSSError or NoSOSSError:
            self.reflect()
        else:
            raise IncorrectCommandError(command, self) from None

    def begin_block(self):
        """Pop n-value from the TOSS. Create new TOSS.
        Transfer n elements from SOSS to TOSS, order is preserved.
        Push storage offset into SOSS, dimension-dependent.
        Change storage offset to the location to be executed next by IP."""
        n = self.stack.pop()
        if n > 0:
            new_toss = self.stack.pop_n(n, reverse=True)
        elif n < 0:
            new_toss = [0] * n
        else:
            new_toss = []
        self.stack.push(*self.storage_offset)
        self.storage_offset = list(
            map(lambda a, b: a + b, self.ip_pos, self.delta)
        )
        self.stack.stack_stack.append(new_toss)

    def end_block(self):
        """Pop n-value from the TOSS.
        Pop storage offset from SOSS, dimension-dependent.
        Change storage offset to popped vector.
        If n > 0, transfer n elements from TOSS to SOSS, order is preserved.
        If n < 0, pop n elements from SOSS.
        If n = 0, transfer 0 elements.
        Then pop entire TOSS."""
        n = self.stack.pop()
        self.storage_offset = self.stack.pop_n(self.dimension, reverse=True)
        values = self.stack.pop_n(n, reverse=True)
        self.stack.pop_stack()
        if n > 0:
            self.stack.push(*values)
        elif n < 0:
            self.stack.pop_n(n)
        else:
            return

    def evaluate(self, command, debug):
        """Main method for evaluation code of Funge-98.
        If debug=True, every evaluation prints:
         - current command,
         - instruction pointer's position,
         - dimensions,
         - delta to instruction pointer,
         - current storage offset,
         - string mode,
         - comment mode,
         - full stack"""
        if debug:
            print("Evaluate command [ {} ] at [ {} ] ({} dimension);"
                  "delta [ {} ]; storage offset: {};"
                  "string mode: {}; comment mode: {}; stack: {}".format
                  (command,
                   ", ".join(map(str, self.ip_pos)),
                   self.dimension,
                   ", ".join(map(str, self.delta)),
                   self.storage_offset,
                   self.string_mode,
                   self.comment_mode,
                   self.stack))
        if self.string_mode:
            if command == '"':
                self.string_mode = False
            elif command == " ":
                pass
            else:
                self.stack.push(command)
        elif self.comment_mode:
            if command == ";":
                self.comment_mode = False
            else:
                pass
        elif command in ">^<v|_?#|[]hjlmrvwx ":
            self._change_direction(command)
        elif command in "{}u":
            self._stack_stack_manipulation(command)
        elif command == "@q":
            return False
        else:
            raise NotImplementedCommandError(command, self)
        self._move()
        return True

    def run(self, debug=False):
        """Endless loop of Funge-98 program interpretation"""
        if self.space is None:
            raise SpaceIsNotDefinedError from None
        while True:
            if self.evaluate(self.space[self.ip_pos], debug):
                continue
            break


class UnefungeSpace(FungeSpace):
    """Class for Unefunge Space with Funge-98 specification"""
    def __init__(self):
        super().__init__(1)
        self.space = " " * 256

    def __getitem__(self, key: int):
        self.getitem(key)
        return self.space[key]

    @staticmethod
    def _read_source(mode="f", source=None):
        """Inner method for reading source.
        Source is either file in "f" mode or string in "s" mode.
        Return space and its maximum dimensions"""
        if mode == "f":
            try:
                with open(source, "r", encoding="utf-8") as file:
                    space = file.read().replace("\n", "")
                    return space, len(space)
            except FileNotFoundError:
                raise CodeFileNotFoundError from None
        elif mode == "s":
            if not isinstance(source, str):
                raise CodeSourceInappropriateFormatError from None
            return source, [len(source)]
        else:
            raise SetSpaceWrongModeError(mode) from None

    def _move(self):
        pass

    def _change_direction(self, command):
        pass


class BefungeSpace(FungeSpace):
    """Class for Befunge Space with Funge-98 specification"""
    def __init__(self):
        super().__init__(2)
        self.space = [" " * 256] * 256

    def __getitem__(self, key: tuple[int] | list[int]):
        self.getitem(key)
        return self.space[key[0]][key[1]]

    @staticmethod
    def _read_source(mode="f", source=None):
        dimensions = [0, 0]
        if mode == "f":
            try:
                with open(source, "r", encoding="utf-8") as file:
                    space = file.read().split("\n")
                    dimensions[0] = max(len(row) for row in space)
                    dimensions[1] = len(space)
                    return space, dimensions
            except FileNotFoundError:
                raise CodeFileNotFoundError from None
        elif mode == "s":
            if not isinstance(source, list):
                raise CodeSourceInappropriateFormatError from None
            dimensions[0] = max(len(row) for row in source)
            dimensions[1] = len(source)
            return source, dimensions
        else:
            raise SetSpaceWrongModeError(mode) from None

    def _move(self):
        pass

    def _change_direction(self, command):
        pass


class TrefungeSpace(FungeSpace):
    """Class for Trefunge Space with Funge-98 specification"""
    def __init__(self):
        super().__init__(3)
        self.space = [" " * 256] * 256

    def __getitem__(self, key: tuple[int] | list[int]):
        self.getitem(key)
        return self.space[key[0]][key[1]][key[0]]

    @staticmethod
    def _read_source(mode="f", source=None):
        dimensions = [0, 0, 0]
        if mode == "f":
            try:
                with open(source, "r", encoding="utf-8") as file:
                    layers = file.read().split("\n\n")
                    space = [layer.split("\n") for layer in layers]
                    dimensions[0] = max(
                        max(len(row) for row in layer)
                        for layer in space)
                    dimensions[1] = max(len(layer) for layer in space)
                    dimensions[2] = len(space)
                    return space, dimensions
            except FileNotFoundError:
                raise CodeFileNotFoundError from None
        elif mode == "s":
            if not isinstance(source, str):
                raise CodeSourceInappropriateFormatError from None
            return source, len(source)
        else:
            raise SetSpaceWrongModeError(mode) from None

    def _move(self):
        pass

    def _change_direction(self, command):
        pass
