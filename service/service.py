from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import plotly.express as px
import pandas as pd

import os
import tempfile

from dao import save_heart, get_all_heart
from model import Heart


def save_heart_service(systolic_BP: int, diastolic_BP: int, puls_Frequency: int):
    heart: Heart = Heart(systolic_BP=systolic_BP, diastolic_BP=diastolic_BP, puls_Frequency=puls_Frequency)

    save_heart(heart)


def get_all_heart_service() -> list[Heart]:
    list: list[Heart] = get_all_heart()

    return list


def make_line_plot_service(data, save: bool):
    df = pd.DataFrame([(d.puls_Frequency, d.date, d.systolic_BP, d.diastolic_BP) for d in data],
                      columns=['puls_Frequency', 'date', 'systolic_BP', 'diastolic_BP'])

    fig = px.line(df, x=df["date"], y=df.columns, width=1024, height=768)

    fig.data[0].name = "Puls"
    fig.data[1].name = "Systolisch"
    fig.data[2].name = "Diastolisch"

    fig.update_layout(
        legend_title="Legende",
        xaxis_title="Datum",
        yaxis_title="Blutdruck/Puls"
    )

    if not save:
        fig.show()

    return fig


def save_plot_to_pdf(plot, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=A4)

    img_bytes = plot.to_image(format="png")

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(img_bytes)
        temp.flush()
        temp_name = temp.name

    x = 50
    y = 550
    width = 500
    height = 300

    c.drawImage(temp_name, x, y, width, height)
    os.remove(temp_name)

    c.save()
