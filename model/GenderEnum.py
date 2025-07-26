from enum import Enum


class GenderEnum(Enum):
    """
    An Enum class for the Gender of the User.
    """
    MALE = "Mann"
    FEMALE = "Frau"
    DIVERSE = "Divers"
    UNKNOWN = "Unbekannt"
