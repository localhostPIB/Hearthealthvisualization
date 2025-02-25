class HeathValueNotSaveException(Exception):
    """This custom exception is thrown if the heath value not save."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
