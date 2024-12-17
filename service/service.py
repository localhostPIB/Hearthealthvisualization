from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
import plotly.express as px
import pandas as pd

import os
import tempfile

from dao import save_heart, get_all_heart
from model import Heart


def save_heart_service(systolic_BP: int, diastolic_BP: int, puls_Frequency: int):
    save_heart(Heart(systolic_BP=systolic_BP, diastolic_BP=diastolic_BP, puls_Frequency=puls_Frequency))


def get_all_heart_service() -> list[Heart]:
    return get_all_heart()


def make_line_plot_service(data):
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

    return fig


def save_plot_to_pdf(plot, pdf_path):
    canvas_width, canvas_height = landscape(A4)
    c = canvas.Canvas(pdf_path, pagesize=(canvas_width, canvas_height))
    try:
        img_bytes = plot.to_image(format="png")

        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(img_bytes)
            temp.flush()
            temp_name = temp.name

        width = 500
        height = 300

        desired_img_width = canvas_width
        scaling_factor = desired_img_width / width
        width *= scaling_factor
        height *= scaling_factor

        x = (canvas_width - width) / 2
        y = (canvas_height - height) / 2

        c.drawImage(temp_name, x, y, width, height)
        os.remove(temp_name)

        c.save()
    except Exception as e:
        raise
