from nicegui import ui, app
from model import GenderEnum


def build_stepper(validate_positive_float, save_user_values, save_bmi_values, build_grid_view):
    """
    If the database is empty, a short interactive question is asked.

    :param validate_positive_float: Function to validate positive float values.
    :param save_user_values: Function to save user values.
    :param save_bmi_values: Function to save BMI values.
    :param build_grid_view: Function to build the grid view.
    """
    size_input = None
    weight_input = None

    stepper_container = ui.column().classes('w-full h-screen/3 flex items-center justify-center')
    result_container = ui.column().classes('w-full')
    result_container.set_visibility(False)

    with (stepper_container):
        with ui.button_group().props('push glossy'):
            ui.button('Schließen',icon='highlight_off' ,color='red', on_click=lambda: app.shutdown()).props('push')
        with ui.stepper().props('vertical').classes('w-full') as stepper:

            with ui.step('Allgemeine Daten: Name, Geschlecht, Alter').classes('w-full'):

                first_name_input = ui.input('Vorname', validation=lambda value: 'Bitte geben Sie ihren Vornamen ein'
                if len(value) < 2 else None)

                last_name_input = ui.input('Nachname', validation=lambda value: 'Bitte geben Sie ihren Nachnamen ein'
                if len(value) < 2 else None)

                gender_select = gender_select = ui.select(options=[(e, ) for e in GenderEnum],label='Geschlecht',
                                                          with_input=True)

                age_input = ui.input('Alter', validation=validate_positive_float)

                # Advances stepper if all inputs are valid
                def go_to_next_if_valid():
                    if age_input.validate() and gender_select.validate() and first_name_input.validate() and last_name_input.validate():
                        stepper.next()

                with ui.stepper_navigation():
                    ui.button('Weiter', on_click=go_to_next_if_valid)

            with ui.step('BMI: Körpergröße'):
                ui.label('Bitte geben Sie Ihre Körpergröße in m ein:')
                size_input = ui.input(
                    'Körpergröße (in m)',
                    placeholder='0.5 - 2.5 m',
                    validation=validate_positive_float
                )

                def go_to_next_if_valid():
                    if size_input.validate():
                        stepper.next()

                with ui.stepper_navigation():
                    ui.button('Weiter', on_click=go_to_next_if_valid)
                    ui.button('Zurück', on_click=stepper.previous).props('flat')

            with ui.step('BMI: Gewicht'):
                ui.label('Bitte geben Sie Ihr Gewicht in kg ein:')
                weight_input = ui.input(
                'Körpergewicht (in kg)',
                    placeholder='1 - 999 kg',
                    validation=validate_positive_float
                    )

                # Validates input; saves data; shows the mainscreen
                def finish_if_valid():
                    global user_id

                    if weight_input.validate():
                        user_id = save_user_values(first_name_input, last_name_input ,gender_select, age_input)
                        save_bmi_values(weight_input, size_input, user_id)
                        stepper_container.set_visibility(False)
                        result_container.set_visibility(True)

                        with result_container:
                            build_grid_view()

                with ui.stepper_navigation():
                    ui.button('Zurück', on_click=stepper.previous).props('flat')
                    ui.button('Fertigstellen', on_click=finish_if_valid)
