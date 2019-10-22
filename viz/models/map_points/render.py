## FOR LIVE
from viz.utils import *
##
#styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
'https://codepen.io/chriddyp/pen/brPBPO.css']

# Mapping MAPBOX_APIKEY
MAPBOX_APIKEY = "pk.eyJ1IjoibHBlYXJzb24tbWFwcyIsImEiOiJjazE3MHZ4Z3UxYmY2M2RvM2Q0YmhzNnQ4In0.ero49roJ3zegSqMEhx7E4Q"

## LAYOUT ##
# Layout
def generate_layout(thread_id):
    # load_spatial_data(thread_id)
    return html.Div([
        dcc.Store(id='e-cols'),
        dcc.Store(id='e-data'),
        html.Div([
            html.Label('Thread id'),
            dcc.Input(id='thread_id', value=thread_id, type='text', style={"width": "33%"}),
        ]),
        html.H2('Map Data'),
        html.Div([
            html.Div([
                html.Div(id='div-map'),
                html.Div(id='testdiv'),
            ],className='six columns'),
            html.Div([
                html.Div(id='map-selections'),
            ],className="six columns"),
        ],className='row')
        ])


## FUNCTIONS ##
def fix_dbname(name):
    return name.strip().lower().replace(' ', '_').replace('(',
        '').replace(')', '').replace('%', 'percentage').replace('/',
        '_per_').replace('.', '_').replace('-', '_')

def load_spatial_data(thread_id):
    if thread_id is not None:
        if ' ' in thread_id:
            return None
        if thread_id.isalnum():
            spatial_query = "SELECT DISTINCT threadid, x as lon, y as lat, id from threads_inputs where threadid='{}' and spatial_type = 'Point';".format(thread_id)
            spatial_df = pd.DataFrame(pd.read_sql(spatial_query, con))
            if spatial_df.empty:
                return None
            return spatial_df
        return None
    return None

## CALLBACKS ##
# Build Map
@app.callback(Output('div-map', 'children'),
              [Input('thread_id', 'value')])
def update_output(thread_id):
    if thread_id == '':
        return ['Please enter a thread ID']
    if ' ' in thread_id or thread_id.isalnum()==False:
        return ['Please enter a properly formatted threadid.']
    if thread_id.isalnum():
        df = load_spatial_data(thread_id)
        if df is None:
            return ['This thread has no Spatial data']
        fig = px.scatter_mapbox(df, lat="lat", lon="lon",
                                color_discrete_sequence=["fuchsia"], zoom=6, height=300)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        kids = [html.P('Please select points from the map below using the plotly selection tools (box or lasso) located in the top right of the map.'),
                    dcc.Graph(id='locations_map',figure=fig)]
        return kids
    # return ['Please enter a properly formatted threadid.']

# Show result of selecting data with either box select or lasso
@app.callback(Output('testdiv','children'),[Input('locations_map','selectedData')])
def selectData(selectData):
    points = selectData['points']
    dfPoints = pd.DataFrame(points)
    dfPoints=dfPoints[['lat','lon']]
    dt_points  = [
        html.P('Selected Data Points'),
        dash_table.DataTable(
                        id='table-selected-points',
                        columns=[{"name": i, "id": i} for i in dfPoints.columns],
                        data=dfPoints.to_dict('records'),
                    )
    ]
    return dt_points

app.layout = generate_layout(thread_id)
