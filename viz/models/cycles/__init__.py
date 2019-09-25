import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table

import pandas as pd
import numpy as np
import plotly.express as px

from viz.app import app

# Data Management Section: import and massage
dmaize = pd.read_csv('./viz/data/cycles/maize.csv')
dsorghum = pd.read_csv('./viz/data/cycles/sorghum.csv')
dall = dmaize.append(dsorghum)
planting_dates =dall['planting_date'].unique()
planting_min = int(planting_dates.min())
planting_max = int(planting_dates.max())

# Layout
app.layout = html.Div([
    html.Div([
        html.Div([
            html.P('Crop:'),
            dcc.Dropdown(id='dd_crop',
                options=[dict(label=x, value=x) for x in dall['crop'].unique()],
                value=dall['crop'].unique()[0]
                ),
            html.P('Location:'),
            dcc.Dropdown(id='dd_location',
                options=[dict(label=x, value=x) for x in dall['location'].unique()],
                value=dall['location'].unique()[0]
                ),
            html.P('Year(s):'),
            dcc.Dropdown(id='dd_year',
                options=[dict(label=x, value=x) for x in dall['year'].unique()],
                value=dall['year'].unique()[0]
                #multi=True,
                #placeholder="Selct years. Shows all if none selected.",
                ),
            html.P('Planting date range:'),
            dcc.Slider(
                id='s_planting',
                min = planting_min,
                max = planting_max,
                marks={int(i):str(i) for i in planting_dates},
                step=None,
                value=planting_min,
            ),
        ],className="three columns"),
        html.Div([
            dcc.Graph(id='cycles_graph'),
        ],className="nine columns"),
    ],className="row"),
])

# Callbacks
@app.callback(
    Output('cycles_graph', 'figure'),
    [Input('dd_crop', 'value'),Input('dd_location', 'value'),
    Input('dd_year', 'value'),Input('s_planting', 'value')])
def update_figure(crop,location,year,planting):
    filtered_df = dall[(dall.crop == crop)&(dall.location == location)&
        (dall['planting_date_fixed']==True)&(dall.year == year)&(dall.planting_date == planting)]
    filtered_df = filtered_df.sort_values('nitrogen_rate')
    return px.line(
        filtered_df,
        x='nitrogen_rate',
        y='yield',
        color='weed_fraction',
    )
