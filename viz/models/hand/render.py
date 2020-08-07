## FOR LIVE
from viz.utils import *
from viz.load_data import *

#styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
'https://codepen.io/chriddyp/pen/brPBPO.css']

# Mapbox setup
mapbox_url = "https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{{z}}/{{x}}/{{y}}{{r}}?access_token={access_token}"
mapbox_token ="pk.eyJ1IjoiaGVscGZ1bHRhbmdlbnQiLCJhIjoiY2tka3F2N3JmMGN1czJya3lnazA2cXIwbiJ9._NRiyORkWgoUuLJV9H3iYg"  # settings.MAPBOX_TOKEN



#pk.eyJ1IjoibHBlYXJzb24tbWFwcyIsImEiOiJjazRhZDh5djQwMnpuM2dud3RpbXp2MGNrIn0.ohZKBd1TFwW85VjKje4DAg

# Manipulate Data FUNCTIONS
# Get MINT API data

#Generate map functions
def render_geotiff(geotiff_file, geotiff_id, center, bounds):
    color_domain = dict(domainMin=0, domainMax=20, colorscale=['orange', 'yellow','green','blue'])
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'},
              center= center,
              bounds = bounds,
              #center = [0, 0],
               #zoom = 10,
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
    # get center and bounds from GeoTIFF
    geotiff_details = get_geotiff_details(geotiff_file)
    dlayout=html.Div([
        html.H5('HAND data visualization'),
        html.Div(render_geotiff(geotiff_file,'hand_raster',geotiff_details['center'],geotiff_details['bounds']))
    ])
    return dlayout
