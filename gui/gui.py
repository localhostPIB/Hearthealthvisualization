from datetime import datetime
from typing import Final

from nicegui import ui, app
from plotly.graph_objs import Figure

from gui.utils import validate_positive_integer
from service import make_line_plot_service, get_all_heart_service, save_heart_service, save_plot_to_document, \
    all_values_as_json_service

table = None
plot = None
raw_plot = None
no_data_label = None
no_data_icon = None


def save_values(diastolic_input, systolic_input, pulse_input, date=None, time=None):
    global plot

    try:
        diastolic = int(diastolic_input.value)
        systolic = int(systolic_input.value)
        pulse = int(pulse_input.value)

        if date and time and date != '' and time != '':
            full_datetime = f"{date.value} {time.value}"
            date = datetime.strptime(f"{full_datetime}",
                                     "%Y-%m-%d %H:%M")

        if (validate_positive_integer(diastolic) or validate_positive_integer(systolic)
                or validate_positive_integer(pulse)):
            ui.notify('Bitte nur positive Werte eingeben!', color='red')
            return

        save_heart_service(systolic, diastolic, pulse, date)
        update_view()
        ui.notify(f'Diastolisch: {diastolic}, Systolisch: {systolic}, Puls: {pulse}', color='green')
    except Exception as e:
        raise e


def update_view():
    global table, plot, raw_plot, no_data_label, no_data_icon
    all_heart_values: Final[list] = get_all_heart_service()

    if table:
        table.rows = all_values_as_json_service(all_heart_values)
        table.update()

    if plot:
        new_fig: Final[Figure] = make_line_plot_service(get_all_heart_service())
        plot.figure = new_fig
        plot.figure.layout = new_fig.layout
        ui.update(plot)

        if no_data_label and no_data_icon:
            no_data_label.delete()
            no_data_icon.delete()
            no_data_label = None
            no_data_icon = None


def build_gui():
    global table, plot, raw_plot, no_data_label, no_data_icon, no_data_label

    current_date = datetime
    all_heart_values = get_all_heart_service()

    with (ui.grid(columns=1).classes('justify-center items-center w-full')):
        with ui.tabs().classes('w-full') as tabs:
            one = ui.tab('Plot', icon='stacked_line_chart')
            two = ui.tab('Speichern', icon='save_as')
            three = ui.tab('Alle Werte', icon='table_view')

        with ui.tab_panels(tabs, value=one).classes('w-full'):
            with ui.tab_panel(one):
                ui.label('Herzwerte Übersicht').classes('text-2xl font-bold mb-4')

                with ui.row().classes('flex w-full items-start gap-4'):
                    plot_container = ui.card().classes('w-fill p-8')
                    input_container = ui.card().classes('w-1/5 p-8')

                    with plot_container:
                        if all_heart_values:
                            raw_plot = make_line_plot_service(all_heart_values)
                        else:
                            from plotly.graph_objects import Figure
                            raw_plot = Figure()

                        plot = ui.plotly(raw_plot).classes('max-w-full h-auto')

                        if not all_heart_values:
                            no_data_icon = ui.icon('info', color='grey', size='xl')
                            no_data_label = ui.label('Keine Daten vorhanden').classes('text-lg text-gray-500')

                    with input_container:
                        ui.label('Eingabe der Werte').classes('text-lg font-semibold mb-2')

                        systolic_input = ui.input('Systolischer Wert', placeholder='1 - 999 mmHg',
                                                  validation=validate_positive_integer).classes('w-full')

                        diastolic_input = ui.input('Diastolischer Wert', placeholder='1 - 999 mmHg',
                                                   validation=validate_positive_integer).classes('w-full')

                        pulse_input = ui.input('Puls', placeholder='1 - 999 bpm',
                                               validation=validate_positive_integer).classes('w-full')

                        ui.label("Gib Datum und Uhrzeit ein:")
                        date_input = ui.input("Datum", placeholder="Tag.Monat.Jahr", value=current_date.today().date()
                                              .isoformat()).props('type=date').classes('w-full')

                        time_input = ui.input("Uhrzeit", placeholder="hh:mm", value=current_date.now().
                                              strftime('%H:%M')).props('type=time').classes('w-full')

                        ui.button('Werte speichern',
                                  on_click=lambda: save_values(diastolic_input, systolic_input, pulse_input,
                                                               date_input, time_input)).classes('px-6 py-2 mt-2')

            with ui.tab_panel(two):
                ui.button('Speichere Plot als PDF',
                          on_click=lambda: ui.download(save_plot_to_document(
                              make_line_plot_service(get_all_heart_service()), "Hearth"))
                          ).classes('px-6 py-2')

            with ui.tab_panel(three):
                columns = [
                    {'name': 'Datum', 'label': 'Datum', 'field': 'Datum'},
                    {'name': 'Systolisch', 'label': 'Systolisch', 'field': 'Systolisch'},
                    {'name': 'Diastolisch', 'label': 'Diastolisch', 'field': 'Diastolisch'},
                    {'name': 'Puls', 'label': 'Puls', 'field': 'Puls'},
                ]
                if all_heart_values:
                    table = ui.table(columns=columns,rows=all_values_as_json_service(all_heart_values), pagination=10,
                                     on_pagination_change=lambda e: ui.notify(e.value))
                else:
                    table = ui.table(columns=columns,rows=[], pagination=10,
                                     on_pagination_change=lambda e: ui.notify(e.value))
        ui.button('App schließen', on_click=lambda: app.shutdown()).classes('bg-red-500 text-white px-6 py-2')
