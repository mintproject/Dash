from viz.utils import *

#styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
'https://codepen.io/chriddyp/pen/brPBPO.css']

# # Load Data
# series = pd.read_excel('./Data/PIHM/seriesmelt.xlsx')
# seriesdf = pd.DataFrame(series)
# locations = pd.read_excel('./Data/PIHM/locations.xlsx')
# locationsdf = pd.DataFrame(locations)
#
# # Data options
# datacols = seriesdf.columns.values.tolist()
#

thread_id=''
# Layout
def generate_layout(thread_id):
    dlayout = html.Div([
        # DATA STORES
        dcc.Store(id='ts-graph-file'),
        dcc.Store(id='ts-graph-data-cols'),
        dcc.Store(id='ts-graph-data'),
        dcc.Store(id='ts-spatial-file'),
        dcc.Store(id='ts-spatial-data-cols'),
        dcc.Store(id='ts-spatial-data'),
        dcc.Store(id='ts-lat-lon'),
        dcc.Store(id='ts-map-selected'),
        html.Div([
            html.Img(src=app.get_asset_url('mint_logo.svg'), style={'height':'50px','float':'left'}),
            html.A([html.P(['Solutions-to-Problems Interactive Narrative & Graphics Service']
                ,style={'float':'right','margin-top':'10px','color':'grey'})], href='https://mint-project.org/mint-overview/spring-dss-service/', target="_blank")
            ],
            id='ts-header',
            style={'background-color':'#e6f5ff','margin-bottom':'5px'},
            className='row'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3(['Spatial Data Visualization']),
                    html.P(['Please Upload data to generate the map'],id='ts-mapheader'),
                    html.Div([
                        dcc.Graph(id='ts-mapfig',style={'width':'300px'}),
                    ],id='ts-mapdiv',style={'display':'none'}),
                ]),
                html.Details([
                html.Summary('Line Graph Settings'),
                html.Div([
                    html.Div([
                        html.P(['X Axis: '],className='four columns'),
                        html.Div([dcc.Dropdown(id='ts-x')],className='eight columns'),
                    ],className='row'),
                    html.Div([
                        html.P(['Y Axis: '],className='four columns'),
                        html.Div([dcc.Dropdown(id='ts-y')],className='eight columns'),
                    ],className='row'),
                    html.Div([
                        html.P(['Color: '],className='four columns'),
                        html.Div([dcc.Dropdown(id='ts-color')],className='eight columns'),
                    ],className='row'),
                    html.Div([
                        html.P(['Facet Column: '],className='four columns'),
                        html.Div([dcc.Dropdown(id='ts-facet_col')],className='eight columns'),
                    ],className='row'),
                    html.Div([
                        html.P(['Facet Row: '],className='four columns'),
                        html.Div([dcc.Dropdown(id='ts-facet_row')],className='eight columns'),
                    ],className='row'),
                    html.Div([
                        html.P(['On Hover Show: '],className='four columns'),
                        html.Div([dcc.Dropdown(id='ts-hover',multi=True)],className='eight columns'),
                    ],className='row'),
                    html.Div([
                        html.Button('Draw Graphs', id='ts-btn-scatter'),
                    ],className='row'),
                ]),
                ]),
                html.Details([
                    html.Summary('Parallel Coordinates Settings'),
                    html.Div('Add elements here'),
                    ]),
            ],id='ts-settings',style={'float':'left','width':'30%'}),
            html.Div([
                dcc.Tabs(id="tabs", children=[
                    dcc.Tab(label='Upload Data',children=[
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H6('Upload Data'),
                                html.P(['Graphing Data: '],style={'float':'left','width':'150px','font-weight':'bold'}),
                                html.P([html.P(['No Data Loaded'],style={'font-style':'italic'})],id='txt-graphing',style={'float':'left','width':'150px'}),
                                html.Div([
                                    html.P(['Spatial Data: '],style={'float':'left','width':'150px','clear':'both','font-weight':'bold'}),
                                    html.P([html.P(['No Data Loaded'],style={'font-style':'italic'})],id='txt-spatial',style={'float':'left','width':'150px'}),
                                ]),
                            ],className='five columns'),
                            html.Div([
                                html.Div([
                                    dcc.RadioItems(
                                        id='ts-rb-filetype',
                                        options=[{'label': 'Upload Graphing Data', 'value': 'graph'},
                                                {'label': 'Upload Spatial Data', 'value': 'spatial'}],
                                        value='graph',
                                        labelStyle={'display': 'inline-block','margin-left':'10px'}
                                    ),
                                ]),
                                dcc.Upload(
                                id='ts-ts-data',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files'),
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '80px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '20px',
                                    'clear':'both'
                                },
                            ),
                            ],className='six columns'),
                            html.Div([
                                html.Div([],id='ts-output-ts-data'),
                            ],className='six columns')

                        ],className='row'),

                        html.H5(['Define Spatial Data'],className='twelve columns'),
                        html.Div([
                            html.Div([
                                html.P(['Latitude Col:']),
                                html.Div([dcc.Dropdown(id='ts-dd-spatialfile-lat')]),
                            ],className='four columns'),
                            html.Div([
                                html.P(['Longitude Column:']),
                                html.Div([dcc.Dropdown(id='ts-dd-spatialfile-lon')]),
                            ],className='four columns'),
                        ],className='row'),
                        html.H5(['Define columns to Link datasets'],className='twelve columns'),
                        html.Div([
                            html.Div([
                                html.P(['Graphing Data Link Columns:']),
                                html.Div([dcc.Dropdown(id='ts-dd-graphdata-merge',multi=True)]),
                            ],className='four columns'),
                            html.Div([
                                html.P(['Spatial Data Link Columns:']),
                                html.Div([dcc.Dropdown(id='ts-dd-spatialdata-merge',multi=True)]),
                            ],className='four columns'),
                        ],className='row'),
                    ],id='ts-upload',className='row',style={'padding':'15px'}),
                ]),
                    dcc.Tab(label='Line', children=[
                        html.Div([html.H6(['Please enter selections in the dropdowns at left.'],style={'margin':'50px'})],id='ts-graphs'),
                    ]),
                    dcc.Tab(label='Parallel', children=[
                        html.Div(id='ts-parallel'),
                    ]),
                ]),
            ],style={'float':'left','width':'70%'}),
        ],className='row'),
    html.Div(['This project is funded by the Defense Advanced Research Projects Agency under award W911NF-18-1-0027.'],
        id='ts-footer',
        className='row',
        style={'background-color':'#e6f5ff','text-align':'center','padding':'15px'}),
    html.Div(id='ts-testdiv')
    ])
    return dlayout

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

