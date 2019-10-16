# dash libs
# libraries
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import json
import time
import base64
import datetime
import io

# dash libraries
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_html_components as html
import dash_core_components as dcc
import dash_table

# Plotting libraries
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# FOR LIVE
from viz.app import app
# FOR LIVE: IMPORT DATABASE
from viz.app import engine
#

#styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
'https://codepen.io/chriddyp/pen/brPBPO.css']

# ## LOCAL ONLY
# ##Config elements
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app.config.suppress_callback_exceptions = True
# ##

# Layout
layout = html.Div([
    html.Div(id='testdiv'),
    dcc.Store(id='s-cols'),
    dcc.Store(id='s-data'),
    dcc.Tabs(id="tabs", children=[
    dcc.Tab(label='Load Data', children=[
            html.H3('File Upload'),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                # multiple=True
            ),
            html.Div(id='output-data-upload'),
        ]),
        dcc.Tab(label='Scatter Plot', children=[
            # html.P('Add note to add data if none'),
            html.Div([
                html.Div([
                    html.P(['X Axis: ']),
                    dcc.Dropdown(id='dd-x'),
                    html.P(['Y Axis: ']),
                    dcc.Dropdown(id='dd-y'),
                    html.P(['Color: ']),
                    dcc.Dropdown(id='dd-color'),
                    html.P(['Facet Column: ']),
                    dcc.Dropdown(id='dd-facet_col'),
                    html.P(['Facet Row: ']),
                    dcc.Dropdown(id='dd-facet_row'),
                    html.P(['On Hover show: ']),
                    html.Div([dcc.Dropdown(id='dd-hover',multi=True)]),
                ],className='three columns'),
                html.Div([
                    dcc.Graph(id="graph_upload")
                ],className="nine columns")
            ],className='row')
        ]),
        # dcc.Tab(label='Parallel Coordinates', children=[
        #     # html.P('Add note to add data if none'),
        #     html.Div([],className='row')
        # ]),
    ])
])

## FUNCTIONS ##
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df


@app.callback([Output('output-data-upload', 'children'), Output('s-cols','data'), Output('s-data','data')],
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def update_output(contents, filename):
    if contents is None:
        raise PreventUpdate
    df = parse_contents(contents, filename)
    outputcontent = html.Div([
        html.H5(filename),
        dash_table.DataTable(
            id='dt',
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),
        html.Hr(),  # horizontal line
        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])
    cols = df.columns.values.tolist()
    sdata = df.to_dict('records')
    return outputcontent,cols,sdata

scatter_dropdowns = ['dd-x','dd-y','dd-color','dd-facet_col','dd-facet_row','dd-hover']
for dd in scatter_dropdowns:
    @app.callback(Output(dd,'options'),
                [Input('s-cols','data')])
    def scatter_options(cols):
        if cols is None:
            raise PreventUpdate
        col_options = [dict(label=x, value=x) for x in cols]
        return col_options

@app.callback(Output("graph_upload", "figure"),
                [Input('dd-x','value'),Input('dd-y','value'),Input('dd-color','value'),
                Input('dd-facet_col','value'),Input('dd-facet_row','value'),Input('dd-hover','value')]
                ,[State('s-data','data')])
def make_scatter(x, y, color, facet_col, facet_row, hover_info,sdata):
    if sdata is None:
        raise PreventUpdate
    data_graph = pd.DataFrame(sdata)
    fig = px.scatter(
        data_graph,
        x=x,
        y=y,
        color=color,
        facet_col=facet_col,
        facet_row=facet_row,
        height=700,
        hover_data = hover_info,
    )
    return fig

# ## LOCAL ONLY
# if __name__ == '__main__':
#     app.run_server(debug=True,port=8030)
# ##
