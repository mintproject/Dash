from viz.utils import *

#styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
'https://codepen.io/chriddyp/pen/brPBPO.css']

thread_id=''
# Layout
def generate_layout(thread_id):
    dlayout = html.Div([
        # DATA STORES
        dcc.Store(id='ts-graph-file'),
        dcc.Store(id='ts-graph-data-cols'),
        dcc.Store(id='ts-graph-data-ncols'),
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
            html.Button('Hide Map', id='btn-map-hide', n_clicks_timestamp=0),
            html.Button('Show Map', id='btn-map-show', n_clicks_timestamp=0,style={'display':'none'}),
        ],style={'float':'right','margin-right':'15px'}),
        html.H3(['Spatial Data Visualization'],className='row'),
        html.Div([
                html.Div([
                    html.P(['Please Upload data to generate the map'],id='ts-mapheader'),
                    html.Div([
                        dcc.Graph(id='ts-mapfig',style={'width':'450px'}),
                    ],id='ts-mapdiv',style={'display':'none'}),
                ],id='ts-settings',className='four columns'),
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
                                    html.Div([
                                        html.P(['Latitude Col:']),
                                        html.Div([dcc.Dropdown(id='ts-dd-spatialfile-lat')]),
                                        html.P(['Longitude Col:']),
                                        html.Div([dcc.Dropdown(id='ts-dd-spatialfile-lon')]),
                                    ]),
                                ],className='four columns'),
                                html.Div([
                                    html.Div([
                                        html.P(['Marker Color:']),
                                        html.Div([dcc.Dropdown(id='ts-dd-spatialfile-mark-color')]),
                                        html.P(['Marker Size:']),
                                        html.Div([dcc.Dropdown(id='ts-dd-spatialfile-mark-size')]),
                                    ]),
                                ],className='four columns'),
                                # html.Div([
                                #     html.Div([
                                #         html.P(['On Hover:']),
                                #         html.Div([dcc.Dropdown(id='ts-dd-spatialfile-hover',multi=True)]),
                                #     ]),
                                # ],className='four columns'),
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
                        dcc.Tab(label='Scatter Graph', children=[
                            html.P('Line Graph Settings'),
                            html.Div([
                                html.Div([
                                    html.P(['X Axis: ']),
                                    html.Div([dcc.Dropdown(id='ts-x')]),
                                    html.P(['Y Axis: ']),
                                    html.Div([dcc.Dropdown(id='ts-y')]),
                                ],className='three columns'),
                                html.Div([
                                    html.P(['Color: ']),
                                    html.Div([dcc.Dropdown(id='ts-color')]),
                                    html.P(['Color as category: ']),
                                    html.Div([
                                        dcc.Dropdown(id='ts-color-category',
                                                options=[
                                                    {'label': 'Default', 'value': 'default'},
                                                    {'label': 'Force Category', 'value': 'force'}
                                                ],
                                                value='default'),
                                                ]),
                                ],className='three columns'),
                                html.Div([
                                    html.P(['Facet Row: ']),
                                    html.Div([dcc.Dropdown(id='ts-facet_row')]),
                                    html.P(['Facet Column: ']),
                                    html.Div([dcc.Dropdown(id='ts-facet_col')]),
                                ],className='three columns'),
                                html.Div([
                                    html.P(['On Hover Show: ']),
                                    html.Div([dcc.Dropdown(id='ts-hover',multi=True)]),
                                    html.Button('Draw Graphs', id='ts-btn-scatter',style={'margin-top':'5px'}),
                                ],className='three columns'),
                            ],className='row'),
                            html.Div([html.H6(['Please enter selections in the Settings dropdowns to generate graphs.'],style={'margin':'50px'})],id='ts-graphs'),
                        ]),
                        dcc.Tab(label='Parallel Coordinates', children=[
                            html.P('Parallel Coordinates Settings'),
                            html.Div([
                                html.P(['Scale:'],className='two columns'),
                                dcc.Dropdown(id='ts-dd-pc-scale',className='four columns'),
                                html.Button('Build Graph',id='ts-btn-pc',className='three columns',style={'float':'right','margin-right':'30px'}),
                            ],className='row'),
                            html.Div([
                                html.P(['Columns to show:'],className='two columns'),
                                dcc.Checklist(id='ts-cl-pc-axes',className='ten columns',options=[{'label': 'Please upload data', 'value': ''}],
                                    labelStyle={'display': 'inline-block','margin-left':'5px'}),
                            ],className='row'),
                            html.P(id='msg-parallel'),
                            html.Div(id='ts-parallel')
                        ]),
                        dcc.Tab(label='Spatial Data table',children=[html.Div(id='map-dt-spatial')]),
                        dcc.Tab(label='Graphing Data table',children=[html.Div(id='map-dt-graphing')]),
                    ]),
                ],id='ts-tabs',className='eight columns'),
        ],className='row'),
    html.Div(['This project is funded by the Defense Advanced Research Projects Agency under award W911NF-18-1-0027.'],
        id='ts-footer',
        className='row',
        style={'background-color':'#e6f5ff','text-align':'center','padding':'15px','clear':'both'}),
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

