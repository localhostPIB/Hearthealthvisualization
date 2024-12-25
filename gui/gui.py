from nicegui import ui, app

from service import make_line_plot_service, get_all_heart_service, save_heart_service


def validate_positive_integer(value):
    try:
        int_value = int(value)
        if int_value <= 0:
            return 'Bitte nur positive Werte'
        return None
    except ValueError:
        return 'Bitte geben Sie eine Zahl ein'


def save_values(diastolic_input, systolic_input, pulse_input, plot):
    try:
        diastolic = int(diastolic_input.value)
        systolic = int(systolic_input.value)
        pulse = int(pulse_input.value)

        if diastolic <= 0 or systolic <= 0 or pulse <= 0:
            ui.notify('Bitte nur positive Werte eingeben!', color='red')
            return

        save_heart_service(systolic, diastolic, pulse)
        ui.notify(f'Diastolisch: {diastolic}, Systolisch: {systolic}, Puls: {pulse}', color='green')
        ui.update(plot)
    except ValueError:
        ui.notify('Ungültige Eingabe. Bitte geben Sie (ganze) positive Zahlen ein!', color='red')


def build_gui():
    with ui.grid(columns=2):
        plot = ui.plotly(make_line_plot_service(get_all_heart_service()))
        ui.space()
        with ui.row():
            diastolic_input = ui.input('Diastolischer Wert', placeholder='1 - 999 mmHg',
                                       validation=validate_positive_integer)
            systolic_input = ui.input('Systolischer Wert', placeholder='1 - 999 mmHg',
                                      validation=validate_positive_integer)
            pulse_input = ui.input('Puls', placeholder='1 - 999 bpm',
                                   validation=validate_positive_integer)

            ui.button('Werte speichern', on_click=lambda: save_values(diastolic_input, systolic_input, pulse_input, plot))
        ui.button('App schließen', on_click=lambda: app.shutdown())
