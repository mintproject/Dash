## FOR LIVE
from viz.utils import *
from viz.load_data import *

#styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
'https://codepen.io/chriddyp/pen/brPBPO.css']

# Mapbox setup
mapbox_url = "https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{{z}}/{{x}}/{{y}}{{r}}?access_token={access_token}"
mapbox_token ="pk.eyJ1IjoibHBlYXJzb24tbWFwcyIsImEiOiJjazRhZDh5djQwMnpuM2dud3RpbXp2MGNrIn0.ohZKBd1TFwW85VjKje4DAg"  # settings.MAPBOX_TOKEN



# Manipulate Data FUNCTIONS
# Get MINT API data

#Generate map functions
def render_geotiff(geotiff_file, geotiff_id):
    color_domain = dict(domainMin=0, domainMax=20, colorscale=['blue', 'red'])
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'},
               center=[30.1844199, -97.8200228],
               zoom = 10,
               children=[
                   dl.TileLayer(id='baselayer'),
                   dl.GeoTIFFOverlay(id=geotiff_id, interactive=True, url=geotiff_file,  opacity=0.8,
                                      **color_domain
                                     ),
                   dl.Colorbar(width=200, height=20,
                    **color_domain,
                    unit="Feet", style={'color': 'black'}),
               ]),
    ]

# Layout
def generate_layout(scenario_id, subgoal_id, thread_id):
    geotiff_file = ''
    resultsdf = get_MINT_data(scenario_id, subgoal_id, thread_id)
    fileurls = resultsdf[(resultsdf['url'].str.contains('distance-down'))&(~resultsdf['url'].str.contains('image'))]['url']
    newraster = fileurls[fileurls.str.contains('distance-down-raster')]
    if len(newraster) > 0:
        geotiff_file = newraster.iloc[0]
    else:
        geotiff_file = fileurls.iloc[0]
    #cols = df.columns.values.tolist()

    dlayout=html.Div([
        html.H5('HAND data visualization'),
        html.Div(render_geotiff(geotiff_file,'hand_raster'))
    ])
    return dlayout
