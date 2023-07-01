from plotly.subplots import make_subplots

from dao import save_heart, get_all_heart
from model import Heart
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def save_heart_service(systolic_BP: int, diastolic_BP: int, puls_Frequency:int):

    heart: Heart = Heart(systolic_BP=systolic_BP, diastolic_BP=diastolic_BP, puls_Frequency=puls_Frequency)

    save_heart(heart)

def get_all_heart_service() -> list[Heart]:
    list: list[Heart] = get_all_heart()

    return list

def make_line_plot_service(data):
    df = pd.DataFrame([(d.puls_Frequency, d.date, d.systolic_BP, d.diastolic_BP ) for d in data],
                      columns=['puls_Frequency', 'date','systolic_BP','diastolic_BP'])

    fig = px.line(df, x=df["date"], y=df.columns,
                  hover_data={"date": "|%B %d, %Y"})

    fig.show()