## CALLBACKS ##
# Show / hide map and adjust Layout
@app.callback([Output('btn-map-show','style'),Output('btn-map-hide','style'),
                Output('ts-settings','style'),Output('ts-settings','className'),
                Output('ts-tabs','className')],
        [Input('btn-map-show','n_clicks_timestamp'),Input('btn-map-hide','n_clicks_timestamp')]
        )
def show_hide_map(showclicks,hideclicks):
    if int(showclicks)== int(hideclicks) is None:
        raise PreventUpdate
    hidestyle = {'display':'none'}
    showstyle = {'display':'block'}
    if int(showclicks) > int(hideclicks):
        return hidestyle,showstyle,showstyle,'four columns','eight columns'
    else:
        return showstyle,hidestyle,hidestyle,'zero columns','twelve columns'


# Load data
@app.callback([Output('txt-graphing','children')
               ,Output('ts-graph-data-file','data'),Output('ts-graph-data-cols','data'),Output('ts-graph-data-ncols','data')
               ,Output('ts-graph-data','data')],
              [Input('ts-ts-data', 'contents')],
              [State('ts-ts-data', 'filename'),State('ts-rb-filetype','value')])
def update_output(contents, names, filetype):
    if contents is None:
        raise PreventUpdate
    if filetype == 'graph':
        df = parse_contents(contents, names)
        #get columns of dataframe
        cols = df.columns.values.tolist()
        #get numeric columns
        ncols =  df.iloc[0:5].select_dtypes(include=np.number).columns.tolist()
        storedata = df.to_json(date_format='iso', orient='split')
        return names, names, cols, ncols, storedata
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

#BUild Datatables
@app.callback(Output('map-dt-spatial','children'),[Input('ts-spatial-data','data')])
def build_spatial_datatable(spatialdata):
    if spatialdata is None:
        raise PreventUpdate
    df = pd.read_json(spatialdata, orient='split')
    dtable = dt.DataTable(
# Table Data
            id='spatial_dtable',
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i, "selectable": True, "hideable": True} for i in df.columns],
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
            export_format='csv',
            export_headers='display',
        )
    return dtable

@app.callback(Output('map-dt-graphing','children'),[Input('ts-graph-data','data')])
def build_graphing_datatable(graphingdata):
    if graphingdata is None:
        return 'No data loaded'
        # raise PreventUpdate
    df = pd.read_json(graphingdata, orient='split')
    dtable = dt.DataTable(
# Table Data
            id='graphing_dtable',
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i, "selectable": True, "hideable": True} for i in df.columns],
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
            export_format='csv',
            export_headers='display',
        )
    return dtable

# Add options for lat lon dropdowns
@app.callback([Output('ts-dd-spatialfile-lat','options'),Output('ts-dd-spatialfile-lon','options'),Output('ts-lat-lon','data'),
                Output('ts-dd-spatialfile-mark-color','options'),Output('ts-dd-spatialfile-mark-size','options'),Output('ts-dd-spatialfile-hover','options')],
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
    return latlons,latlons,latlonfile,latlons,latlons,latlons

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
                [Input('ts-dd-spatialfile-lat','value'),Input('ts-dd-spatialfile-lon','value'),
                Input('ts-dd-spatialfile-mark-color','value'),Input('ts-dd-spatialfile-mark-size','value')
                # ,Input('ts-dd-spatialfile-hover','value')
                ],
                [State('ts-lat-lon','data'),State('ts-spatial-data','data'),State('ts-graph-data','data')])
