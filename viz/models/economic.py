import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import numpy as np

from viz.app import app

#Link to Barton Springs Data
df = pd.read_csv(
    './Data/EconModel/'
    'results_summary_bycrop.csv')
dp = df['p'].unique()
dc1 = df['c1'].unique()
dc2 = df['c2'].unique()
dcassava = df[df['crop']=='cassava']['p'].unique()
dgroundnuts = df[df['crop']=='groundnuts']['p'].unique()
dmaize = df[df['crop']=='maize']['p'].unique()
dsesame = df[df['crop']=='sesame']['p'].unique()
dsorghum = df[df['crop']=='sorghum']['p'].unique()
#'groundnuts', 'maize', 'sesame', 'sorghum', 'cassava']

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


layout = html.Div([
    html.H1(children='Economic Agricultural Data'),
    html.Div([        
        html.H3('COSTS'),
        html.H5(id='slider-output-c1'),
        #html.Div(id='slider-output-c1',style={'float': 'left'}),
        html.Div(dcc.Slider(
            id='slider-c1',
            min=int(dc1.min()),
            max=int(dc1.max()),
            marks={int(i):str(i) for i in dc1},
            step=None,
            value=0,
        ),style={'clear': 'both'}),
        html.H1(' '),
        
        html.H5(id='slider-output-c2'),
        dcc.Slider(
            id='slider-c2',
            min=int(dc2.min()),
            max=int(dc2.max()),
            marks={int(i):str(i) for i in dc2},
            step=None,
            value=0,
        ),
        html.H1(' '),
        
        html.H3('CROP PRICES'),
        html.H5(id='slider-output-p-cassava'),
        dcc.Slider(
            id='slider-p-cassava',
            min=int(dcassava.min()),
            max=int(dcassava.max()),
            marks={int(i):str(i) for i in dcassava},
            step=None,
            value=0,
        ),
        html.H1(' '),
        html.H5(id='slider-output-p-groundnuts'),
        dcc.Slider(
            id='slider-p-groundnuts',
            min=int(dgroundnuts.min()),
            max=int(dgroundnuts.max()),
            marks={int(i):str(i) for i in dgroundnuts},
            step=None,
            value=0,
        ),
        html.H1(' '),
        html.H5(id='slider-output-p-maize'),
        dcc.Slider(
            id='slider-p-maize',
            min=int(dmaize.min()),
            max=int(dmaize.max()),
            marks={int(i):str(i) for i in dmaize},
            step=None,
            value=0,
        ),
        html.H1(' '),
        html.H5(id='slider-output-p-sesame'),
        dcc.Slider(
            id='slider-p-sesame',
            min=int(dsesame.min()),
            max=int(dsesame.max()),
            marks={int(i):str(i) for i in dsesame},
            step=None,
            value=0,
        ),
        html.H1(' '),
        html.H5(id='slider-output-p-sorghum'),
        dcc.Slider(
            id='slider-p-sorghum',
            min=int(dsorghum.min()),
            max=int(dsorghum.max()),
            marks={int(i):str(i) for i in dsorghum},
            step=None,
            value=0,
        ),
        html.H1(' ')                     
    ],style={'float':'left','width':'20%','margin':'10px'}),
    html.Div([
        dcc.Tabs(id="tabs", value='tab-5', children=[
            dcc.Tab(label='Yield', value='tab-1'),
            dcc.Tab(label='Production', value='tab-2'),
            dcc.Tab(label='Fertilizer Application', value='tab-3'),
            dcc.Tab(label='Land Allocation', value='tab-4'),
            dcc.Tab(label='Data', value='tab-5'),
        ]),
        html.Div(id='tabs-content')
    ],style={'float':'left','width':'75%','margin':'10px'}),
])

@app.callback(
    dash.dependencies.Output('slider-output-c1', 'children'),
    [dash.dependencies.Input('slider-c1', 'value')])
def update_output(value):
    return 'Land Cost: {}'.format(value)

@app.callback(
    dash.dependencies.Output('slider-output-c2', 'children'),
    [dash.dependencies.Input('slider-c2', 'value')])
def update_output(value):
    return 'Nitrogen Fertilizer Cost: {}'.format(value)

@app.callback(
    dash.dependencies.Output('slider-output-p-cassava', 'children'),
    [dash.dependencies.Input('slider-p-cassava', 'value')])
def update_output(value):
    return 'Cassava: {}'.format(value)

@app.callback(
    dash.dependencies.Output('slider-output-p-groundnuts', 'children'),
    [dash.dependencies.Input('slider-p-groundnuts', 'value')])
def update_output(value):
    return 'Groundnuts: {}'.format(value)

@app.callback(
    dash.dependencies.Output('slider-output-p-maize', 'children'),
    [dash.dependencies.Input('slider-p-maize', 'value')])
def update_output(value):
    return 'Maize: {}'.format(value)

@app.callback(
    dash.dependencies.Output('slider-output-p-sesame', 'children'),
    [dash.dependencies.Input('slider-p-sesame', 'value')])
def update_output(value):
    return 'Sesame: {}'.format(value)

@app.callback(
    dash.dependencies.Output('slider-output-p-sorghum', 'children'),
    [dash.dependencies.Input('slider-p-sorghum', 'value')])
def update_output(value):
    return 'Sorghum: {}'.format(value)


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Yield')
            ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Production')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Fertilizer Application')
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Land Allocation')
        ])
    elif tab == 'tab-5':
        return html.Div([
            html.H3('Data Table'),
            generate_table(df)
        ])