@app.callback([Output('txt-graphing','children')
               ,Output('ts-graph-data-file','data'),Output('ts-graph-data-cols','data')
               ,Output('ts-graph-data','data')],
              [Input('ts-ts-data', 'contents')],
              [State('ts-ts-data', 'filename'),State('ts-rb-filetype','value')])
def update_output(contents, names, filetype):
    if contents is None:
        raise PreventUpdate
    if filetype == 'graph':
        df = parse_contents(contents, names)
        cols = df.columns.values.tolist()
        storedata = df.to_json(date_format='iso', orient='split')
        return names, names, cols, storedata
    else:
        raise PreventUpdate

@app.callback([Output('txt-spatial','children')
               ,Output('ts-spatial-data-file','data'),Output('ts-spatial-data-cols','data')
               ,Output('ts-spatial-data','data')],
              [Input('ts-ts-data', 'contents')],
              [State('ts-ts-data', 'filename'),State('ts-rb-filetype','value')])
def update_output(contents, names, filetype):
    if contents is None:
        raise PreventUpdate
    if filetype == 'spatial':
        df = parse_contents(contents, names)
        cols = df.columns.values.tolist()
        storedata = df.to_json(date_format='iso', orient='split')
        return names, names, cols, storedata
    else:
        raise PreventUpdate

# Add options for lat lon dropdowns
@app.callback([Output('ts-dd-spatialfile-lat','options'),Output('ts-dd-spatialfile-lon','options'),Output('ts-lat-lon','data')],
                [Input('ts-graph-data-cols','data'),Input('ts-spatial-data-cols','data')])
def update_latloncols(graphcols,spatialcols):
    if graphcols is None and spatialcols is None:
        raise PreventUpdate
    if spatialcols is None:
        #if no spatial data get options from graphing data
        latlons = [dict(label=x, value=x) for x in graphcols]
        latlonfile = 'graph'
    else:
        # if spatial data, get options from there
        latlons = [dict(label=x, value=x) for x in spatialcols]
        latlonfile = 'spatial'
    return latlons,latlons,latlonfile

