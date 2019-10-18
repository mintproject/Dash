from viz.utils import *

# styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://codepen.io/chriddyp/pen/brPBPO.css']

#pointless comment to force rebuild

## threadid.  Change to get this from url when avilable.
#thread_id = 'b2oR7iGkFEzVgimbNZFO'

# Options lists for cycles.  Move to callback when metadata available
options_list=['end_planting_day','fertilizer_rate','start_planting_day', 'weed_fraction', 'total_biomass', 'root_biomass',
   'grain_yield', 'forage_yield', 'ag_residue', 'harvest_index', 'potential_tr', 'actual_tr', 'soil_evap', 'total_n', 'root_n',
   'grain_n', 'forage_n', '"cum._n_stress"', 'n_in_harvest', 'n_in_residue', 'n_concn_forage','latitude','longitude'
]
selected_options=['fertilizer_rate','start_planting_day', 'weed_fraction','grain_yield','latitude','longitude']

# Layout
def generate_layout(thread_id):
    layout = html.Div([
        html.H3('Parallel Coordinates Graph'),
        html.Div([
            html.Label('Thread id'),
            dcc.Input(id='thread_id', value=thread_id, type='text', style={"width": "33%"}),
        ]),
        dcc.Store(id='s-settings'),
        dcc.Store(id='s-sqldata'),
        html.Div([
            html.Div([
                html.P('CROP'),
                dcc.Dropdown(id='dd_crop'),
                # dcc.Dropdown(id='dd_crop',multi=True),
                html.P('PLANTING START DATE'),
                dcc.Dropdown(id='dd_planting',multi=True),
            ],className="four columns"),
            html.Div([
                html.P('LOCATIONS'),
                dcc.Dropdown(id='dd_locations',multi=True),
                html.P('YEAR'),
                html.Div(id='rs_year'),
            ],className="eight columns"),
        ],className="row"),
        html.Div([
            html.Div([
                html.P('AXES:'),
                dcc.Dropdown(id='dd_pcoptions',
                            options=[dict(label=x, value=x) for x in sorted(options_list)],
                            value=selected_options,
                            multi=True),
            ],className="six columns"),
            html.Div([
                html.P('SCALE:'),
                dcc.Dropdown(id='dd_pcscale',
                            options=[dict(label=x, value=x) for x in sorted(options_list)],
                            value=selected_options[0]
                            ),
            ],className="three columns"),
            html.Div([
                html.Div([html.Button('Build Parallel Coordinates', id='btn-pc')],style={"margin-top":'30px'})
            ],className="two columns"),
        ],className="row"),
        html.Div([
                html.Div(id='div_pcoptions')
        ],className="row"),
        html.Div([
            dcc.Loading(id='l-graph',children=[
                html.Div(id='graph')
            ],type="circle"),
        ],className="row"),
        html.Div(id='testdiv'),
    ])
    return layout


# Callbacks
#Set Dropdown Values
@app.callback(
    [Output('dd_crop','options'),Output('dd_crop','value'),
    Output('dd_locations','options'),Output('dd_locations','value'),
    Output('dd_planting','options'), Output('dd_planting','value')
    ,Output('rs_year','children')
    ],
    [
        Input('s-settings','data'),
        Input(component_id='thread_id', component_property='value')
    ]
    )
def set_dropdowns(settings,thread_id):
    if thread_id is None or thread_id == '':
        raise PreventUpdate
    tablename = 'cycles_0_9_4_alpha_advanced_pongo_weather_runs'
    query = """SELECT crop_name, fertilizer_rate, start_planting_day, weed_fraction, latitude, longitude,start_year,end_year,location
                FROM
                (Select id, x as longitude, y as latitude, CONCAT(ROUND(y::numeric,2)::text ,'Nx',ROUND(x::numeric,2)::text ,'E') as location
                FROM threads_inputs where threadid = '{}') ti
                INNER JOIN
                (select * from {} where threadid = '{}') i
                ON ti.id = i.cycles_weather;""".format(thread_id,tablename,thread_id)
    df = pd.DataFrame(pd.read_sql(query,con))

    #dropdown options
    crops = df.crop_name.unique()
    crop_options = [dict(label=x, value=x) for x in sorted(crops)]
    planting_starts = df.start_planting_day.unique()
    planting_options =[dict(label=x, value=x) for x in sorted(planting_starts)]
    locations = df.location.unique()
    location_options = [dict(label=x, value=x) for x in sorted(locations)]
    #year range slider options
    start_year = df.start_year.min()
    end_year = df.end_year.max()
    year_options = [dict(label=x, value=x) for x in range(start_year, end_year)]
    testdiv = 'years: {} - {}'.format(start_year, end_year)
    print("ok:" + thread_id)

    yearslider =dcc.RangeSlider(
                id='rs_year',
                min=start_year,
                max=end_year,
                marks={i: '{}'.format(i) for i in range(start_year,end_year+1)},
                step=None,
                value=[(end_year-3),(end_year-1)],
                allowCross=False
            ),
    return [crop_options,crops[0],
            location_options,locations[0:5],
            planting_options,planting_starts,
            yearslider]