def show_map(lat,lon,color,size,latlontype,spatialdata,graphdata):
    if lat is None or lon is None:
        raise PreventUpdate
    if latlontype == 'spatial':
        spatialdf = pd.read_json(spatialdata, orient='split')
    elif latlontype == 'graph':
        spatialdf = pd.read_json(graphdata, orient='split')
    headerdisplay = {'display': 'none'}
    mapdisplay = {'display':'inline-block'}
    mapfig = generate_map(spatialdf,lat,lon,color,size,None)
    return headerdisplay, mapdisplay, mapfig

## Generate Map from user selections
def generate_map(spatial_data,lat,lon,color,size,hover):
    fig = px.scatter_mapbox(spatial_data, lat=lat, lon=lon, hover_name=hover, color=color, size=size,zoom=6)
    fig.update_layout(mapbox_style="stamen-terrain")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

# Filter data on map selection ts-map-selected
@app.callback(Output('ts-map-selected','data'),
            [Input('ts-mapfig','selectedData')],
            [State('ts-graph-data','data'),State('ts-spatial-data','data')
                ,State('ts-lat-lon','data'),State('ts-dd-spatialfile-lat','value'),State('ts-dd-spatialfile-lon','value')
                ,State('ts-dd-graphdata-merge','value'),State('ts-dd-spatialdata-merge','value')])
def merge_data(selectedpoints,graphdata,spatialdata,latlontype,latcol,loncol,graphmerge,spatialmerge):
        if graphdata is None:
            raise PreventUpdate
        if selectedpoints is None:
            return None
        if selectedpoints is not None:
            data_graph = pd.read_json(graphdata, orient='split')
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
        return data_graph.to_json(date_format='iso', orient='split')


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
                ,Input('ts-y','value'),Input('ts-color','value'),Input('ts-color-category','value')
                ,Input('ts-facet_col','value'),Input('ts-facet_row','value')
                ,Input('ts-hover','value'),Input('ts-mapfig','selectedData')]
                ,[State('ts-graph-data','data'),State('ts-map-selected','data')]
                )
def make_scatter(n_clicks, x, y, color, colorcat, facet_col, facet_row, hover_info,selectedpoints,graphdata,selecteddata):
    if n_clicks is None:
        raise PreventUpdate
    if selecteddata is not None:
        data_graph = pd.read_json(selecteddata, orient='split')
    else:
        data_graph = pd.read_json(graphdata, orient='split')
    if colorcat == 'force':
        data_graph[color]=data_graph[color].astype(str)
    fig = px.scatter(
        data_graph,
        x=x,
        y=y,
        color=color,
        facet_col=facet_col,
        facet_row=facet_row,
        height=500,
        hover_data = hover_info,
    )
    fig.update_traces(marker=dict(size=4))
    graphs = dcc.Graph(id='ts-graphs-line',figure=fig)
    return graphs

### PARALLEL COORDINATES ###
## Create Options selectors for Parallel Coordinates plot
@app.callback([Output('ts-dd-pc-scale','options'),Output('ts-cl-pc-axes','options')],
            [Input('ts-graph-data-cols','data'),Input('ts-graph-data-ncols','data')])
def parallel_coordinates_options(cols,ncols):
    if cols is None:
        raise PreventUpdate
    if ncols is None:
        raise PreventUpdate
    col_options = [dict(label=x, value=x) for x in sorted(ncols)]
    return col_options,col_options

## Build Parallel Graphs
# dcc.Graph(id='ts-graph-parallel')
@app.callback([Output('ts-parallel', 'children'),Output('ts-msg-parallel', 'children')],
                [Input('ts-btn-pc','n_clicks')],
                [State('ts-dd-pc-scale','value'),State('ts-cl-pc-axes','value'),
                State('ts-graph-data','data'),State('ts-map-selected','data')]
                )
def make_parallel(n_clicks,scale,cols,graphdata,selecteddata):
    if n_clicks is None:
        raise PreventUpdate
    if scale is None or cols is None:
        msg = 'Please select scale and axes options'
        children =[]
        return children, msg
    cols.append(scale)
    colset = set(cols)
    collist = list(colset)
    if selecteddata is not None:
        data_graph = pd.read_json(selecteddata, orient='split')
    else:
        data_graph = pd.read_json(graphdata, orient='split')
    figdata = data_graph[collist]
    fig = px.parallel_coordinates(figdata, color=scale,
                            color_continuous_midpoint = figdata.loc[:,scale].median(),
                             color_continuous_scale=px.colors.diverging.Tealrose
                             )
    msg=''
    children = [dcc.Graph(id='ts-pc-graph',figure = fig)]
    return children,msg
