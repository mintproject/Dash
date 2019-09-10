# -*- coding: utf-8 -*-
from viz.app import app
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

from viz.app import app

#Link to Econ Model Data
df = pd.read_csv('./Data/EconModel/results_summary_bycrop_aggregate.csv')
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

#unique c2 subsidy values
sc2 = df['p'].unique()
c2cassava = df[df['crop']=='cassava']['p'].unique()
c2groundnuts = df[df['crop']=='groundnuts']['p'].unique()
c2maize = df[df['crop']=='maize']['p'].unique()
c2sesame = df[df['crop']=='sesame']['p'].unique()
c2sorghum = df[df['crop']=='sorghum']['p'].unique()

#unique p values
sp = df['p'].unique()
scassava = df[df['crop']=='cassava']['p'].unique()
sgroundnuts = df[df['crop']=='groundnuts']['p'].unique()
smaize = df[df['crop']=='maize']['p'].unique()
ssesame = df[df['crop']=='sesame']['p'].unique()
ssorghum = df[df['crop']=='sorghum']['p'].unique()

#unique productions cost values
sc1 = df['c1'].unique()
c1cassava = df[df['crop']=='cassava']['c1'].unique()
c1groundnuts = df[df['crop']=='groundnuts']['c1'].unique()
c1maize = df[df['crop']=='maize']['c1'].unique()
c1sesame = df[df['crop']=='sesame']['c1'].unique()
c1sorghum = df[df['crop']=='sorghum']['c1'].unique()


image_filename = "./images/ConceptMap_Econ.jpg"# replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Layout
app.layout = html.Div([
    html.H2('Economic Agricultural Data'),
    html.Div([
            html.Div([
            html.H5('Intervetion Variables'),
            html.Details([
                html.Summary('Fertilizer Subsidy (%)'),
                html.Div([
                    html.Div([
                            html.Div(['Cassava'],className="three columns"),
                            html.Div([dcc.Slider(
                                id='sc2-cassava',
                                min=int(c2cassava.min()),
                                max=int(c2cassava.max()),
                                marks={int(i):str(i) for i in c2cassava},
                                step=None,
                                value=0,
                            )],className="nine columns"),
                    ],className="row"),html.Br(),
                    html.Div([
                            html.Div(['Groundnuts'],className="three columns"),
                            html.Div([dcc.Slider(
                                id='sc2-groundnuts',
                                min=int(c2groundnuts.min()),
                                max=int(c2groundnuts.max()),
                                marks={int(i):str(i) for i in c2groundnuts},
                                step=None,
                                value=0,
                            )],className="nine columns"),
                    ],className="row"),html.Br(),
                    html.Div([
                            html.Div(['Maize'],className="three columns"),
                            html.Div([dcc.Slider(
                                id='sc2-maize',
                                min=int(c2maize.min()),
                                max=int(c2maize.max()),
                                marks={int(i):str(i) for i in c2maize},
                                step=None,
                                value=0,
                            )],className="nine columns"),
                    ],className="row"),html.Br(),
                    html.Div([
                            html.Div(['Sesame'],className="three columns"),
                            html.Div([dcc.Slider(
                                id='sc2-sesame',
                                min=int(c2sesame.min()),
                                max=int(c2sesame.max()),
                                marks={int(i):str(i) for i in c2sesame},
                                step=None,
                                value=0,
                            )],className="nine columns"),
                    ],className="row"),html.Br(),
                    html.Div([
                            html.Div(['Sorghum'],className="three columns"),
                            html.Div([dcc.Slider(
                                id='sc2-sorghum',
                                min=int(c2sorghum.min()),
                                max=int(c2sorghum.max()),
                                marks={int(i):str(i) for i in c2sorghum},
                                step=None,
                                value=0,
                            )],className="nine columns"),
                    ],className="row"),html.Br(),
                    html.Div([
                            html.Div(['Set All Crops to:'],className="six columns"),
                            html.Div([dcc.Dropdown(
                                id='dd-c2',
                                options = sorted([{'label': i, 'value': i} for i in sc2],key = lambda x: x['label']),
                                value=0
                            )],className="six columns"),
                    ],className="row"),html.Br(),

                    ])
            ]),
            html.H5('Economic Conditions'),
            html.Details([
                html.Summary('Crop Price'),
                html.Div([
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
                ]),
            ]),
            html.Details([
                html.Summary('Cost of Production (Non-fertilizer)'),
                html.Div([
                    html.Div([
                            html.Div(['Cassava'],className="three columns"),
                            html.Div([dcc.Slider(
                                id='sc1-cassava',
                                min=int(c1cassava.min()),
                                max=int(c1cassava.max()),
                                marks={int(i):str(i) for i in c1cassava},
                                step=None,
                                value=0,
                            )],className="nine columns"),
                    ],className="row"),html.Br(),
                    html.Div([
                            html.Div(['Groundnuts'],className="three columns"),
                            html.Div([dcc.Slider(
                                id='sc1-groundnuts',
                                min=int(c1groundnuts.min()),
                                max=int(c1groundnuts.max()),
                                marks={int(i):str(i) for i in c1groundnuts},
                                step=None,
                                value=0,
                            )],className="nine columns"),
                    ],className="row"),html.Br(),
                    html.Div([
                            html.Div(['Maize'],className="three columns"),
                            html.Div([dcc.Slider(
                                id='sc1-maize',
                                min=int(c1maize.min()),
                                max=int(c1maize.max()),
                                marks={int(i):str(i) for i in c1maize},
                                step=None,
                                value=0,
                            )],className="nine columns"),
                    ],className="row"),html.Br(),
                    html.Div([
                            html.Div(['Sesame'],className="three columns"),
                            html.Div([dcc.Slider(
                                id='sc1-sesame',
                                min=int(c1sesame.min()),
                                max=int(c1sesame.max()),
                                marks={int(i):str(i) for i in c1sesame},
                                step=None,
                                value=0,
                            )],className="nine columns"),
                    ],className="row"),html.Br(),
                    html.Div([
                            html.Div(['Sorghum'],className="three columns"),
                            html.Div([dcc.Slider(
                                id='sc1-sorghum',
                                min=int(c1sorghum.min()),
                                max=int(c1sorghum.max()),
                                marks={int(i):str(i) for i in c1sorghum},
                                step=None,
                                value=0,
                            )],className="nine columns"),
                    ],className="row"),html.Br(),
                    html.Div([
                            html.Div(['Set All Crops to:'],className="six columns"),
                            html.Div([dcc.Dropdown(
                                id='dd-c1',
                                options = sorted([{'label': i, 'value': i} for i in sc1],key = lambda x: x['label']),
                                value=0
                            )],className="six columns"),
                    ],className="row"),html.Br(),
                ])

                ]),html.Br(),
            ],className="three columns"),
    html.Div([
                    dcc.Tabs(id="tabs", value='tab-1', children=[
                        dcc.Tab(label='Visualize', value='tab-1'),
                        dcc.Tab(label='Model Cag', value='tab-2'),
                    ]),
                    html.Div(id='tabs-content')
                ],className="nine columns" ),
    ],className="row")        
])


