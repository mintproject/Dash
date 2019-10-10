# dash libs
import collections
import dash
import pandas as pd
from sqlalchemy import create_engine

# dash interactive states
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# dash components
import dash_html_components as html
import dash_core_components as dcc
import dash_table

# Plotly figure libraries
import plotly.express as px

# set connection string
user = 'user'
password = 'password'
DATABASE_URI = 'postgres+psycopg2://{}:{}@localhost:5432/dataviz'.format(user,password)
con = create_engine(DATABASE_URI)

#styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dimensions = ["x", "y", "color", "facet_col", "facet_row"]
dgraph = dimensions + ['hover-dropdown']
user_cols = {'':{},
                'cycles':{'crop', 'location',
                'planting_date', 'nitrogen_rate', 'weed_fraction', 'yield',
                'year','unique_id'},
                'economic':{}}

#Config elements
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

tables = ['cycles']
# Layout

app.layout = html.Div([
    dcc.Store(id='s-cols'),
    dcc.Store(id='s-data'),
    html.Div([
        html.Div([
            html.P(['Datasource: ']),
            dcc.Dropdown(id='dd-table',
                options=[dict(label=x, value=x) for x in tables]
                ),
            html.Button('Show Data', id='btn-table'),
            html.P(['X Axis: ']),
            dcc.Dropdown(id='dd-x',options=[]),
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
            # html.Div(id='collist'),
            # dcc.Dropdown(id='dd-cols'),
            # html.Div(id='table'),
            html.Div(id='test'),
            html.Div([
                html.Button('Build Graph', id='btn-graph'),
            ],style={'float':'right'})
        ],className="four columns"),
        html.Div([
            dcc.Graph(id='g-scatter')
        ],className="eight columns")
    ], className="row"),
    html.Div([
        html.Div(id='dt-table')
    ],className="row")
])

# Callbacks
# Query SQL for selected table to generate columns list
@app.callback([Output('s-cols', 'data'),Output('s-data', 'data')],
              [Input("dd-table", "value")],
              [State('s-cols', 'data'),State('s-data', 'data')]
              )
def update_cols(table, cols, data):
    if table is None or table == '':
        raise PreventUpdate
    col_list = list(user_cols[table])
    col_list.sort(key=str.lower)
    select_cols = ", ".join(list(col_list))
    query = 'SELECT {} FROM {}'.format(select_cols,table)
    dataf = pd.read_sql(query,con)
    return [col_list, dataf.to_dict('records')]

@app.callback(Output('dt-table', 'children'),
    [Input('btn-table', 'n_clicks')],
    [State('s-data', 'data')]
    )
def show_data(n_clicks,sdata):
    if n_clicks is None:
        raise PreventUpdate
    tabledata = pd.DataFrame(sdata)
    dt = [dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in tabledata.columns],
            data=tabledata.to_dict('records'),
        )]
    return dt

#Update options for all graph component elements
for d in ('dd-x','dd-y','dd-color','dd-facet_col','dd-facet_row','dd-hover'):
    @app.callback(
        Output(d, "options"),
          [Input('s-cols', 'modified_timestamp')],
          [State('s-cols', 'data')])
    def update_dropdown(ts, col_list):
        if ts is None:
            raise PreventUpdate
        data_options = [{"label": i, "value":i} for i in col_list]
        return data_options

if __name__ == '__main__':
    app.run_server(debug=True,port=8060)
