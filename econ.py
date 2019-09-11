# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import base64

#Link to Econ Model Data
df = pd.read_csv('./Data/EconModel/results_summary_bycrop_aggregate.csv')

#unique values for dropdowns
dp = df['p'].unique()
dc1 = df['c1'].unique()
#Dropdown to select y axis
available_indicators = df.select_dtypes(include=['float64']).columns

##crop               55 non-null object
##p                  55 non-null int64
##c1                 55 non-null int64
##c2                 55 non-null int64
##land_area_ha       55 non-null float64
##yield_kg_per_ha    55 non-null float64
##production_kg      55 non-null float64
##nuse_kg            55 non-null float64
##nfert_kg_per_ha    55 non-null float64

#Split data by crop
dcassava = df[df['crop']=='cassava']
dgroundnuts = df[df['crop']=='groundnuts']
dmaize = df[df['crop']=='maize']
dsesame = df[df['crop']=='sesame']
dsorghum = df[df['crop']=='sorghum']

#Config elements
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

image_filename = "./assets/images/ConceptMap_Econ.jpg"# replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Resuable functions
def update_scatter(dataframe, yaxis):
    return {
        'data': [
            go.Scatter(
                x=dataframe[dataframe['crop'] == i]['c2'],
                y=dataframe[dataframe['crop'] == i][yaxis],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 8,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in df.crop.unique()
        ],
        'layout': go.Layout(
            legend={'orientation':'h'},
            hovermode='closest'
        )
    }

# Layout
app.layout = html.Div([
    html.H2('Economic Agricultural Data'),
        dcc.Dropdown(
            id='crossfilter-yaxis-column',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value='production_kg'
            ),
    html.Div([
        html.Div([
            html.H4('Scenario 1'),
            html.Div([
                    html.Div(['P'],className="two columns"),
                    html.Div([dcc.Slider(
                        id='s1p',
                        min=int(dp.min()),
                        max=int(dp.max()),
                        marks={int(i):str(i) for i in dp},
                        step=None,
                        value=0,
                    )],className="ten columns"),
            ],className="row"),html.Br(),
            html.Div([
                    html.Div(['C1'],className="two columns"),
                    html.Div([dcc.Slider(
                        id='s1c1',
                        min=int(dc1.min()),
                        max=int(dc1.max()),
                        marks={int(i):str(i) for i in dc1},
                        step=None,
                        value=0,
                    )],className="ten columns"),
            ],className="row"),html.Br(),
            dcc.Graph(id='s1-graph'),
        ],className="four columns"),
        html.Div([
            html.H4('Scenario 2'),
            html.Div([
                    #html.Div(['P'],className="two columns"),
                    html.Div([dcc.Slider(
                        id='s2p',
                        min=int(dp.min()),
                        max=int(dp.max()),
                        marks={int(i):str(i) for i in dp},
                        step=None,
                        value=0,
                    )],className="ten columns"),
            ],className="row"),html.Br(),
            html.Div([
                    #html.Div(['C1'],className="two columns"),
                    html.Div([dcc.Slider(
                        id='s2c1',
                        min=int(dc1.min()),
                        max=int(dc1.max()),
                        marks={int(i):str(i) for i in dc1},
                        step=None,
                        value=0,
                    )],className="ten columns"),
            ],className="row"),html.Br(),
            dcc.Graph(id='s2-graph'),
        ],className="four columns"),
        html.Div([
            html.H4('Scenario 3'),
            html.Div([
                    #html.Div(['P'],className="two columns"),
                    html.Div([dcc.Slider(
                        id='s3p',
                        min=int(dp.min()),
                        max=int(dp.max()),
                        marks={int(i):str(i) for i in dp},
                        step=None,
                        value=0,
                    )],className="ten columns"),
            ],className="row"),html.Br(),
            html.Div([
                    #html.Div(['C1'],className="two columns"),
                    html.Div([dcc.Slider(
                        id='s3c1',
                        min=int(dc1.min()),
                        max=int(dc1.max()),
                        marks={int(i):str(i) for i in dc1},
                        step=None,
                        value=0,
                    )],className="ten columns"),
            ],className="row"),html.Br(),
            dcc.Graph(id='s3-graph'),
        ],className="four columns"),

    ],id="scenarios-display", className="row"),
])

#Update graphs with Sliders
@app.callback(
    Output('s1-graph', 'figure'),
    [Input('s1p', 'value'), Input('s1c1', 'value'),Input('crossfilter-yaxis-column', 'value') ])
def update_figure(p, c1, yaxis):
    dfiltered = df[(df['p']==p)&(df['c1']==c1)]
    return update_scatter(dfiltered, yaxis)

@app.callback(
    Output('s2-graph', 'figure'),
    [Input('s2p', 'value'), Input('s2c1', 'value'),Input('crossfilter-yaxis-column', 'value') ])
def update_figure(p, c1, yaxis):
    dfiltered = df[(df['p']==p)&(df['c1']==c1)]
    return update_scatter(dfiltered, yaxis)

@app.callback(
    Output('s3-graph', 'figure'),
    [Input('s3p', 'value'), Input('s3c1', 'value'),Input('crossfilter-yaxis-column', 'value') ])
def update_figure(p, c1, yaxis):
    dfiltered = df[(df['p']==p)&(df['c1']==c1)]
    return update_scatter(dfiltered, yaxis)


if __name__ == '__main__':
    app.run_server(debug=True,port=8080)
