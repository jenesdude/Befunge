class CompleteIAGridAlterationError(Exception):
    """Exception raised for attempts of alteration the complete interactive
    Befunge grid"""

    def __init__(self):
        self.message = "The alteration of complete interactive Befunge grid" \
                       "if prohibited"
        super().__init__(self.message)


class IAGridIsNotDefinedError(Exception):
    """Exception raised for executing empty interactive Befunge grid"""

    def __init__(self):
        self.message = "The interactive grid is empty"
        super().__init__(self.message)
