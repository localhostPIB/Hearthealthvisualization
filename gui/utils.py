def validate_positive(value):
    try:
        number = float(value)
        if number >= 0:
            return True
        else:
            return False
    except ValueError:
        return False
