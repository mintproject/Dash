import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table

import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

## FOR LIVE
from viz.app import app
##

#styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Data Management Section: import and massage,
### LIVE
dmaize = pd.read_csv('./viz/data/cycles/maize.csv')
dsorghum = pd.read_csv('./viz/data/cycles/sorghum.csv')
### END LIVE

## LOCAL
# dmaize = pd.read_csv('Data/cycles/maize.csv')
# dsorghum = pd.read_csv('Data/cycles/sorghum.csv')
## END LOCAL

dall = dmaize.append(dsorghum)
planting_dates =dall['planting_date'].unique()
planting_min = int(planting_dates.min())
planting_max = int(planting_dates.max())
locations = dall['location'].unique()

### *REMOVE* for live
###Config elements
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app.config.suppress_callback_exceptions = True
###

# Layout
app.layout = html.Div([
    html.Div([
        html.Div([
            html.P('Crop:'),
            dcc.Dropdown(id='dd_crop',
                options=[dict(label=x, value=x) for x in dall['crop'].unique()],
                value=dall['crop'].unique()[0]
                ),
        ],className="four columns"),
        html.Div([
            html.P('Year:'),
            dcc.Dropdown(id='dd_year',
                options=[dict(label=x, value=x) for x in dall['year'].unique()],
                value=dall['year'].unique()[0]
                #multi=True,
                #placeholder="Selct years. Shows all if none selected.",
                ),
        ],className="four columns"),
        html.Div([
                    html.P('Planting date range:'),
                    dcc.Slider(
                        id='s_planting',
                        min = planting_min,
                        max = planting_max,
                        marks={int(i):str(i) for i in planting_dates},
                        step=None,
                        value = planting_min
                    ),
        ],className="four columns"),
        html.Div([],className="three columns"),
    ],className="row"),
    html.Div([
            html.Div(id='graph')
    ],className="row"),

])

# Callbacks
@app.callback(
    Output('graph', 'children'),
    [Input('dd_crop', 'value'),Input('dd_year', 'value'),Input('s_planting', 'value')])
def update_figure(crop,year,planting):
    fig_list = []
    filtered_df = dall[(dall.crop == crop)&
        (dall['planting_date_fixed']==True)&(dall.year == year)&(dall.planting_date == planting)]
    filtered_df = filtered_df.sort_values('weed_fraction')
    n=0
    for l in locations:
        n=n+1
        ldata = filtered_df[filtered_df.location == l].sort_values('nitrogen_rate')
        graphid = 'graph-' + str(n)
        fig = px.line(
            ldata,
            x='nitrogen_rate',
            y='yield',
            color='weed_fraction',
            # colorscale="Viridis",
            height = 400,
        )
        fig.update_traces(mode='lines+markers')
        fig.update_layout(
            title_text=l,
                legend=go.layout.Legend(
                        x=.7,
                        y=0,
                        traceorder="normal",
                        font=dict(
                            family="sans-serif",
                            size=12,
                            color="black"
                        ),
                        bgcolor="LightSteelBlue",
                        bordercolor="Black",
                        borderwidth=2
                    )
        )
        lgraph = html.Div([dcc.Graph(
                        id=graphid,
                        figure=fig
                    )],style={'float':'left','width':'50%'})
        fig_list.append(lgraph)
    return fig_list

### REMOVE FOR LIVE
# if __name__ == '__main__':
#     app.run_server(debug=True,port=8080)
###
