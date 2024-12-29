from nicegui import ui, app

from gui.utils import validate_positive_integer
from service import make_line_plot_service, get_all_heart_service, save_heart_service, save_plot_to_pdf


def save_values(diastolic_input, systolic_input, pulse_input, plot):
    try:
        diastolic = int(diastolic_input.value)
        systolic = int(systolic_input.value)
        pulse = int(pulse_input.value)

        if validate_positive_integer(diastolic) or validate_positive_integer(systolic) or validate_positive_integer(pulse):
            ui.notify('Bitte nur positive Werte eingeben!', color='red')
            return

        save_heart_service(systolic, diastolic, pulse)
        ui.notify(f'Diastolisch: {diastolic}, Systolisch: {systolic}, Puls: {pulse}', color='green')
        ui.update(plot)
    except ValueError:
        ui.notify('Ungültige Eingabe. Bitte geben Sie (ganze) positive Zahlen ein!', color='red')


def build_gui():
    with ui.grid(columns=2):
        raw_plot = make_line_plot_service(get_all_heart_service())
        plot = ui.plotly(raw_plot)
        ui.space()
        with ui.row():
            diastolic_input = ui.input('Diastolischer Wert', placeholder='1 - 999 mmHg',
                                       validation=validate_positive_integer)
            systolic_input = ui.input('Systolischer Wert', placeholder='1 - 999 mmHg',
                                      validation=validate_positive_integer)
            pulse_input = ui.input('Puls', placeholder='1 - 999 bpm',
                                   validation=validate_positive_integer)

            ui.button('Werte speichern', on_click=lambda: save_values(diastolic_input, systolic_input, pulse_input, plot))
            ui.button('Speichere Plot als PDF', on_click=lambda: ui.download(save_plot_to_pdf(raw_plot, "Hearth")))
        ui.button('App schließen', on_click=lambda: app.shutdown())
