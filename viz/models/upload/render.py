# import base64
# import io

# FOR LIVE
from viz.utils import *

#styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
'https://codepen.io/chriddyp/pen/brPBPO.css']

# Layout
def generate_layout(thread_id):
    dlayout = html.Div([
        # Data Stores
        dcc.Store(id='upload-s-cols'),
        dcc.Store(id='upload-s-num'),
        dcc.Store(id='s-data'),
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
            html.Div(id='map-div',style={'float':'left'}),
            dcc.Tabs(id="tabs", children=[
                dcc.Tab(label='Data', children=[
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
                dcc.Tab(label='Scatter / Line', children=[
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
                dcc.Tab(label='Parallel', children=[
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


            ])
        ],className='row'),

        html.Div([

            html.Div(id='output-data-upload'),
        ],className='row',style={'border-top':'2px solid black','margin-top':'20px','padding-top':'20px'}),
    ])
    return dlayout

## FUNCTIONS ##
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
                    filter_action="native",
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
                    export_format='csv',
                    export_headers='display',
                )
    return dtable

## CALLBACKS ##
# Load Uploaded data into data table and store.  Use default dataframe if no data
@app.callback([Output('uploadInfo','children'),Output('output-data-upload', 'children'),
                Output('upload-s-cols','data'), Output('upload-s-num','data'),
                Output('upload-div-scatter','children'),Output('upload-div-parallel','children')
                ],
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def update_output(contents, filename):
    if contents is None:
        raise PreventUpdate
    else:
        df = parse_contents(contents, filename)
    uploadinfo = html.Div(['Data Source: ',filename])
    outputcontent = html.Div([
        html.H4(['DATA'],className='two columns'),
        html.Div([' '],className='nine columns'),
        create_datatable(df)
        ])
    #get columns of dataframe
    cols = df.columns.values.tolist()
    #get numeric columns
    ncols =  df.iloc[0:5].select_dtypes(include=np.number).columns.tolist()
    #store data from file
    sdata = df.to_dict('records')
    scatterchildren = dcc.Graph(id='graph-scatter')
    parallelchildren = [html.P(id='msg-parallel'),dcc.Graph(id='graph-parallel')]
    return uploadinfo,outputcontent,cols,ncols,scatterchildren,parallelchildren

### SCATTER / LINE ###
# Create dropdown Options for Scatter plot selections
scatter_dropdowns = ['upload-x','upload-y','upload-color','upload-facet_col','upload-facet_row','upload-hover']
for dd in scatter_dropdowns:
    @app.callback(Output(dd,'options'),
                [Input('upload-s-cols','data')])
    def scatter_options(cols):
        if cols is None:
            raise PreventUpdate
        col_options = [dict(label=x, value=x) for x in cols]
        return col_options

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
