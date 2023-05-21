class GridAssignmentError(Exception):
    """Parent exception for all grid assignments errors"""

    def __init__(self, message):
        self.message = "Grid assignment isn't correct.\n" + message
        super().__init__(self.message)


class WrongSetGridModeError(GridAssignmentError):
    """Exception raised for using wrong setting grid mode"""

    def __init__(self):
        self.message = "The grid setting mode is wrong, should be" \
                       "'f' for files or 's' for string list"
        super().__init__(self.message)


class CodeFileIsOutOfBoundsError(GridAssignmentError):
    """Exception raised for code file width or height is out of 25×80 bounds"""

    def __init__(self):
        self.message = "The befunge code file width or height" \
                       "is out of 25×80 bounds"
        super().__init__(self.message)


class CodeFileIsNotRectangleError(GridAssignmentError):
    """Exception raised for non-rectangle code files"""

    def __init__(self):
        self.message = "The befunge code file is not rectangle"
        super().__init__(self.message)


class GridFileAssignmentError(GridAssignmentError):
    """Parent exception for assignment grid from a file"""

    def __init__(self, message):
        self.message = "Assignment from file mode.\n" + message
        super().__init__(self.message)


class CodeFileNotFoundError(GridFileAssignmentError):
    """Exception raised for code file is not found"""

    def __init__(self):
        self.message = "The befunge code file is not found"
        super().__init__(self.message)


class GridStringAssignmentError(GridAssignmentError):
    """Parent exception for assignment grid from a list of strings"""

    def __init__(self, message):
        self.message = "Assignment from string mode.\n" + message
        super().__init__(self.message)


class CodeSourceIsEmptyError(GridAssignmentError):
    """Exception raised for any input other than list of strings
    while reading source in 's' mode"""

    def __init__(self):
        self.message = "Code source contains empty string"
        super().__init__(self.message)


class CodeSourceIsNotStringListError(GridStringAssignmentError):
    """Exception raised for any input other than list of strings
    while reading source in 's' mode"""

    def __init__(self):
        self.message = "Code source is not list of string for mode 's'"
        super().__init__(self.message)


class GridIsNotDefinedError(Exception):
    """Exception raised for executing any command without assigning grid"""

    def __init__(self):
        self.message = "The grid is not defined"
        super().__init__(self.message)


class BefungeError(Exception):
    """Base Exception for any befunge errors"""

    def __init__(self, message, grid):
        command = grid.grid[grid.y][grid.x]
        super().__init__(f"{message} [ {command} ] at Y: {str(grid.y)},"
                         f"X:{str(grid.x)}")


class NotEnoughElementsInStackError(BefungeError):
    """Exception raised for executing commands
    that require more arguments than there are in stack"""

    def __init__(self, grid):
        self.message = "The stack doesn't have enough elements for command"
        super().__init__(self.message, grid)
