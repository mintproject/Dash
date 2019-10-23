##### RENDER.PY #####
## FOR LIVE
from viz.utils import *
##

#styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
'https://codepen.io/chriddyp/pen/brPBPO.css']

# Options lists for cycles.  Move to callback when metadata available
options_list=['end_planting_day','fertilizer_rate','start_planting_day', 'weed_fraction', 'total_biomass', 'root_biomass',
   'grain_yield', 'forage_yield', 'ag_residue', 'harvest_index', 'potential_tr', 'actual_tr', 'soil_evap', 'total_n', 'root_n',
   'grain_n', 'forage_n', '"cum._n_stress"', 'n_in_harvest', 'n_in_residue', 'n_concn_forage']
selected_options=['fertilizer_rate','start_planting_day', 'weed_fraction','grain_yield']

# Layout
def generate_layout(thread_id):
    layout = html.Div([
    # Local Data Stores
    dcc.Store(id='cyclespc-s-filtdata'),
    dcc.Store(id='cyclespc-map-ids'),
    dcc.Store(id='cyclespc-map-selected'),
    # dcc.Store(id='cyclespc-s-settings'),
    # dcc.Store(id='cyclespc-cyclespc-s-sqldata'),
    #Page elements
        html.Div([
            html.H3(['Parallel Coordinates Graph']),
            html.Label(['for MINT modeling thread: '],style={'float':'left'}),
            dcc.Input(id='thread_id', value=thread_id,style={'float':'left'}),
        ],className='row'),

        html.Div([
            html.Div([
                html.P('CROP'),
                dcc.Dropdown(id='dd_crop'),
            ],className='three columns'),
            html.Div([
                html.P('PLANTING START DATE'),
                dcc.Dropdown(id='dd_planting',multi=True),
            ],className='three columns'),
        # ],className='row'),
        # html.Div([
            html.Div([
                html.P('AXES:'),
                dcc.Dropdown(id='dd_pcoptions',
                            options=[dict(label=x, value=x) for x in sorted(options_list)],
                            value=selected_options,
                            multi=True),
            ],className='six columns'),
        ],className='row'),
        html.Div([
            html.Div([
                html.P('YEAR'),
                html.Div(id='div_rs_year',children=[dcc.RangeSlider(id='rs_year')]),
            ],className="six columns"),
            html.Div([
                html.P('SCALE:'),
                dcc.Dropdown(id='dd_pcscale',
                            options=[dict(label=x, value=x) for x in sorted(options_list)],
                            value=selected_options[0]
                            ),
            ],className="three columns"),
            html.Div([
                html.Button('Build Parallel Coordinates', id='btn-pc',style={'margin':'30px'})
            ],className="three columns"),
        ],className="row"),

        html.Div([
            html.Div([
                dcc.Loading(id='l-cycles-map',children=[
                    html.Div(id='cycles-map'),
                ],type="circle"),
            ],className="four columns"),
            html.Div([
                dcc.Loading(id='l-pc-graph',children=[
                    html.Div(id='cycles-pc')
                ],type="circle"),
            ],className="eight columns"),
        ],className="row"),
        html.Div([
            html.Div(id="cycles-datatable")
        ],className='row')
    ])
    return layout

# FUNCTIONS
def load_spatial_data(thread_id):
    if thread_id is not None:
        if ' ' in thread_id:
            return None
        if thread_id.isalnum():
            spatial_query = """SELECT DISTINCT threadid, x as lon, y as lat,
                            id from threads_inputs where threadid='{}' and spatial_type = 'Point';""".format(thread_id)
            spatial_df = pd.DataFrame(pd.read_sql(spatial_query, con))
            if spatial_df.empty:
                return None
            return spatial_df
        return None
    return None

# Callbacks
# Build Map
@app.callback([Output('cycles-map', 'children'),Output('cyclespc-map-ids','data')],
              [Input('thread_id', 'value')],
              [State('cyclespc-map-ids','data')])
def update_output(thread_id,mapdata):
    if thread_id == '':
        kids =  ['Please enter a thread ID']
    if ' ' in thread_id or thread_id.isalnum()==False:
        kids = ['Please enter a properly formatted threadid.']
    df=pd.DataFrame()
    if thread_id.isalnum():
        df = load_spatial_data(thread_id)
        if df is None:
            return ['This thread has no Spatial data']
        fig = px.scatter_mapbox(df, lat="lat", lon="lon",
                                color_discrete_sequence=["fuchsia"], zoom=6, height=300)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        kids = [html.P('Please select points from the map below using the plotly selection tools (box or lasso) located in the top right of the map.'),
            dcc.Graph(id='locations_map', figure=fig)]
    locationsdata = df.to_dict('records')
    return kids, locationsdata

# Show result of selecting data with either box select or lasso
@app.callback(Output('cyclespc-map-selected','data'),
    [Input('locations_map','selectedData')],
    [State('cyclespc-map-selected','data')]
    )
