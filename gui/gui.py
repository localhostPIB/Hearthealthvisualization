from nicegui import ui, app

from gui.utils import validate_positive_integer
from service import make_line_plot_service, get_all_heart_service, save_heart_service, save_plot_to_pdf, \
    all_heart_values_as_json_service

table = None
plot = None


def save_values(diastolic_input, systolic_input, pulse_input):
    try:
        diastolic = int(diastolic_input.value)
        systolic = int(systolic_input.value)
        pulse = int(pulse_input.value)

        if (validate_positive_integer(diastolic) or validate_positive_integer(systolic)
                or validate_positive_integer(pulse)):
            ui.notify('Bitte nur positive Werte eingeben!', color='red')
            return

        save_heart_service(systolic, diastolic, pulse)
        update_view()
        ui.notify(f'Diastolisch: {diastolic}, Systolisch: {systolic}, Puls: {pulse}', color='green')
    except ValueError:
        ui.notify('Ungültige Eingabe. Bitte geben Sie (ganze) positive Zahlen ein!', color='red')


def update_view():
    if table and plot:
        table.rows = all_heart_values_as_json_service()
        table.update()
        plot.fig = make_line_plot_service(get_all_heart_service())
        plot.update()


def build_gui():
    global table
    global plot

    with (ui.grid(columns=1).classes('justify-center items-center w-full')):
        with ui.tabs().classes('w-full') as tabs:
            one = ui.tab('Plot', icon='stacked_line_chart')
            two = ui.tab('Speichern', icon='save_as')
            three = ui.tab('Alle Werte', icon='table_view')
        with ui.tab_panels(tabs, value=one).classes('w-full'):
            with ui.tab_panel(one):
                ui.label('Herzwerte Übersicht').classes('text-2xl font-bold mb-4')

                raw_plot = make_line_plot_service(get_all_heart_service())
                plot = ui.plotly(raw_plot).classes('mb-6 w-full')

                with ui.column().classes('gap-4 mb-6'):
                    diastolic_input = ui.input('Diastolischer Wert', placeholder='1 - 999 mmHg',
                                               validation=validate_positive_integer).classes('w-full')

                    systolic_input = ui.input('Systolischer Wert', placeholder='1 - 999 mmHg',
                                              validation=validate_positive_integer).classes('w-full')

                    pulse_input = ui.input('Puls', placeholder='1 - 999 bpm',
                                           validation=validate_positive_integer).classes('w-full')

                with ui.row().classes('gap-4 justify-center mb-6'):
                    ui.button('Werte speichern',
                              on_click=lambda: save_values(diastolic_input, systolic_input, pulse_input)).classes(
                        'px-6 py-2')

            with ui.tab_panel(two):
                ui.button('Speichere Plot als PDF',
                          on_click=lambda: ui.download(save_plot_to_pdf(make_line_plot_service(get_all_heart_service()),
                                                                        "Hearth"))).classes('px-6 py-2')

            with ui.tab_panel(three):
                table = ui.table(rows=all_heart_values_as_json_service(), pagination=10,
                                 on_pagination_change=lambda e: ui.notify(e.value))

        ui.button('App schließen', on_click=lambda: app.shutdown()).classes('bg-red-500 text-white px-6 py-2')
