from datetime import datetime
from typing import Final

from nicegui import ui, app
from plotly.graph_objs import Figure

from exception import HeathValueNotSaveException
from gui.utils import validate_positive_integer, validate_positive_float
from service import make_line_plot_service, get_all_heart_service, save_heart_service, save_health_data_to_document, \
    all_values_as_json_service, make_gauge_chart_service, save_bmi_service, get_all_bmi_service, get_newest_bmi_service

table = None
plot = None
bmi_plot = None
raw_plot = None
bmi_label = None
no_data_label_bmi = None
no_data_label = None
no_data_icon_bmi = None
no_data_icon = None


def save_bmi_values(weight_input, size_input):
    weight = float(weight_input.value)
    size = float(size_input.value)

    if validate_positive_float(weight) or validate_positive_float(size):
        ui.notify('Bitte nur positive Werte eingeben!', color='red')
        return

    save_bmi_service(weight, size)
    update_view()


def save_heart_values(diastolic_input, systolic_input, pulse_input, date=None, time=None):
    """
    Here the new heart values are validated and forwarded to the service for storage, and the user receives feedback.
    
    :param diastolic_input: Diastolic value of the blood pressure measurement.
    :param systolic_input: Systolic value of the blood pressure measurement.
    :param pulse_input: Pulse of the blood pressure measurement.
    :param date: Date of measurement.
    :param time: Time of the measurement.
    """

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
    except HeathValueNotSaveException as e:
        raise e


def update_view():
    """
    Gui elements are updated here as soon as something is added, such as the table, plot and the symbols/hints.
    """
    global table, plot, raw_plot, no_data_label, no_data_icon, bmi_plot, bmi_label, no_data_icon_bmi, no_data_label_bmi
    all_heart_values: Final[list] = get_all_heart_service()
    all_bmi_values: Final[list] = get_all_bmi_service()

    if table and all_heart_values:
        table.rows = all_values_as_json_service(all_heart_values)
        table.update()
        add_label()

    if plot and all_heart_values:
        new_fig: Final[Figure] = make_line_plot_service(get_all_heart_service())
        plot.figure = new_fig
        plot.figure.layout = new_fig.layout
        ui.update(plot)

        if no_data_label and no_data_icon:
            no_data_label.delete()
            no_data_icon.delete()
            no_data_label = None
            no_data_icon = None

    if bmi_plot and all_bmi_values:
        new_bmi_plot: Final[Figure] = make_gauge_chart_service(get_newest_bmi_service().calc_bmi())
        bmi_plot.figure = new_bmi_plot
        bmi_plot.figure.layout = new_bmi_plot.layout
        ui.update(bmi_plot)
        #bmi_label.set_text(f"Bei einer Körpergröße von: {get_newest_bmi_service().size}m "
         #                                f"wiegen Sie {get_newest_bmi_service().weight}kg")

        if no_data_label_bmi:
            no_data_icon_bmi.delete()
            no_data_label_bmi.delete()
            no_data_icon_bmi = None
            no_data_label_bmi = None



