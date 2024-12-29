import os


def validate_positive_integer(value):
    """Checks whether the number is positive"""
    try:
        int_value = int(value)
        if int_value <= 0:
            return 'Bitte nur positive Werte'
        return None
    except ValueError:
        return 'Bitte geben Sie eine Zahl ein'


def get_downloads_folder():
    """Checks whether the operating system is a Windows or a Mac."""
    if os.name == "nt":  # Windows
        return os.path.join(os.getenv('USERPROFILE'), "Downloads")
    return os.path.expanduser("~/Downloads")  # macOS/Linux
