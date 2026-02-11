from nicegui import ui


def set_dark_mode():
    """
    Adds a Nicegui dark mode.
    """
    dark = ui.dark_mode()
    dark.auto()

    with ui.row().classes('items-center gap-4 ml-6'):
        ui.icon('light_mode').classes('text-yellow-500 text-2xl')
        ui.switch().bind_value_to(dark, 'value')
        ui.icon('dark_mode').classes('text-indigo-400 text-2xl')


def systolic_color(systolic_value: int) -> str:
    """
    Adds a color for the systolic heart value.

    Systolic:
    Green: Normal (<120)
    Yellow: High-normal (120-129)
    Orange: Grade 1 hypertension (130-139)
    Red: Grade 2 hypertension (140-179)
    Purple: Grade 3 hypertension (≥180)

    :param systolic_value:  systolic heart value
    :returns: The name of the color
    :rtype: str
    """
    if systolic_value >= 180:
        return 'purple'
    if systolic_value >= 140:
        return 'red'
    if systolic_value >= 130:
        return 'orange'
    if systolic_value >= 120:
        return 'yellow'
    return 'green'


def pulse_color(pulse_value: int) -> str:
    """
    Adds a color for the diastolic heart value.

    Pulse:
    Blue: Bradycardia (<60)
    Green: Normal (60-100)
    Orange: Mild tachycardia (101-120)
    Red: Severe tachycardia (>120)

    :param pulse_value: The Pulse value.
    :returns: The name of the color.
    :rtype: str
        """
    if pulse_value > 120:
        return 'red'
    if pulse_value > 100:
        return 'orange'
    if pulse_value < 60:
        return 'blue'
    return 'green'


def diastolic_color(diastolic_value: int) -> str:
    """
        Adds a color for the diastolic heart value.

        Diastolic:
        Green: Normal (<85)
        Yellow: High-normal (85-89)
        Orange: Hypertension grade 1 (90-99)
        Red: Hypertension grade 2 (100-109)
        Violet (purple): Grade 3 hypertension (≥110)

        :param diastolic_value: Diastolic heart value
        :returns: The name of the color
        :rtype: str
    """
    if diastolic_value >= 110:
        return 'purple'
    if diastolic_value >= 100:
        return 'red'
    if diastolic_value >= 90:
        return 'orange'
    if diastolic_value >= 85:
        return 'yellow'
    return 'green'


def puls_pressure_color(pulse_pressure_value: int) -> str:
    """
    Adds a color for the pulse pressure.
        
    :param pulse_pressure_value: The pulse pressure value.
    :returns: The name of the color.
    :rtype: str
    """
    if pulse_pressure_value >= 90:
        return 'red'
    if pulse_pressure_value >= 76:
        return 'yellow'
    if pulse_pressure_value >= 66:
        return 'orange'
    if pulse_pressure_value >= 40:
        return 'green'
    return 'grey'
