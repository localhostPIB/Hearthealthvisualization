from datetime import datetime
import os
import tempfile
from typing import List, Any, LiteralString

from plotly.graph_objs import Figure, Indicator
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from PyPDF2 import PdfMerger
import plotly.express as px
import pandas as pd
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate

from dao import save_heart, get_all_bmi, get_all_heart, save_bmi, delete_bmi, get_newest_bmi
from exception import PDFNotCreatedException
from model import Heart, BMI
from .utils import create_temp_file


def save_heart_service(systolic_bp: int, diastolic_bp: int, puls_frequency: int, date=None):
    """
    Save the heart-object in the Database.

    :param systolic_bp: the systolic blood pressure.
    :param diastolic_bp: the diastolic blood pressure.
    :param puls_frequency: the pulse frequency.
    :param date: the date of the measuring.
    """
    if date is None:
        save_heart(Heart(systolic_BP=systolic_bp, diastolic_BP=diastolic_bp, puls_Frequency=puls_frequency))
    else:
        save_heart(Heart(systolic_BP=systolic_bp, diastolic_BP=diastolic_bp, puls_Frequency=puls_frequency, date=date))


def save_bmi_service(weight: float, size: float, created_at=None):
    """
    Save the heart-object in the Database.

    :param weight:
    :param size:
    :param date: the date of the measuring.
    """
    save_bmi(BMI(weight=weight, size=size, created_at=created_at))


def get_all_heart_service() -> list[Heart]:
    """
    Outputs all heart-objects in a list.

    :returns: List with all heart-objects.
    :rtype: list
    """
    return get_all_heart()


def get_newest_bmi_service() -> BMI:
    return get_newest_bmi()


def get_all_bmi_service() -> list[BMI]:
    """
    Outputs all bmi-objects in a list.

    :returns: List with all bmi-objects.
    :rtype: list
    """
    return get_all_bmi()


def all_values_as_json_service(all_values: list) -> list[dict[str, Any]]:
    """
    Revised the blood pressure values for Nicegui as JSON.

    :returns: Blood pressure values as JSON.
    :rtype: list
    """
    return [
        {
            "Systolisch": heart.systolic_BP,
            "Diastolisch": heart.diastolic_BP,
            "Pulsdruck": heart.calc_pulse_pressure(),
            "Puls": heart.puls_Frequency,
            "Datum": heart.date.strftime("%d-%m-%Y")
        }
        for heart in all_values
    ]


def delete_bmi_value(bmi_id: id):
    """
    Deletes the BMI entry in the database using the id in the database
        
    :param bmi_id: the id of the BMI entry.
    """
    delete_bmi(bmi_id)


def make_gauge_chart_service(bmi: float) -> Figure:
    """
    Creates a plot for the Body-Mass-Index (BMI) with Plotly based on the heart values.
    BMI = weight / (height ** 2)

    :param bmi: BMI value as float.
    :returns: Plotly figure.
    :rtype:  Figure
    """
    return Figure(Indicator(
        mode="gauge+number",
        value=bmi,
        title={'text': "BMI"},
        gauge={
            'axis': {'range': [0, 40]},
            'steps': [
                {'range': [0, 18.5], 'color': "lightblue", 'name': "Untergewicht"},
                {'range': [18.5, 24.9], 'color': "lightgreen", 'name': "Normalgewicht"},
                {'range': [25, 29.9], 'color': "yellow", 'name': "Übergewicht"},
                {'range': [30, 34.9], 'color': "orange", 'name': "Adipositas I"},
                {'range': [35, 40], 'color': "red", 'name': "Adipositas II+"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': bmi
            }
        }
    ))


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

    df = df.sort_values(by='date')

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


def create_measurement_table(measurements: list[dict]) -> Table:
    """
    Creates a table with all heart values
        
    :param measurements: measurement list
    :returns: Table with all heart values.
    :rtype: Table
    """
    if not measurements:
        return Table([["Keine Daten verfügbar"]])

    keys = ["Datum", "Systolisch", "Diastolisch", "Pulsdruck", "Puls"]
    units = {
        "Systolisch": "mmHg",
        "Diastolisch": "mmHg",
        "Pulsdruck": "mmHg",
        "Puls": "bpm",
        "Datum": ""
    }

    header = ["#"] + keys
    table_data = [header]

    for i, measurement in enumerate(measurements):
        row = [f"Messung {i + 1}"]
        for key in keys:
            value = measurement.get(key, "")
            einheit = units.get(key, "")
            wert_str = f"{value} {einheit}" if einheit and value != "" else str(value)
            row.append(wert_str)
        table_data.append(row)

    table = Table(table_data, colWidths=[3 * cm] + [3.5 * cm] * len(keys))
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2e6da4")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (1, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
    ]))

    return table


def save_health_data_to_document(heart_plot: Figure, bmi_plot: Figure ,measured_values: dict, pdf_name=None) -> LiteralString | str | bytes:
    """
    Makes a PDF from the heart values, the BMI plot and the plot of the heart values.

    :param heart_plot: The plot with the heart values.
    :param bmi_plot: The plot with the BMI values.
    :param measured_values: The heart values.
    :param pdf_name: Name of the final PDF-file.
    :returns: The path of the final PDF-file.
    :rtype: LiteralString | str | bytes
    """
    canvas_width, canvas_height = landscape(A4)
    now = datetime.now()
    pdf_name = pdf_name or "plot"

    timestamp = str(int(now.timestamp() * 1000))
    temp_dir = tempfile.gettempdir()
    pdf_base = f"{pdf_name}_{timestamp}"

    plot_pdf_path = os.path.join(temp_dir, f"{pdf_base}_plot.pdf")
    table_pdf_path = os.path.join(temp_dir, f"{pdf_base}_table.pdf")
    final_pdf_path = os.path.join(temp_dir, f"{pdf_base}.pdf")

    try:
        c = canvas.Canvas(plot_pdf_path, pagesize=(canvas_width, canvas_height))
        img_bytes_heart = heart_plot.to_image(format="png", width=1000, height=600)
        img_bytes_bmi = bmi_plot.to_image(format="png", width=1000, height=600)

        img_path_temp_bmi = create_temp_file(img_bytes_bmi)
        img_path_temp_heart = create_temp_file(img_bytes_heart)

        scale = canvas_width / 1000
        width, height = 1000 * scale, 600 * scale
        x, y = (canvas_width - width) / 2, (canvas_height - height) / 2
        c.drawImage(img_path_temp_heart, x, y, width, height)
        c.showPage()
        c.drawImage(img_path_temp_bmi, x, y, width, height)
        c.showPage()
        c.save()
        os.remove(img_path_temp_heart)
        os.remove(img_path_temp_bmi)

        doc = SimpleDocTemplate(table_pdf_path, pagesize=landscape(A4))
        table = create_measurement_table(measured_values)
        doc.build([table])

        merger = PdfMerger()
        merger.append(plot_pdf_path)
        merger.append(table_pdf_path)
        merger.write(final_pdf_path)
        merger.close()
        os.remove(plot_pdf_path)
        os.remove(table_pdf_path)

        return final_pdf_path

    except PDFNotCreatedException as e:
        raise e
