import json
from datetime import datetime
import os
import tempfile
from typing import List, Dict, Any, LiteralString

from plotly.graph_objs import Figure
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
import plotly.express as px
import pandas as pd

from dao import save_heart, get_all_heart
from gui.utils import get_downloads_folder
from model import Heart


def save_heart_service(systolic_bp: int, diastolic_bp: int, puls_frequency: int):
    save_heart(Heart(systolic_BP=systolic_bp, diastolic_BP=diastolic_bp, puls_Frequency=puls_frequency))


def get_all_heart_service() -> list[Heart]:
    """
    Outputs all heart-objects in a list.

    :returns: List with all heart-objects.
    :rtype: list
    """
    return get_all_heart()


def all_heart_values_as_json_service() -> list[dict[str, Any]]:
    """
    Revised the blood pressure values for Nicegui as JSON.

    :returns: Blood pressure values as JSON.
    :rtype: list
    """
    return [
        {
            "Systolisch": heart.systolic_BP,
            "Diastolisch": heart.diastolic_BP,
            "Puls": heart.puls_Frequency,
            "Datum": heart.date.strftime("%d-%m-%Y")
        }
        for heart in get_all_heart_service()
    ]


def make_line_plot_service(heart_list: List[Heart]) -> Figure:
    """
    Creates a plot with Plotly based on the heart values.
        
    :param heart_list:
    :returns: Plotly figure.
    :rtype:  Figure
    """
    df = pd.DataFrame([(heart_value.puls_Frequency, heart_value.date, heart_value.systolic_BP, heart_value.diastolic_BP)
                       for heart_value in heart_list],
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


def save_plot_to_document(plot: Figure, pdf_name=None, file_format=".pdf") -> LiteralString | str | bytes:
    """
    Creates a document of the plot.

    :param plot: Plotly figure.
    :param pdf_name: The name of the output PDF.
    :param file_format: The format of the output document, default is '.pdf'.
    :returns: The name of the output PDF.
    :rtype: str
    """
    canvas_width, canvas_height = landscape(A4)
    now = datetime.now()
    pdf_path = os.path.join(get_downloads_folder(), pdf_name + str(now.timestamp() * 1000) + file_format)

    if pdf_name is None:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_format)

    c = canvas.Canvas(pdf_path, pagesize=(canvas_width, canvas_height))

    try:
        img_bytes = plot.to_image(format="png", width=1000, height=600)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
            temp_img.write(img_bytes)
            temp_img.flush()
            temp_name = temp_img.name

        desired_img_width = canvas_width
        scaling_factor = desired_img_width / 1000
        width = 1000 * scaling_factor
        height = 600 * scaling_factor

        x = (canvas_width - width) / 2
        y = (canvas_height - height) / 2

        c.drawImage(temp_name, x, y, width, height)
        os.remove(temp_name)

        c.save()

        return pdf_path
    except Exception as e:
        raise RuntimeError(f"Fehler beim Erstellen der PDF: {e}")
