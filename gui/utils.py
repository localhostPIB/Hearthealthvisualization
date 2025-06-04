import os


def validate_positive_integer(value: int) -> str | None:
    """Checks whether the number is positive.

    :param value: The number to validate.
    :return: The number or None if the number is negative.
    :rtype: str | None
    """
    try:
        int_value = int(value)
        if int_value <= 0:
            return 'Bitte nur positive Werte'
        return None
    except ValueError:
        return 'Bitte geben Sie eine Zahl ein'


def get_downloads_folder() -> str:
    """Checks whether the operating system is a Windows or a Mac.

    :return: Download Path to the operating system.
    :rtype: str | None
    """
    if os.name == "nt":  # Windows
        return os.path.join(os.getenv('USERPROFILE'), "Downloads")
    return os.path.expanduser("~/Downloads")  # macOS/Linux
