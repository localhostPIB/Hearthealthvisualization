from nicegui import ui, app

from service import make_line_plot_service, get_all_heart_service


def build_gui():
    ui.plotly(make_line_plot_service(get_all_heart_service()))
    ui.input(label='Diastolischer Wert', placeholder='Diastolischer Wert')
    ui.input(label='Systolischer Wert', placeholder='Systolischer Wert')
    ui.button('App schließen', on_click=lambda: app.shutdown())
