## FOR LIVE
from viz.utils import *

#styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
'https://codepen.io/chriddyp/pen/brPBPO.css']


# Layout
def generate_layout(thread_id):
    activetab='scatter'
    if thread_id is None or thread_id == '':
        activetab='data'
    dlayout = html.Div([
        # Data Stores
        dcc.Store(id='upload-s-cols'),
        dcc.Store(id='upload-s-num'),
        dcc.Store(id='upload-s-data'),
        dcc.Store(id='upload-s-selectedpoints'),
        #Test DIV
        html.Div(id='testdiv'),
        # Layout Elements
        html.Div([
            html.Div([
                html.H4('Upload and Visualize Data'),
            ],className="six columns"),
            html.Div(id='uploadInfo',className='five columns',style={'float':'right','margin-top':'30px'}),
        ],className='row'),
        html.Div([
            dcc.Tabs(id="tabs", value=activetab,
                children=[
                dcc.Tab(label='Data', value='data',children=[
                    html.Div([
                        html.Label('Thread id'),
                        dcc.Input(id='thread_id', value=thread_id, type='text', style={"width": "33%"}),
                    ]),
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files'),
                            ' to upload or change data '
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
                ]),
                dcc.Tab(label='Scatter / Line', value='scatter', children=[
                    html.Div([
                        html.P(['X Axis: ']),
                        dcc.Dropdown(id='upload-x'),
                        html.P(['Y Axis: ']),
                        dcc.Dropdown(id='upload-y'),
                        html.P(['Color: ']),
                        dcc.Dropdown(id='upload-color'),
                        html.P(['Facet Column: ']),
                        dcc.Dropdown(id='upload-facet_col'),
                        html.P(['Facet Row: ']),
                        dcc.Dropdown(id='upload-facet_row'),
                        html.P(['On Hover show: ']),
                        html.Div([dcc.Dropdown(id='upload-hover',multi=True)]),
                        html.Button('Draw Graph', id='btn-scatter'),
                    ],style={'float':'left','width':'25%'}),
                    html.Div(id='upload-div-scatter',style={'float':'left','width':'75%'}),
                ]),
                dcc.Tab(label='Parallel', value='parallel', children=[
                    html.Div([
                        html.H3('Parallel Coordinates Graph'),
                        html.P('Scale: '),
                        dcc.Dropdown(
                            id='dd_pcoord_scale',
                            # options=[dict(label=x, value=x) for x in sorted(ncols)]
                        ),
                        html.P('Columns to show: '),
                        dcc.Checklist(
                            id='cl_pcoord',
                            # options=[dict(label=x, value=x) for x in sorted(ncols)]
                        ),
                        html.Button('Build Graph', id='btn-pcoord')
                    ],style={'float':'left','width':'25%'}),
                    html.Div(id='upload-div-parallel',style={'float':'left','width':'75%'}),
                ]),
                dcc.Tab(label='Map',value='map',children=[
                    html.P(['Generate a map of the data if it includes a latitude and longitude column'],className='row'),
                    html.Div([
                        html.Div(['Latitude Column:'],className='two columns'),
                        html.Div([dcc.Dropdown(id='upload-lat-selector')],className='three columns'),
                        html.Div(['Longitude Column:'],className='two columns'),
                        html.Div([dcc.Dropdown(id='upload-lon-selector')],className='three columns'),
                        html.Div([html.Button('Build Map', id='btn-map')],className='two columns')
                    ],className='row'),
                    html.Div([
                        html.Div(id='upload-map')
                    ],className='row'),
                ]),
            ])
        ],className='row'),
        html.Div([
            html.Div(id='upload-datatable'),
        ],className='row',style={'border-top':'2px solid black','margin-top':'20px','padding-top':'20px'}),
    ])
    return dlayout

## FUNCTIONS ##
# Load thread data if threadid is supplied
def fix_dbname(name):
    return name.strip().lower().replace(' ', '_').replace('(',
        '').replace(')', '').replace('%', 'percentage').replace('/',
        '_per_').replace('.', '_').replace('-', '_')

