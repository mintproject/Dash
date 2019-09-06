# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

#Link to Econ Model Data
df = pd.read_csv('./Data/EconModel/results_summary_bycrop.csv')
#Config elements
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

#unique values for sliders
sc1 = df['c1'].unique()
sc2 = df['c2'].unique()

#unique fertilizer subsidy values
fall = df['p'].unique()
fcassava = df[df['crop']=='cassava']['p'].unique()
fgroundnuts = df[df['crop']=='groundnuts']['p'].unique()
fmaize = df[df['crop']=='maize']['p'].unique()
fsesame = df[df['crop']=='sesame']['p'].unique()
fsorghum = df[df['crop']=='sorghum']['p'].unique()

#unique p values
sp = df['p'].unique()
scassava = df[df['crop']=='cassava']['p'].unique()
sgroundnuts = df[df['crop']=='groundnuts']['p'].unique()
smaize = df[df['crop']=='maize']['p'].unique()
ssesame = df[df['crop']=='sesame']['p'].unique()
ssorghum = df[df['crop']=='sorghum']['p'].unique()

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

# Layout
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H2('Economic Agricultural Data'),
            html.H5('Intervetion Variables'),
            html.Details([
                html.Summary('Fertilizer Subsidy (%)'),
                html.Div([
html.Div([
	html.Div(['ALL CROPS'],className="three columns"),
	html.Div(['Slider'],className="nine columns"),
],className="row"),
html.Div([
	html.Div(['Cassava'],className="three columns"),
	html.Div(['Slider'],className="nine columns"),
],className="row"),
html.Div([
	html.Div(['Groundnuts'],className="three columns"),
	html.Div(['Slider'],className="nine columns"),
],className="row"),
html.Div([
	html.Div(['Maize'],className="three columns"),
	html.Div(['Slider'],className="nine columns"),
],className="row"),
html.Div([
	html.Div(['Sesame'],className="three columns"),
	html.Div(['Slider'],className="nine columns"),
],className="row"),
html.Div([
	html.Div(['Sorghum'],className="three columns"),
	html.Div(['Slider'],className="nine columns"),
],className="row")
                    ])
            ]),
            html.H5('Economic Conditions'),
            html.Details([
                html.Summary('Crop Price'),
                html.Div([
html.Div([
	html.Div(['ALL CROPS'],className="three columns"),
	html.Div([dcc.Slider(
            id='sp-all',
            min=int(sp.min()),
            max=int(sp.max()),
            marks={int(i):str(i) for i in sp},
            step=None,
            value=0,
        )],className="nine columns"),
],className="row"),html.Br(),
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
],className="row"),html.Br()
                    ])
            ]),
            html.Details([
                html.Summary('Cost of Production (Non-fertilizer)'),
                html.Div([
html.Div([
	html.Div(['ALL CROPS'],className="three columns"),
	html.Div(['Slider'],className="nine columns"),
],className="row"),
html.Div([
	html.Div(['Cassava'],className="three columns"),
	html.Div(['Slider'],className="nine columns"),
],className="row"),
html.Div([
	html.Div(['Groundnuts'],className="three columns"),
	html.Div(['Slider'],className="nine columns"),
],className="row"),
html.Div([
	html.Div(['Maize'],className="three columns"),
	html.Div(['Slider'],className="nine columns"),
],className="row"),
html.Div([
	html.Div(['Sesame'],className="three columns"),
	html.Div(['Slider'],className="nine columns"),
],className="row"),
html.Div([
	html.Div(['Sorghum'],className="three columns"),
	html.Div(['Slider'],className="nine columns"),
],className="row")
                    ])
            ])
        ], className="four columns"),

        html.Div([
            dcc.Tabs(id="tabs", value='tab-1', children=[
                dcc.Tab(label='Visualize', value='tab-1'),
                dcc.Tab(label='Model Cag', value='tab-2'),
                dcc.Tab(label='Data', value='tab-3'),
            ]),
            html.Div(id='tabs-content')
        ], className="eight columns"),
    ], className="row")
])


#Interactive Callback components
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Data Viz'),
            html.Div(id='testdiv')
            ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('CAG')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Data Table'),
            generate_table(df)
        ])


if __name__ == '__main__':
    app.run_server(debug=True,port=8080)
