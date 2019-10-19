from viz.utils import *

# styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://codepen.io/chriddyp/pen/brPBPO.css']

## threadid.  Change to get this from url when avilable.
# hard code if needed thread_id = 'b2oR7iGkFEzVgimbNZFO'

thread_id = ""

# Layout
def generate_layout(cycles_thread_id):
    global thread_id
    thread_id = cycles_thread_id
    return html.Div([
        dcc.Store(id='s-settings'),
        html.Div([
            html.Label('Thread id'),
            dcc.Input(id='cycles_thread_id', value=thread_id, type='text', style={"width": "33%"}),
        ]),
        html.Div([
            html.Div([
                html.P('CROP'),
                dcc.Dropdown(id='dd_crop_cylces'),
                html.P('PLANTING START DATE'),
                dcc.Dropdown(id='dd_planting_cylces'),
            ], className="four columns"),
            html.Div([
                html.P('LOCATIONS'),
                dcc.Dropdown(id='dd_locations_cylces', multi=True),
            ], className="eight columns"),
        ], className="row"),
        html.Div([
            html.Div([
                html.P('YEAR'),
            ], className="one columns"),
            html.Div([
                html.Div(id='rs_year_cylces'),
            ], className="eleven columns"),
        ], className="row"),
        html.Div([
            dcc.Loading(id='l-graph', children=[
                html.Div(id='graph')
            ], type="circle"),
        ], className="row"),
        html.Div(id='testvid_cylces'),
    ])


# Callbacks
@app.callback(
    [Output('dd_crop_cylces', 'options'), Output('dd_crop_cylces', 'value'),
     Output('dd_locations_cylces', 'options'), Output('dd_locations_cylces', 'value'),
     Output('dd_planting_cylces', 'options'), Output('dd_planting_cylces', 'value')
        , Output('rs_year_cylces', 'children')
     ],
    [
        Input('s-settings', 'data'),
        Input(component_id='cycles_thread_id', component_property='value')
    ]
)
def set_dropdowns(settings, cycles_thread_id):
    thread_id = cycles_thread_id
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
    df = pd.DataFrame(pd.read_sql(query, con))
    crops = df.crop_name.unique()
    crop_options = [dict(label=x, value=x) for x in sorted(crops)]
    planting_starts = df.start_planting_day.unique()
    planting_options = [dict(label=x, value=x) for x in planting_starts]
    locations = df.location.unique()
    location_options = [dict(label=x, value=x) for x in sorted(locations)]
    start_year = df.start_year.min()
    end_year = df.end_year.max()
    year_options = [dict(label=x, value=x) for x in range(start_year, end_year)]
    testvid_cylces = 'years: {} - {}'.format(start_year, end_year)
    yearslider = dcc.Slider(
        id='rs_year_cylces',
        min=start_year,
        max=end_year,
        marks={i: '{}'.format(i) for i in range(start_year, end_year)},
        step=None,
        value=start_year
    ),

    return [crop_options, crops[0],
            location_options, locations[0:3],
            planting_options, planting_starts[0],
            yearslider]


@app.callback(
    Output('testvid_cylces', 'children'),
    #  Output('graph', 'children'),
    [Input('dd_crop_cylces', 'value'), Input('dd_locations_cylces', 'value'), Input('dd_planting_cylces', 'value'),
     Input('rs_year_cylces', 'value')],
[State('cycles_thread_id','value')]
)
def update_figure(crop, locations, planting, year,thread_id):
    for item in (crop, locations, planting, year):
        if item is None or item == '':
            # raise PreventUpdate
            return "Please ensure all variables are selected"
    ins = 'cycles_0_9_4_alpha_advanced_pongo_weather_runs'
    outs = 'cycles_0_9_4_alpha_advanced_pongo_weather_cycles_season'
    if isinstance(locations, list):
        location_list = "','".join(list(locations))
        location_list = "'" + location_list + "'"
    else:
        location_list = "'" + locations + "'"
    query="""SELECT * FROM (SELECT ins.*, outs.grain_yield, EXTRACT(year FROM TO_DATE(outs.date, 'YYYY-MM-DD')) AS year from
            (
            SELECT * FROM
                ((Select id, x as longitude, y as latitude, CONCAT(ROUND(y::numeric,2)::text ,'Nx',ROUND(x::numeric,2)::text ,'E') as location
                FROM threads_inputs where threadid = '{}') ti
                INNER JOIN
                (select * from {} where threadid = '{}') i
                ON ti.id = i.cycles_weather)
            WHERE crop_name LIKE '{}' AND start_planting_day = {}
            AND location IN ({})
            ) ins
            INNER JOIN {} outs
            ON ins.mint_runid = outs.mint_runid) inout
            WHERE inout.year = {} """.format(thread_id,ins,thread_id,crop,planting,location_list,outs,year)
    figdata = pd.DataFrame(pd.read_sql(query, con))
    fig_list = []
    filtered_df = figdata.sort_values(by=['fertilizer_rate', 'weed_fraction'])
    n = 0
    for l in locations:
        n = n + 1
        ldata = filtered_df[filtered_df.location == l]
        graphid = 'graph-' + str(n)
        fig = px.line(
            ldata,
            x='fertilizer_rate',
            y='grain_yield',
            color='weed_fraction',
            # colorscale="Viridis",
            height=400,
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
        )], style={'float': 'left', 'width': '50%'})
        fig_list.append(lgraph)
    return fig_list
