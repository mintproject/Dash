# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go
import numpy as np



#Link to Econ Model Data
df = pd.read_csv(
    './Data/EconModel/results_summary_bycrop.csv')
#unique values of criteria
sp = df['p'].unique()
sc1 = df['c1'].unique()
sc2 = df['c2'].unique()

#unique values of p per crop
selected_variable = 'p'
scassava = df[df['crop']=='cassava'][selected_variable].unique()
sgroundnuts = df[df['crop']=='groundnuts'][selected_variable].unique()
smaize = df[df['crop']=='maize'][selected_variable].unique()
ssesame = df[df['crop']=='sesame'][selected_variable].unique()
ssorghum = df[df['crop']=='sorghum'][selected_variable].unique()

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    #Add radio buttons for what to adjust
    html.Div([
        dcc.RadioItems(
            id='r-variable',
            options=[
                {'label': 'C2', 'value': 'C2'},
                {'label': 'C1', 'value': 'C1'},
                {'label': 'P', 'value': 'P'}
            ],
            value='C2'
        )  
        ]),
   
    # turn this into returned html by callback
                    html.Div(id='s-variable'),
                    html.Div('sliders'),
                    html.Div([
                            html.Div(['Cassava'],className="three columns"),
                            html.Div([dcc.Slider(
                                id='sp-cassava',
                                min=int(scassava.min()),
                                max=int(scassava.max()),
                                marks={int(i):str(i) for i in scassava},
                                step=None,
                                value=0,
                            )],className="nine columns"),
                    ],className="row"),html.Br(),
                    html.Div([
                            html.Div(['Groundnuts'],className="three columns"),
                            html.Div([dcc.Slider(
                                id='sp-groundnuts',
                                min=int(sgroundnuts.min()),
                                max=int(sgroundnuts.max()),
                                marks={int(i):str(i) for i in sgroundnuts},
                                step=None,
                                value=0,
                            )],className="nine columns"),
                    ],className="row"),html.Br(),
                    html.Div([
                            html.Div(['Maize'],className="three columns"),
                            html.Div([dcc.Slider(
                                id='sp-maize',
                                min=int(smaize.min()),
                                max=int(smaize.max()),
                                marks={int(i):str(i) for i in smaize},
                                step=None,
                                value=0,
                            )],className="nine columns"),
                    ],className="row"),html.Br(),
                    html.Div([
                            html.Div(['Sesame'],className="three columns"),
                            html.Div([dcc.Slider(
                                id='sp-sesame',
                                min=int(ssesame.min()),
                                max=int(ssesame.max()),
                                marks={int(i):str(i) for i in ssesame},
                                step=None,
                                value=0,
                            )],className="nine columns"),
                    ],className="row"),html.Br(),
                    html.Div([
                            html.Div(['Sorghum'],className="three columns"),
                            html.Div([dcc.Slider(
                                id='sp-sorghum',
                                min=int(ssorghum.min()),
                                max=int(ssorghum.max()),
                                marks={int(i):str(i) for i in ssorghum},
                                step=None,
                                value=0,
                            )],className="nine columns"),
                    ],className="row"),html.Br(),
                    html.Div([
                            html.Div(['Set All Crops to:'],className="six columns"),
                            html.Div([dcc.Dropdown(
                                id='dd-p',
                                options = sorted([{'label': i, 'value': i} for i in sp],key = lambda x: x['label']),
                                value=0
                            )],className="six columns"),
                    ],className="row"),html.Br(),

    ])


#Update Sliders when dropdown resets all
@app.callback([Output('sp-cassava', 'value'),
              Output('sp-groundnuts', 'value'),
              Output('sp-maize', 'value'),
              Output('sp-sesame', 'value'),
              Output('sp-sorghum', 'value')],
              [Input('dd-p', 'value')])
def update_all_p(value):
    return value, value, value, value, value

#select proper Sliders set
@app.callback(
    Output(component_id='s-variable', component_property='children'),
    [Input(component_id='r-variable', component_property='value')]
)
def update_output_div(input_value):
    if input_value == 'P':
        return 'Adjust settings for {}'.format(input_value)
    else:
        return 'not p'


# @app.callback(Output('time-slider', 'children'), [Input('my-dropdown', 'value')])
# def change_range(dropdown_value): return slider_options(dropdown_value)
##@app.callback([
##    Output('sp-cassava', 'value'),
##    Output('data-table', 'data'),
##    Output('data-table', 'columns'),
##    Output('container', 'style')
##], [Input('data-dropdown', 'value')])
##def multi_output(value):
##    if value is None:
##        raise PreventUpdate
##
##    selected = sample_data[value]
##    data = selected['data']
##    columns = [
##        {'name': k.capitalize(), 'id': k}
##        for k in data[0].keys()
##    ]
##    figure = go.Figure(
##        data=[
##            go.Bar(x=[x['score']], text=x['title'], name=x['title'])
##            for x in data
##        ]
##    )
##
##    return figure, data, columns, selected['style']

if __name__ == '__main__':
    app.run_server(debug=True,port=8080)
