# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import base64

from viz.app import app
from . import tips

tips = pd.read_csv('./viz/data/economic/results_summary_bycrop.csv')
col_options = [dict(label=x, value=x) for x in tips.columns]
dimensions = ["x", "y", "color", "facet_col", "facet_row"]
dhover = dimensions + ["dd_hover"]


layout = html.Div(
    [
        html.H1("Data Exploration: Scatter Plot"),
        html.Div(
            [
                html.Div([
                html.P([d + ":", dcc.Dropdown(id=d, options=col_options)])
                for d in dimensions
                ]),
                html.P(['On Hover show: ',
                    dcc.Dropdown(
                    id='dd_hover',
                    options=col_options,
                    multi=True
                )])
            ],
            style={"width": "25%", "float": "left"},
        ),
        dcc.Graph(id="graph", style={"width": "75%", "display": "inline-block"}),
    ]
)


@app.callback(Output("graph", "figure"), [Input(d, "value") for d in dhover])
def make_figure(x, y, color, facet_col, facet_row, hover_info):
    return px.scatter(
        tips,
        x=x,
        y=y,
        color=color,
        facet_col=facet_col,
        facet_row=facet_row,
        height=700,
        hover_data = hover_info,
    )