def load_thread_data(thread_id):
    if thread_id != None and thread_id != None:
        meta_query = "SELECT metadata FROM threads WHERE threadid='{}'".format(thread_id)
        meta_df = pd.DataFrame(pd.read_sql(meta_query, con))
        if meta_df.empty:
            print("Thread doesn't exist")
            return None
        meta = json.loads(meta_df.metadata[0])
        models = meta["thread"]["models"]
        for modelid in models:
            model = models[modelid]
            model_config = model["model_configuration"]
            runs_table_name = fix_dbname("{}_runs".format(model_config))

            op_table_query = "SELECT output_table_name from threads_output_table WHERE threadid='{}'".format(thread_id)
            op_table_df = pd.DataFrame(pd.read_sql(op_table_query, con))
            output_table_name = op_table_df.output_table_name[0]

            #identify cycles runs:
            if 'cycles' in model_config:
                data_query = """SELECT runs.*, outputs.*, ti.x as lon, ti.y as lat FROM
                    {}	runs
                    LEFT JOIN threads_inputs ti ON ti.id = runs.cycles_weather and ti.threadid = runs.threadid and ti.spatial_type = 'Point'
                    LEFT JOIN {} outputs
                        ON runs.mint_runid = outputs.mint_runid AND runs.threadid = outputs.threadid
                        WHERE runs.threadid='{}'  """.format(runs_table_name, output_table_name, thread_id)
            else:
                data_query = """SELECT * from {} runs LEFT JOIN {} outputs
                    ON runs.mint_runid = outputs.mint_runid AND runs.threadid = outputs.threadid
                    WHERE runs.threadid='{}' """.format(runs_table_name, output_table_name, thread_id)
            df = pd.DataFrame(pd.read_sql(data_query, con))
            df = df.drop(["threadid", "mint_runid"], axis=1)
            return df

def store_data(dataframe):
    scols = dataframe.columns.values.tolist()
    sdata = dataframe.to_dict('records')
    return scols, sdata

#datatable filtering
operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

# Read in the data from an uploaded file
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

# Build dash data table from dataframe
def create_datatable(dataframe):
    dtable = dt.DataTable(
        # Table Data
                    id='dtable',
                    data=dataframe.to_dict('records'),
                    columns=[{'name': i, 'id': i, "selectable": True, "hideable": True} for i in dataframe.columns],
        # Table Controls
                    filter_action='custom',
                    filter_query='',
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="multi",
                    # row_selectable="multi",
                    # row_deletable=True,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 10,
                )
    return dtable

## Generate Map from user selections
def generate_map(spatial_data,lat,lon,hover,color):
    fig = px.scatter_mapbox(spatial_data, lat=lat, lon=lon, hover_name=hover, color=color, zoom=6,height=300)
    fig.update_layout(mapbox_style="stamen-terrain")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

