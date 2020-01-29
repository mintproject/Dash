import math
import re
from viz.utils import * 
# styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://codepen.io/chriddyp/pen/brPBPO.css']

## threadid.  Change to get this from url when avilable.
# hard code if needed thread_id = 'b2oR7iGkFEzVgimbNZFO'

thread_id = ""

# Layout
def generate_layout(thread_id):
    return html.Div([
        dcc.Store(id='s-settings'),
        dcc.Store(id='cycles-thread-info'),
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


def fix_dbname(name):
    return name.strip().lower().replace(' ', '_').replace('(',
        '').replace(')', '').replace('%', 'percentage').replace('/', 
        '_per_').replace('.', '_').replace('-', '_')

def load_thread_info(thread_id):
    if thread_id != None and thread_id != None:
        meta_query = "SELECT metadata FROM threads WHERE threadid='{}'".format(thread_id)
        meta_df = pd.DataFrame(pd.read_sql(meta_query, con))
        if meta_df.empty:
            print("Thread doesn't exist")
            return None
        meta = meta_df.metadata[0]
        models = meta["thread"]["models"]
        for modelid in models:
            model = models[modelid]
            model_config = model["model_configuration"]
            runs_table_name = fix_dbname("{}_runs".format(model_config))
            mname = re.sub(".+/", "", model_config)

            if mname.find("cycles") == 0: 
                # If this is a cycles model, fetch 
                # - the input column names, 
                # - the output table names, 
                # - the run table name

                ip_columns_query = "SELECT input_column_name FROM threads_input_column WHERE threadid='{}'".format(thread_id)
                ip_columns_df = pd.DataFrame(pd.read_sql(ip_columns_query, con))
                ip_columns = list(ip_columns_df.input_column_name)

                op_table_query = "SELECT output_table_name FROM threads_output_table WHERE threadid='{}'".format(thread_id)
                op_table_df = pd.DataFrame(pd.read_sql(op_table_query, con))
                output_table_names = list(op_table_df.output_table_name)

                return {
                    "runs_table": runs_table_name, 
                    "input_columns": ip_columns, 
                    "output_tables": output_table_names
                }
                

# Callbacks

# Fetch thread information into data stores
@app.callback(Output('cycles-thread-info','data'),
             [Input('cycles_thread_id', 'value')])
def update_thread_information(thread_id):
    return load_thread_info(thread_id)


def get_match_from_list(dlist, dstring):
    for ditem in dlist:
        if ditem.find(dstring) >= 0:
            return ditem

@app.callback(
    [Output('dd_crop_cylces', 'options'), Output('dd_crop_cylces', 'value'),
     Output('dd_locations_cylces', 'options'), Output('dd_locations_cylces', 'value'),
     Output('dd_planting_cylces', 'options'), Output('dd_planting_cylces', 'value'), 
     Output('rs_year_cylces', 'children')],
    [Input('cycles_thread_id','value'),
     Input('cycles-thread-info','data')]
)
def set_dropdowns(thread_id, thread_info):
    print(thread_info)

    if thread_id is None or thread_id == '' or thread_info is None:
        raise PreventUpdate

    tablename = thread_info["runs_table"]
    matchcol = "url"
    if tablename == "cycles_0_9_4_alpha_runs":
        matchcol = "id"
    weathercol = get_match_from_list(thread_info["input_columns"], "cycles_weather")
    outputtable = get_match_from_list(thread_info["output_tables"], "cycles_season")

    query = """SELECT crop_name, fertilizer_rate, start_planting_day, weed_fraction, latitude, longitude,start_year,end_year,location
                FROM
                (Select {}, x as longitude, y as latitude, CONCAT(ROUND(y::numeric,2)::text ,'Nx',ROUND(x::numeric,2)::text ,'E') as location
                FROM threads_inputs where threadid = '{}') ti
                INNER JOIN
                (select * from {} where threadid = '{}') i
                ON ti.{} = i.{};""".format(matchcol, thread_id,tablename,thread_id,matchcol, weathercol)
                
    df = pd.DataFrame(pd.read_sql(query, con))
    if df.empty:      
        empty_data_options = [{'label':'Waiting on Data Ingestion','value':'waiting'}]
        emptymsg = 'Please Wait for Data Ingestion'
        return [empty_data_options, empty_data_options[0],
            empty_data_options, empty_data_options[0],
            empty_data_options, empty_data_options[0],
            emptymsg]     
    crops = df.crop_name.unique()
    crop_options = [dict(label=x, value=x) for x in sorted(crops)]
    planting_starts = df.start_planting_day.unique()
    planting_options = [dict(label=x, value=x) for x in planting_starts]
    locations = df.location.unique()
    location_options = [dict(label=x, value=x) for x in sorted(locations)]
    start_year = df.start_year.min()
    end_year = df.end_year.max() + 1 
    year_options = [dict(label=x, value=x) for x in range(int(start_year), int(end_year))]
    testvid_cylces = 'years: {} - {}'.format(start_year, end_year)
    yearslider = dcc.Slider(
        id='rs_year_cylces',
        min=start_year,
        max=end_year,
        marks={i: '{}'.format(i) for i in range(start_year, end_year)},
        step=None,
        value=start_year
    )
    return [crop_options, crops[0],
            location_options, locations[0:3],
            planting_options, planting_starts[0],
            yearslider]


@app.callback(
    Output('testvid_cylces', 'children'),
    #  Output('graph', 'children'),
    [Input('dd_crop_cylces', 'value'), Input('dd_locations_cylces', 'value'), Input('dd_planting_cylces', 'value'),
     Input('rs_year_cylces', 'value'),
     Input('cycles-thread-info','data')],
[State('cycles_thread_id','value')]
)
def update_figure(crop, locations, planting, year, thread_info, thread_id):
    
  if thread_id is None or thread_id == '':
      return "Please enter a threadID to load data"
  if year is None or year == '':
      return "Loading..."
  if planting is None or planting == '':
      return "Loading..."
  if locations is None or locations == '':
      return "Loading..."
  if thread_info is None:
      return "Loading..."

  tablename = thread_info["runs_table"] 

  for item in (crop, locations, planting, year):
    if item is None or item == '':
        return "Please make a selection for all inputs"
    
    ins = thread_info["runs_table"]
    matchcol = "url"
    if tablename == "cycles_0_9_4_alpha_runs":
        matchcol = "id"        
    outs = get_match_from_list(thread_info["output_tables"], "cycles_season")
    weathercol = get_match_from_list(thread_info["input_columns"], "cycles_weather")

    if isinstance(locations, list):
        location_list = "','".join(list(locations))
        location_list = "'" + location_list + "'"
    else:
        location_list = "'" + locations + "'"
    query="""SELECT * FROM (SELECT ins.*, outs.grain_yield, EXTRACT(year FROM TO_DATE(outs.date, 'YYYY-MM-DD')) AS year from
            (
            SELECT * FROM
                ((Select {}, x as longitude, y as latitude, CONCAT(ROUND(y::numeric,2)::text ,'Nx',ROUND(x::numeric,2)::text ,'E') as location
                FROM threads_inputs where threadid = '{}') ti
                INNER JOIN
                (select * from {} where threadid = '{}') i
                ON ti.{} = i.{})
            WHERE crop_name LIKE '{}' AND start_planting_day = {}
            AND location IN ({})
            ) ins
            INNER JOIN {} outs
            ON ins.mint_runid = outs.mint_runid) inout
            WHERE inout.year = {} """.format(matchcol,thread_id,ins,thread_id,matchcol,weathercol,crop,planting,location_list,outs,year)

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