#Interactive Callback components

#Update Sliders when dropdown resets all
@app.callback([Output('sp-cassava', 'value'),
              Output('sp-groundnuts', 'value'),
              Output('sp-maize', 'value'),
              Output('sp-sesame', 'value'),
              Output('sp-sorghum', 'value')],
              [Input('dd-p', 'value')])
def update_all_p(value):
    return value, value, value, value, value

@app.callback([Output('sc1-cassava', 'value'),
              Output('sc1-groundnuts', 'value'),
              Output('sc1-maize', 'value'),
              Output('sc1-sesame', 'value'),
              Output('sc1-sorghum', 'value')],
              [Input('dd-c1', 'value')])
def update_all_p(value):
    return value, value, value, value, value

@app.callback([Output('sc2-cassava', 'value'),
              Output('sc2-groundnuts', 'value'),
              Output('sc2-maize', 'value'),
              Output('sc2-sesame', 'value'),
              Output('sc2-sorghum', 'value')],
              [Input('dd-c2', 'value')])
def update_all_p(value):
    return value, value, value, value, value

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Div([
            dcc.Graph(id='basic-graph'),
                ])
            ],className="row")
    elif tab == 'tab-2':
        return html.Div([
             html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
        ])
##    elif tab == 'tab-3':
##        return html.Div([
##            html.H3('Data Table'),
##            generate_table(df)
##        ])

@app.callback(Output('basic-graph', 'figure'),
              [Input('dd-c1', 'value'),Input('dd-p', 'value')])
def update_figure(c1value,pvalue):
    dff=df[(df['p']==pvalue)&(df['c1']==c1value)]
    return {
        'data': [go.Scatter(
            x = dff['c2'], #x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y = dff['yield_kg-ha'], #y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text= dff['crop'], #text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'c1' #xaxis_column_name,
            },
            yaxis={
                'title': 'Yield' #yaxis_column_name,
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

##def update_figure():
##    filtered_df = df
##    traces = []
##    for i in filtered_df.crop.unique():
##        df_by_crop = filtered_df[filtered_df['crop'] == i]
##        traces.append(go.Scatter(
##            x=df_by_crop['p'],
##            y=df_by_crop['c1'],
##            text=df_by_crop['c2'],
##            mode='markers',
##            opacity=0.7,
##            marker={
##                'size': 15,
##                'line': {'width': 0.5, 'color': 'white'}
##            },
##            name=i
##        ))
##
##    return {
##        'data': traces,
##        'layout': go.Layout(
##            xaxis={'title': 'crop price'},
##            yaxis={'title': 'cost of production'},
##            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
##            legend={'x': 0, 'y': 1},
##            hovermode='closest'
##        )
##    }


if __name__ == '__main__':
    app.run_server(debug=True,port=8080)
