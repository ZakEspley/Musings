import pandas as pd
import plotly.express as px
import numpy as np
from jupyter_dash import JupyterDash
import dash as d
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from datetime import date
import datetime

pd.options.plotting.backend = "plotly"


df = pd.read_csv('BigGValues.csv')
uqYears = df["Year"].drop_duplicates()
uqYears.sort_values(inplace=True)
uqYears.reset_index(drop=True,inplace=True)


# rangeMarks = {year:{'label': f'{year}',
#         'style': {'transform': 'rotate(90deg)'}} for year in uqYears}

rangeMarks = {i: f'Label {uqYears.loc[i]}' for i in range(len(uqYears)) }

rangeMarks = {1:'Hi', 2:'Small', 3:'World'}

rangeMarks = {uqYears.loc[i]: f'{uqYears.loc[i]}' if i%3==0 else '' for i in range(len(uqYears))}

app = JupyterDash(__name__)
app.layout = html.Div([
    html.H1("Values of G Measured over Time"),
    html.Br(),

#     dcc.DatePickerRange(
#         id = 'date-picker',
#         display_format="YYYY",
#         start_date = date(1798,1,1),
#         end_date = date.today(),
#         min_date_allowed = date(1796,1,1)
#     ),

    dcc.RangeSlider(
        min = uqYears.min(),
        max = uqYears.max(),
        step = None,
        marks = rangeMarks,
        value = [uqYears.min(), uqYears.max()]
    ),


    dcc.Graph(id="plot")
])

if __name__ == "__main__":
    app.run_server(debug=True)
