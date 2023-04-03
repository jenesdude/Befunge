class CodeFileNotFoundError(Exception):
    """Exception raised for code file is not found"""

    def __init__(self):
        self.message = "The Befunge code file is not found"
        super().__init__(self.message)


class CodeFileIsOutOfBoundsError(Exception):
    """Exception raised for code file width or height is out of 25×80 bounds"""

    def __init__(self):
        self.message = "The Befunge code file width or height is out of 25×80 bounds"
        super().__init__(self.message)


class CodeFileIsNotRectangleError(Exception):
    """Exception raised for non-rectangle code files"""

    def __init__(self):
        self.message = "The Befunge code file is not rectangle"
        super().__init__(self.message)


class BefungeError(Exception):
    """Base Exception for any Befunge errors"""

    def __init__(self, message, grid):
        command = grid.grid[grid.y][grid.x]
        super().__init__(message + " [ " + command + " ] at Y:" + str(grid.y) + ", X:" + str(grid.x))


class NotEnoughElementsInStackError(BefungeError):
    """Exception raised for executing commands that require more arguments than there are in stack"""

    def __init__(self, grid):
        self.message = "The stack doesn't have enough elements for command"
        super().__init__(self.message, grid)
