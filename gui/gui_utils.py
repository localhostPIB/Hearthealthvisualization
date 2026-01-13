from nicegui import ui


def set_dark_mode():
    """
    You can use a dark mode with this function.
    """
    dark = ui.dark_mode()

    def toggle_dark_mode(e):
        if e.value:
            dark.enable()
        else:
            dark.disable()

    with ui.row().classes('items-center gap-4'):
        ui.icon('light_mode').classes('text-yellow-500 text-2xl')
        ui.switch().bind_value_to(dark, 'value')
        ui.icon('dark_mode').classes('text-indigo-400 text-2xl')

def add_label(table):
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
