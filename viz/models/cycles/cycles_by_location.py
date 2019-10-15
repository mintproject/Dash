# dash libs
# import collections
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import json
import time

# dash interactive states
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# dash components
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt

# Plotting graphics
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

## FOR LIVE
# from viz.app import app
##

#styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
'https://codepen.io/chriddyp/pen/brPBPO.css']

# set connection string
user = 'viz'
password = 'Zc2D63rSbIko6d'
DATABASE_URI = 'postgres+psycopg2://{}:{}@aws1.mint.isi.edu:5432/publicingestion'.format(user,password)
con = create_engine(DATABASE_URI)


## threadid.  Change to get this from url when avilable.
thread_id = 'b2oR7iGkFEzVgimbNZFO'

## LOCAL ONLY
##Config elements
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
##

# Layout
app.layout = html.Div([
    dcc.Store(id='s-settings'),
    html.Div([
        html.Div([
            html.P('CROP'),
            dcc.Dropdown(id='dd_crop'),
            html.P('PLANTING START DATE'),
            dcc.Dropdown(id='dd_planting'),
        ],className="four columns"),
        html.Div([
            html.P('LOCATIONS'),
            dcc.Dropdown(id='dd_locations',multi=True),
        ],className="eight columns"),
    ],className="row"),
    html.Div([
        html.Div([
            html.P('YEAR'),
        ],className="one columns"),
        html.Div([
            html.Div(id='rs_year'),
        ],className="eleven columns"),
    ],className="row"),
    html.Div([
        dcc.Loading(id='l-graph',children=[
            html.Div(id='graph')
        ],type="circle"),
    ],className="row"),
    html.Div(id='testdiv'),
])


# Callbacks
@app.callback(
    [Output('dd_crop','options'),Output('dd_crop','value'),
    Output('dd_locations','options'),Output('dd_locations','value'),
    Output('dd_planting','options'), Output('dd_planting','value')
    ,Output('rs_year','children')
    ],
    [Input('s-settings','data')]
    )
def set_dropdowns(settings):
    if thread_id is None or thread_id == '':
        raise PreventUpdate
    tablename = 'public."cycles-0.9.4-alpha-advanced-pongo-weather"'
    query = """select crop_name, fertilizer_rate, start_planting_day, start_year, end_year, weed_fraction, location
                from {} WHERE threadid = '{}';""".format(tablename,thread_id)
    df = pd.DataFrame(pd.read_sql(query,con))
    crops = df.crop_name.unique()
    crop_options = [dict(label=x, value=x) for x in sorted(crops)]
    planting_starts = df.start_planting_day.unique()
    planting_options =[dict(label=x, value=x) for x in planting_starts]
    locations = df.location.unique()
    location_options = [dict(label=x, value=x) for x in sorted(locations)]
    start_year = df.start_year.min()
    end_year = df.end_year.max()
    year_options = [dict(label=x, value=x) for x in range(start_year, end_year)]
    testdiv = 'years: {} - {}'.format(start_year, end_year)
    yearslider =dcc.Slider(
                id='rs_year',
                min=start_year,
                max=end_year,
                marks={i: '{}'.format(i) for i in range(start_year,end_year)},
                step=None,
                value=start_year
            ),

    return [crop_options,crops[0],
            location_options,locations[0:3],
            planting_options,planting_starts[0],
            yearslider]

@app.callback(
    Output('testdiv','children'),
    #  Output('graph', 'children'),
    [Input('dd_crop','value'),Input('dd_locations','value'), Input('dd_planting','value'), Input('rs_year','value')]
     )
def update_figure(crop,locations,planting,year):
    for item in (crop,locations,planting,year):
        if item is None or item == '':
            # raise PreventUpdate
            return "Please ensure all variables are selected"
    ins = 'public."cycles-0.9.4-alpha-advanced-pongo-weather"'
    outs = 'public."cycles-0.9.4-alpha-advanced-pongo-weather_cycles_season"'
    if isinstance(locations, list):
        location_list = "','".join(list(locations))
        location_list = "'" + location_list + "'"
    else:
        location_list = "'" + locations + "'"
    query="""SELECT * FROM (SELECT ins.*, outs.grain_yield, EXTRACT(year FROM TO_DATE(outs.date, 'YYYY-MM-DD')) AS year from
        (
        SELECT * FROM {}
        WHERE crop_name LIKE '{}' AND start_planting_day = {} AND location IN ({})) ins
        LEFT JOIN {} outs ON ins."mint-runid" = outs."mint-runid") inout
        WHERE inout.year = {}""".format(ins,crop,planting,location_list,outs,year)
    figdata = pd.DataFrame(pd.read_sql(query,con))
#     return "{}".format(len(figdata))
#
# @app.callback(
#     Output('graph', 'children'),
#     [Input('s-inputs','data'),Input('s-otput')]
#     # [Input('dd_crop', 'value'),Input('dd_year', 'value'),Input('s_planting', 'value')])
# def update_figure(crop,year,planting):

    fig_list = []
    filtered_df = figdata.sort_values('weed_fraction')
#     columns: threadid
# mint-runid
# cycles_weather
# crop_name
# end_planting_day
# end_year
# fertilizer_rate
# start_planting_day
# start_year
# weed_fraction
# location
# grain_yield
# year
    n=0
    for l in locations:
        n=n+1
        ldata = filtered_df[filtered_df.location == l].sort_values('fertilizer_rate')
        graphid = 'graph-' + str(n)
        fig = px.line(
            ldata,
            x='fertilizer_rate',
            y='grain_yield',
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

## LOCAL ONLY
if __name__ == '__main__':
    app.run_server(debug=True,port=8080)
##