## CALLBACKS ##
# Load thread or upload data into data table and store.  Use default dataframe if no data
@app.callback([Output('uploadInfo','children'),
                Output('upload-s-data','data'), Output('upload-s-cols','data'), Output('upload-s-num','data'),
                Output('upload-div-scatter','children'),Output('upload-div-parallel','children'),Output('upload-map','children'),
                Output('upload-datatable', 'children')],
              [Input('thread_id', 'value'),Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def update_output(threadid,contents, filename):
    df = pd.DataFrame([])
    if contents is None:
        if threadid is None or threadid == '':
            raise PreventUpdate
        else:
            df = load_thread_data(threadid)
            uploadinfo = html.Div(['Data Source: ',threadid])
    else:
        df = parse_contents(contents, filename)
        uploadinfo = html.Div(['Data Source: ',filename])

    #get columns of dataframe
    cols = df.columns.values.tolist()
    #get numeric columns
    ncols =  df.iloc[0:5].select_dtypes(include=np.number).columns.tolist()
    #store data from file
    sdata = df.to_dict('records')
    #Build tab figures
    scatterchildren = dcc.Graph(id='graph-scatter')
    parallelchildren = [html.P(id='msg-parallel'),dcc.Graph(id='graph-parallel')]
    mapchildren = dcc.Graph(id='map-graph')
    #Build Datatable
    outputcontent = html.Div([
        html.H4(['DATA'],className='two columns'),
        html.Div([' '],className='nine columns'),
        create_datatable(df),
        html.Div(id='datatable-filter-container')
    ])
    return uploadinfo,sdata, cols,ncols,scatterchildren,parallelchildren,mapchildren,outputcontent

#Backend Filter data table. **Add by selected points
@app.callback(
    Output('dtable', "data"),
    [Input('dtable', "filter_query"),Input('map-graph','selectedData')],
    [State('upload-s-data','data'),
     State('upload-lat-selector','value'),State('upload-lon-selector','value')
    ])
def update_table(filter,selectedpoints,sdata,latcol,loncol):
    filtering_expressions = filter.split(' && ')
    dff = pd.DataFrame(sdata)
    if selectedpoints is not None:
        points = selectedpoints['points']
        dfPoints = pd.DataFrame(points)
        dfPoints=dfPoints[['lat','lon']]
        dff = pd.merge(dff,dfPoints, left_on=[latcol,loncol],right_on=['lat','lon'])
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    return dff.to_dict('records')


### SCATTER / LINE ###
# Create dropdown Options for elements that take all columns: Scatter plot and Map selections
scatter_dropdowns = ['upload-x','upload-y','upload-color','upload-facet_col','upload-facet_row','upload-hover','upload-lat-selector','upload-lon-selector']
for dd in scatter_dropdowns:
    @app.callback(Output(dd,'options'),
                [Input('upload-s-cols','data')])
    def scatter_options(cols):
        if cols is None:
            raise PreventUpdate
        col_options = [dict(label=x, value=x) for x in cols]
        return col_options

## Make Scatter PLot##
@app.callback(Output('graph-scatter', 'figure'),
                [Input('btn-scatter','n_clicks')
                ,Input('upload-x','value')
                ,Input('upload-y','value'),Input('upload-color','value')
                ,Input('upload-facet_col','value'),Input('upload-facet_row','value')
                ,Input('upload-hover','value')]
                ,[State('dtable','data')]
                )
def make_scatter(n_clicks, x, y, color, facet_col, facet_row, hover_info,tabledata):
    if n_clicks is None:
        raise PreventUpdate
    if tabledata is None:
        raise PreventUpdate
    data_graph = pd.DataFrame(tabledata)
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

## Make Map PLot##
@app.callback(Output('map-graph', 'figure'),
                [Input('btn-map','n_clicks')
                ,Input('upload-lat-selector','value')
                ,Input('upload-lon-selector','value')]
                ,[State('dtable','data')]
                )
def make_map(n_clicks, lat,lon,tabledata):
    if n_clicks is None:
        raise PreventUpdate
    if tabledata is None:
        raise PreventUpdate
    data_graph = pd.DataFrame(tabledata)
    data_graph = data_graph[[lat,lon]].drop_duplicates()
    fig = generate_map(data_graph,lat,lon,None,None)
    return fig

### Save Selected Map points to data storedata
@app.callback(Output('upload-s-selectedpoints','data'),
                [Input('map-graph','selectedData')])
def store_selectedpoints(selectedpoints):
    if selectedpoints is None:
        return None
    else:
        points = selectedpoints['points']
        dfPoints = pd.DataFrame(points)
        dfPoints=dfPoints[['lat','lon']]
        return dfPoints.to_dict('records')

### PARALLEL COORDINATES ###
## Create Options selectors for Parallel Coordinates plot
@app.callback([Output('dd_pcoord_scale','options'),Output('cl_pcoord','options')],
            [Input('upload-s-cols','data'),Input('upload-s-num','data')])
def parallel_coordinates_options(cols,ncols):
    if cols is None:
        raise PreventUpdate
    if ncols is None:
        raise PreventUpdate
    col_options = [dict(label=x, value=x) for x in sorted(ncols)]
    return col_options,col_options

## Build Parallel Graphs
@app.callback([Output('graph-parallel', 'figure'),Output('msg-parallel', 'children')],
                [Input('btn-pcoord','n_clicks')],
                [State('dd_pcoord_scale','value'),State('cl_pcoord','value'),State('dtable','data')]
                )
def make_parallel(n_clicks,scale,cols,tabledata):
    if n_clicks is None:
        raise PreventUpdate
    if scale is None or cols is None:
        msg = 'Please select scale and axes options'
        fig = {}
        return fig, msg
    # scale = "'" + scale + "'"
    cols.append(scale)
    colset = set(cols)
    collist = list(colset)
    figdata = pd.DataFrame(tabledata)
    figdata = figdata[collist]
    fig = px.parallel_coordinates(figdata, color=scale,
                            color_continuous_midpoint = figdata.loc[:,scale].median(),
                             color_continuous_scale=px.colors.diverging.Tealrose
                             )
    msg=''
    return fig,msg

# Comment to force rebuild
