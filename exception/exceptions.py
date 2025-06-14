class HeathValueNotSaveException(Exception):
    """This custom exception is thrown if the heath value not saves."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class BMIValueNotSaveException(Exception):
    """This custom exception is thrown if the BMI value not saves."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NiceGUINotStartedException(Exception):
    """This custom exception is thrown if the niceGUI start is not started."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class PDFNotCreatedException(Exception):
    """This custom exception is thrown if the PDF cannot be created."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
