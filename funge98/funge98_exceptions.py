class SpaceAssignmentError(Exception):
    """Parent exception for all space assignments errors"""

    def __init__(self, message):
        self.message = "Space assignment isn't correct.\n" + message
        super().__init__(self.message)


class WrongSetSpaceModeError(SpaceAssignmentError):
    """Exception raised for using wrong setting space mode"""

    def __init__(self):
        self.message = "The space setting mode is wrong, should be" \
                       "'f' for files or 's' for string list"
        super().__init__(self.message)


class CodeFileIsOutOfBoundsError(SpaceAssignmentError):
    """Exception raised for code file width or height is more than 256"""

    def __init__(self):
        self.message = "The Funge-98 code file width or height" \
                       "is out of 256×256 bounds"
        super().__init__(self.message)


class SpaceFileAssignmentError(SpaceAssignmentError):
    """Parent exception for assignment space from a file"""

    def __init__(self, message):
        self.message = "Assignment from file mode.\n" + message
        super().__init__(self.message)


class CodeFileNotFoundError(SpaceFileAssignmentError):
    """Exception raised for code file is not found"""

    def __init__(self):
        self.message = "The Funge-98 code file is not found"
        super().__init__(self.message)


class SpaceStringAssignmentError(SpaceAssignmentError):
    """Parent exception for assignment space from a list of strings"""

    def __init__(self, message):
        self.message = "Assignment from string mode.\n" + message
        super().__init__(self.message)


class CodeSourceIsEmptyError(SpaceStringAssignmentError):
    """Exception raised for any input other than list of strings
    while reading source in 's' mode"""

    def __init__(self):
        self.message = "Code source contains empty string"
        super().__init__(self.message)


class CodeSourceIsNotStringListError(SpaceStringAssignmentError):
    """Exception raised for any input other than list of strings
    while reading source in 's' mode"""

    def __init__(self):
        self.message = "Code source is not list of string for mode 's'"
        super().__init__(self.message)


class SpaceIsNotDefinedError(Exception):
    """Exception raised for executing any command without assigning space"""

    def __init__(self):
        self.message = "The Funge-98 space is not defined"
        super().__init__(self.message)


class FungeError(Exception):
    """Base Exception for any Funge-98 errors"""

    def __init__(self, message, space):
        command = space.space[space.y][space.x]
        super().__init__(f"{message} [ {command} ] at Y: {str(space.y)},"
                         f"X:{str(space.x)}")


class NotEnoughElementsInStackError(FungeError):
    """Exception raised for executing commands
    that require more arguments than there are in stack"""

    def __init__(self, space):
        self.message = "The stack doesn't have enough elements for command"
        super().__init__(self.message, space)


class IPHasInWrongDimensionError(FungeError):
    """Exception raised when in 'begin block' command '{' ip vector is not
    equal to space dimension"""

    def __init__(self, space):
        self.message = "The ip vector length to 'begin block' command" \
                       "is not equal to the space dimension"
        super().__init__(self.message, space)