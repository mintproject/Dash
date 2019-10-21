## FOR LIVE
from viz.utils import *
##

#styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
'https://codepen.io/chriddyp/pen/brPBPO.css']

## LAYOUT ##
def generate_layout():
    try:
        thread_id
    except NameError:
        thread_id = ''
        # 'b2oR7iGkFEzVgimbNZFO'
    sdata=''
    if thread_id != '':
        # if there is a thread, load the data into the data store
        # tablename = 'cycles_0_9_4_alpha__runs'
        # query = """SELECT crop_name, fertilizer_rate, start_planting_day, weed_fraction, latitude, longitude,start_year,end_year,location
        #         FROM
        #         (Select id, x as longitude, y as latitude, CONCAT(ROUND(y::numeric,2)::text ,'Nx',ROUND(x::numeric,2)::text ,'E') as location
        #         FROM threads_inputs where threadid = '{}') ti
        #         INNER JOIN
        #         (select * from {} where threadid = '{}') i
        #         ON ti.id = i.cycles_weather;""".format(thread_id,tablename,thread_id)
        # df = pd.DataFrame(pd.read_sql(query,con))
        sdata = 'Got a thread here!'
    return html.Div([
        dcc.Store(id='s-cols'),
        dcc.Store(id='s-data'),
        dcc.Tabs(id="tabs", children=[
            dcc.Tab(label='Load Data', children=[
                html.Div([
                    html.Label('Thread id'),
                    dcc.Input(id='cycles_thread_id', value=thread_id, type='text', style={"width": "33%"}),
                ]),
                html.Div(check_data(thread_id)),
            ]),
            dcc.Tab(label='Scatter', children=[
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
                        html.Div([html.Button('Build Graph', id='btn-scatter')]),
                    ],className='three columns'),
                    html.Div([
                        dcc.Graph(id='graph-scatter')
                    ],className="nine columns"),
                ],className='row')
            ]),
            dcc.Tab(label='Parallel', children=[]),
        ]),
        html.Div(id='stores'),
    ])


## FUNCTIONS ##
# Check and Load data
def check_data(thread_id):
    if thread_id is None or thread_id == '':
        children = upload_file()
    else:
        children = 'You have loaded data for the thread: ' + thread_id
    return children

def store_data(dataframe):
    scols = dataframe.columns.values.tolist()
    sdata = dataframe.to_dict('records')
    return scols, sdata

# Upload data
def upload_file():
    children = [html.H3('File Upload'),
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
                html.Div(id='output-data-upload')]
    return children

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


## CALLBACKS ##
# Upload data into data stores
@app.callback([Output('s-cols','data'),Output('s-data','data')],
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def update_output(contents, filename):
    if contents is None:
        raise PreventUpdate
    df = parse_contents(contents, filename)
    return store_data(df)

# Build dropdowns for Scatte plot
scatter_dropdowns = ['dd-x','dd-y','dd-color','dd-facet_col','dd-facet_row','dd-hover']
for dd in scatter_dropdowns:
    @app.callback(Output(dd,'options'),
                [Input('s-cols','data')])
    def scatter_options(cols):
        if cols is None:
            raise PreventUpdate
        col_options = [dict(label=x, value=x) for x in cols]
        return col_options

# Build Scatter graph
@app.callback(Output("graph-scatter", "figure"),
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