@app.callback(
    Output('testdiv','children'),
    # Output('sqldata','data')
    [Input('btn-pc', 'n_clicks')],
    [State('dd_crop','value'),State('dd_locations','value'), State('dd_planting','value'), State('rs_year','value'),
    State('dd_locations','options'),State('rs_year','min'),State('rs_year','max'),State('dd_pcoptions','value'),State('dd_pcscale','value')
     ,State(component_id='thread_id', component_property='value')])
def update_figure(n_clicks,crop,locations,planting,year,locationoptions,yearmin,yearmax,selectlist,scale,thread_id):
    if n_clicks is None:
        raise PreventUpdate
    for item in (crop,locations,planting,year):
        if item is None or item == '':
            # raise PreventUpdate
            return "Please ensure all variables are selected"
    ins = 'cycles_0_9_4_alpha_advanced_pongo_weather_runs'
    outs = 'cycles_0_9_4_alpha_advanced_pongo_weather_cycles_season outs'
    thread = "'" + thread_id + "'"
    #build lists for strings
    select_cols = 'crop'
    selectlist.append(scale)
    selectlist = list(sorted(set(selectlist)))
    if isinstance(selectlist, list):
        scols = "::numeric,".join(list(selectlist))
    if len(selectlist) > 0:
        select_cols = select_cols + ', ' + scols + '::numeric'

    # crop_list=[]
    # if isinstance(crop, list):
    #     crop_list = "','".join(list(crop))
    # crop_list = "'" + crop_list + "'"

    #build lists for ints
    planting_list = ",".join(str(x) for x in list(planting))
    #if locations selected < total locations, add locations clause
    # locationclause = ''
    # if len(locations) != len(locationoptions):
    locations_list=[]
    if isinstance(locations, list):
        locations_list = "','".join(list(locations))
    locations_list = "'" + locations_list + "'"
        # locationclause = ' AND location IN  ({}) '.format(locations_list)
    query="""SELECT {}
              FROM
            (
            SELECT * FROM 
            (Select id, x as longitude, y as latitude, CONCAT(ROUND(y::numeric,2)::text ,'Nx',ROUND(x::numeric,2)::text ,'E') as location
              FROM threads_inputs 
              where threadid =  '{}' ) ti
              INNER JOIN
              (select * from {} 
                where threadid = '{}' 
                AND crop_name LIKE '{}'
                AND start_planting_day IN ({})
                ) i
              ON ti.id = i.cycles_weather
              AND ti.location in ({})  
            ) ins
            INNER JOIN
            (Select * from
            (SELECT *, EXTRACT(year FROM TO_DATE(date, 'YYYY-MM-DD')) as year
            FROM {}) o
            WHERE year >= {} and year <= {}
            ) outs
            ON ins.mint_runid = outs.mint_runid """.format(select_cols,thread_id,ins,thread_id,crop,planting_list,locations_list,outs,year[0],year[1])
    pcdata = pd.DataFrame(pd.read_sql(query,con))
    # contents=[]
    # for c in crop:
    # graphid = 'graph-' + c
    # c = crop[0]
    figdata = pcdata
    fig = px.parallel_coordinates(figdata, color=scale,
                            # color_continuous_midpoint = figdata.loc[:,scale].median(),
                            #  color_continuous_scale=px.colors.diverging.Tealrose
                             )
    pc = dcc.Graph(id='graphid',figure=fig)
    # contents.append(pc)
    return pc