#add options for data merge column
# ts-dd-spatialata-merge
@app.callback([Output('ts-dd-graphdata-merge','options'),Output('ts-dd-spatialdata-merge','options')],
                [Input('ts-graph-data-cols','data'),Input('ts-spatial-data-cols','data')])
def update_mergecols(graphcols,spatialcols):
    if graphcols is None:
        raise PreventUpdate
    if spatialcols is None:
        raise PreventUpdate
    else:
        graph_options = [dict(label=x, value=x) for x in graphcols]
        spatial_options = [dict(label=x, value=x) for x in spatialcols]
        return graph_options, spatial_options
    return None

# Display map when data loaded and lat / lon selected
@app.callback([Output('ts-mapheader','style'),Output('ts-mapdiv','style'),Output('ts-mapfig','figure')],
                [Input('ts-dd-spatialfile-lat','value'),Input('ts-dd-spatialfile-lon','value')],
                [State('ts-lat-lon','data'),State('ts-spatial-data','data'),State('ts-graph-data','data')])
def show_map(lat,lon,latlontype,spatialdata,graphdata):
    if lat is None or lon is None:
        raise PreventUpdate
    if latlontype == 'spatial':
        spatialdf = pd.read_json(spatialdata, orient='split')
    elif latlontype == 'graph':
        spatialdf = pd.read_json(graphdata, orient='split')
    headerdisplay = {'display': 'none'}
    mapdisplay = {'display':'inline-block'}
    mapfig = generate_map(spatialdf,lat,lon,None,None)
    return headerdisplay, mapdisplay, mapfig

## Generate Map from user selections
def generate_map(spatial_data,lat,lon,hover,color):
    fig = px.scatter_mapbox(spatial_data, lat=lat, lon=lon, hover_name=hover, color=color, zoom=6,height=300)
    fig.update_layout(mapbox_style="stamen-terrain")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

# Create dropdown Options for Scatter plot selections
scatter_dropdowns = ['ts-x','ts-y','ts-color','ts-facet_col','ts-facet_row','ts-hover']
for dd in scatter_dropdowns:
    @app.callback(Output(dd,'options'),
                [Input('ts-graph-data-cols','data')])
    def scatter_options(cols):
        if cols is None:
            raise PreventUpdate
        col_options = [dict(label=x, value=x) for x in cols]
        return col_options

# Output time series
@app.callback(Output('ts-graphs', 'children'),
                [Input('ts-btn-scatter','n_clicks')
                ,Input('ts-x','value')
                ,Input('ts-y','value'),Input('ts-color','value')
                ,Input('ts-facet_col','value'),Input('ts-facet_row','value')
                ,Input('ts-hover','value')
                ,Input('ts-mapfig','selectedData')]
                ,[State('ts-graph-data','data'),State('ts-spatial-data','data')
                    ,State('ts-lat-lon','data'),State('ts-dd-spatialfile-lat','value'),State('ts-dd-spatialfile-lon','value')
                    ,State('ts-dd-graphdata-merge','value'),State('ts-dd-spatialdata-merge','value')]
                )
def make_scatter(n_clicks, x, y, color, facet_col, facet_row, hover_info,selectedpoints,graphdata,spatialdata,latlontype,latcol,loncol,graphmerge,spatialmerge):
    if n_clicks is None:
        raise PreventUpdate
    data_graph = pd.read_json(graphdata, orient='split')
    if selectedpoints is not None:
        points = selectedpoints['points']
        dfPoints = pd.DataFrame(points)
        dfPoints=dfPoints[['lat','lon']]
        if latlontype == 'spatial':
            spatialdf = pd.read_json(spatialdata, orient='split')
            selecteddf = pd.merge(spatialdf,dfPoints, left_on=[latcol,loncol],right_on=['lat','lon'])
            data_graph = pd.merge(data_graph,selecteddf,left_on=graphmerge, right_on=spatialmerge)
        elif latlontype == 'graph':
            graphdf = pd.read_json(graphdata, orient='split')
            data_graph = pd.merge(graphdf,dfPoints, left_on=[latcol,loncol],right_on=['lat','lon'])
    fig = px.line(
        data_graph,
        x=x,
        y=y,
        color=color,
        facet_col=facet_col,
        facet_row=facet_row,
        height=500,
        hover_data = hover_info,
    )
    graphs = dcc.Graph(id='ts-graphs-line',figure=fig)
    return graphs