def build_gui():
    """
    The gui is assembled here.
    """
    global table, plot, raw_plot, no_data_label_bmi ,no_data_label, no_data_icon, no_data_label,no_data_icon_bmi ,bmi_plot, bmi_label

    ui.page_title('Gesundheitsmonitoring')
    current_date = datetime
    all_heart_values = get_all_heart_service()

    with (ui.grid(columns=1).classes('justify-center items-center w-full')):
        with ui.tabs().classes('w-full') as tabs:
            one = ui.tab('Plot', icon='stacked_line_chart')
            two = ui.tab('Speichern', icon='save_as')
            three = ui.tab('Alle Werte', icon='table_view')

        with ui.tab_panels(tabs, value=one).classes('w-full'):
            with ui.tab_panel(one):
                with ui.expansion('Herzgesundheit', icon='monitor_heart').classes('w-full'):
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
                            date_input = ui.input("Datum", placeholder="Tag.Monat.Jahr",
                                                  value=current_date.today().date()
                                                  .isoformat()).props('type=date').classes('w-full')

                            time_input = ui.input("Uhrzeit", placeholder="hh:mm", value=current_date.now().
                                                  strftime('%H:%M')).props('type=time').classes('w-full')

                            ui.button('Werte speichern',
                                      on_click=lambda: save_heart_values(diastolic_input, systolic_input, pulse_input,
                                                                   date_input, time_input)).classes('px-6 py-2 mt-2')

                with ui.expansion("Übersicht Body Mass Index", icon='run_circle').classes('w-full'):
                    ui.label('Übersicht Body Mass Index (BMI) Übersicht').classes('text-2xl font-bold mb-4')
                    with ui.row().classes('flex w-full flex-wrap justify-between gap-1'):
                        plot_container = ui.card().classes('w-[50%] min-h-[400px] p-6 flex flex-col items-center justify-center')
                        input_container = ui.card().classes('w-[40%] min-h-[400px] p-6 flex flex-col justify-between')

                        with plot_container:
                            bmi = get_newest_bmi_service()
                            if not bmi:
                                no_data_icon_bmi = ui.icon('info', color='grey', size='xl')
                                no_data_label_bmi = ui.label('Keine Daten vorhanden').classes('text-lg text-gray-500')
                                bmi_raw_plot = make_gauge_chart_service(0)
                            else:
                                bmi_raw_plot = make_gauge_chart_service(get_newest_bmi_service().calc_bmi())
                                #ui.image('resources/static/img/body_img.png').classes('max-h-100')
                                ui.label(f"Bei einer Körpergröße von: {bmi.size} m wiegen Sie {bmi.weight} kg").classes(
                                'text-center')

                            bmi_plot = ui.plotly(bmi_raw_plot).classes('w-full max-w-[500px] h-[500px]')

                        with input_container:
                            ui.label('Eingabe der Werte').classes('text-lg font-semibold mb-4')

                            weight_input = ui.input(
                                'Körpergewicht (in kg)',
                                placeholder='1 - 999 kg',
                                validation=validate_positive_float
                            ).classes('w-full mb-2')

                            size_input = ui.input(
                                'Körpergröße (in m)',
                                placeholder='0.5 - 2.5 m',
                                validation=validate_positive_float
                            ).classes('w-full mb-4')

                            ui.button(
                                'Werte speichern',
                                on_click=lambda: save_bmi_values(weight_input, size_input)
                            ).classes('px-6 py-2 self-start')


            with ui.tab_panel(two):
                all_heart_values = get_all_heart_service()

                ui.button('Speichere Plot als PDF',
                          on_click=lambda: ui.download(save_health_data_to_document(
                              make_line_plot_service(all_heart_values),
                              make_gauge_chart_service(get_newest_bmi_service().calc_bmi()),
                              all_values_as_json_service(all_heart_values)),"Health")
                          ).classes('px-6 py-2')

            with ui.tab_panel(three):
                columns = [
                    {'name': 'Datum', 'label': 'Datum', 'field': 'Datum'},
                    {'name': 'Systolisch', 'label': 'Systolisch', 'field': 'Systolisch'},
                    {'name': 'Diastolisch', 'label': 'Diastolisch', 'field': 'Diastolisch'},
                    {'name': 'Pulsdruck', 'label': 'Pulsdruck', 'field': 'Pulsdruck'},
                    {'name': 'Puls', 'label': 'Puls', 'field': 'Puls'},
                ]
                if all_heart_values:
                    table = ui.table(columns=columns, rows=all_values_as_json_service(all_heart_values), pagination=10,
                                     on_pagination_change=lambda e: ui.notify(e.value))
                    add_label()
                else:
                    table = ui.table(columns=columns, rows=[], pagination=10,
                                     on_pagination_change=lambda e: ui.notify(e.value))
        ui.button('App schließen', on_click=lambda: app.shutdown()).classes('bg-red-500 text-white px-6 py-2')


def add_label():
    """
    Adds label to show the user which values are okay and which are too high

    Pulse:
    Blue: Bradycardia (<60)
    Green: Normal (60-100)
    Orange: Mild tachycardia (101-120)
    Red: Severe tachycardia (>120)

    Systolic:
    Green: Normal (<120)
    Yellow: High-normal (120-129)
    Orange: Grade 1 hypertension (130-139)
    Red: Grade 2 hypertension (140-179)
    Purple: Grade 3 hypertension (≥180)

    Diastolic:
    Green: Normal (<85)
    Yellow: High-normal (85-89)
    Orange: Hypertension grade 1 (90-99)
    Red: Hypertension grade 2 (100-109)
    Violet (purple): Grade 3 hypertension (≥110)
    """
    table.add_slot('body-cell-Puls', '''
        <q-td key="puls" :props="props">
            <q-badge :color="
                props.value > 120 ? 'red' :
                props.value > 100 ? 'orange' :
                props.value < 60 ? 'blue' :
                'green'">
                {{ props.value }}
            </q-badge>
        </q-td>
    ''')

    table.add_slot('body-cell-Systolisch', '''
        <q-td key="systolisch" :props="props">
            <q-badge :color="
                props.value >= 180 ? 'purple' : 
                props.value >= 140 ? 'red' : 
                props.value >= 130 ? 'orange' : 
                props.value >= 120 ? 'yellow' : 
                'green'">
                {{ props.value }}
            </q-badge>
        </q-td>
    ''')

    table.add_slot('body-cell-Diastolisch', '''
        <q-td key="diastolisch" :props="props">
            <q-badge :color="
                props.value >= 110 ? 'purple' : 
                props.value >= 100 ? 'red' : 
                props.value >= 90 ? 'orange' : 
                props.value >= 85 ? 'yellow' : 
                'green'">
                {{ props.value }}
            </q-badge>
        </q-td>
    ''')

    table.add_slot('body-cell-Pulsdruck', '''
        <q-td key="pulsdruck" :props="props">
            <q-badge :color="props.value >= 90 ? 'red' : 
                             props.value >= 76 ? 'yellow' : 
                             props.value >= 66 ? 'orange' : 
                             props.value >= 40 ? 'green' : 'grey'">
                {{ props.value }}
            </q-badge>
        </q-td>
    ''')