def selectData(selectData,sData):
    kids = ''
    if selectData is None:
        return {}
    dfPoints = pd.DataFrame(selectData['points'])
    selectedData = dfPoints.to_dict('records')
    return  selectedData

#Set Dropdown Values
@app.callback(
    [Output('dd_crop','options'),Output('dd_crop','value'),
    Output('dd_planting','options'), Output('dd_planting','value')
    ,Output('div_rs_year','children')],
    [
        # Input('cyclespc-s-settings','data'),
        Input(component_id='thread_id', component_property='value')
    ]
    )
def set_dropdowns(thread_id):
    if thread_id is None or thread_id == '':
        raise PreventUpdate
    tablename = 'cycles_0_9_4_alpha_runs'
    query = """SELECT crop_name, fertilizer_rate, start_planting_day, weed_fraction, start_year,end_year
                FROM {} where threadid = '{}';""".format(tablename,thread_id)
    df = pd.DataFrame(pd.read_sql(query,con))
    #dropdown options
    crops = df.crop_name.unique()
    crop_options = [dict(label=x, value=x) for x in sorted(crops)]
    planting_starts = df.start_planting_day.unique()
    planting_options =[dict(label=x, value=x) for x in sorted(planting_starts)]
    #year range slider options
    start_year = df.start_year.min()
    end_year = df.end_year.max()
    year_options = [dict(label=x, value=x) for x in range(start_year, end_year)]
    testdiv = 'years: {} - {}'.format(start_year, end_year)
    yearslider =dcc.RangeSlider(
                id='rs_year',
                min=start_year,
                max=end_year,
                marks={i: '{}'.format(i) for i in range(start_year,end_year+1)},
                step=None,
                value=[end_year,(end_year+1)],
                allowCross=False
            ),
    return [crop_options,crops[0],
            planting_options,planting_starts,
            yearslider]

@app.callback(
    Output('cycles-pc','children'),
    [Input('btn-pc', 'n_clicks'),Input('cyclespc-map-selected','data')]
     ,[State('dd_crop','value'),State('dd_planting','value'), State('rs_year','value')
    ,State('rs_year','min'),State('rs_year','max')
    ,State('dd_pcoptions','value'),State('dd_pcscale','value'),State('thread_id', 'value')
    ,State('cyclespc-map-ids','data')
    ]
    )
def update_figure(n_clicks,selectedPoints,crop,planting,year,yearmin,yearmax,selectlist,scale,thread_id,mapData):
    if n_clicks is None:
        raise PreventUpdate
    # Get Data filtered by top selections
    for item in (crop,planting,year):
        if item is None or item == '':
            # raise PreventUpdate
            return "Please ensure all variables are selected"
    ins = 'cycles_0_9_4_alpha_runs'
    outs = 'cycles_0_9_4_alpha_cycles_season'
    thread = "'" + thread_id + "'"
    # build select lists, correcting for database characterization of columns as text
    select_cols = 'crop'
    selectlist.append(scale)
    selectlist = list(sorted(set(selectlist)))
    if isinstance(selectlist, list):
        scols = "::numeric,".join(list(selectlist))
    if len(selectlist) > 0:
        select_cols = select_cols + ', ' + scols + '::numeric'
    # build lists for ints
    planting_list = ",".join(str(x) for x in list(planting))
    locations_filter=''
    if selectedPoints is not None:
        md = pd.DataFrame(mapData)
        dfPoints = pd.DataFrame(selectedPoints)
        dfMap = pd.merge(md,dfPoints, left_on=['lat','lon'], right_on=['lat','lon'])
        cycles_weather_list = "','".join(dfMap.id.unique())
        cycles_weather_list = "'" + cycles_weather_list + "'"
        locations_filter = 'AND cycles_weather IN ({})'.format(cycles_weather_list)

    query="""SELECT {}
              FROM
            (
              select * from {}
                where threadid = '{}'
                AND crop_name LIKE '{}'
                AND start_planting_day IN ({})
                {}
            ) ins
            INNER JOIN
            (Select * from
            (SELECT *, EXTRACT(year FROM TO_DATE(date, 'YYYY-MM-DD')) as year
            FROM {}) o
            WHERE year >= {} and year <= {}
            ) outs
            ON ins.mint_runid = outs.mint_runid""".format(select_cols,ins,thread_id,crop,planting_list,locations_filter,outs,year[0],year[1])
    # get data filtered to settings
    figdata = pd.DataFrame(pd.read_sql(query,con))
    fig = px.parallel_coordinates(figdata, color=scale,
                            # color_continuous_midpoint = figdata.loc[:,scale].median(),
                            #  color_continuous_scale=px.colors.diverging.Tealrose
                             )
    pc = dcc.Graph(id='graphid',figure=fig)
    return pc

##### END RENDER.PY #####
