class CodeFileNotFoundError(Exception):
    """Exception raised for code file is not found"""

    def __init__(self):
        self.message = "The befunge code file is not found"
        super().__init__(self.message)


class CodeFileIsOutOfBoundsError(Exception):
    """Exception raised for code file width or height is out of 25×80 bounds"""

    def __init__(self):
        self.message = "The befunge code file width or height is out of 25×80 bounds"
        super().__init__(self.message)


class CodeFileIsNotRectangleError(Exception):
    """Exception raised for non-rectangle code files"""

    def __init__(self):
        self.message = "The befunge code file is not rectangle"
        super().__init__(self.message)


class GridIsNotDefinedError(Exception):
    """Exception raised for executing any command without assigning grid"""

    def __init__(self):
        self.message = "The grid is not defined"
        super().__init__(self.message)


class WrongSetGridModeError(Exception):
    """Exception raised for using wrong setting grid mode"""

    def __init__(self):
        self.message = "The grid setting mode is wrong, should be 'f' for files or 's' for string list"
        super().__init__(self.message)


class BefungeError(Exception):
    """Base Exception for any befunge errors"""

    def __init__(self, message, grid):
        command = grid.grid[grid.y][grid.x]
        super().__init__(message + " [ " + command + " ] at Y:" + str(grid.y) + ", X:" + str(grid.x))


class NotEnoughElementsInStackError(BefungeError):
    """Exception raised for executing commands that require more arguments than there are in stack"""

    def __init__(self, grid):
        self.message = "The stack doesn't have enough elements for command"
        super().__init__(self.message, grid)
