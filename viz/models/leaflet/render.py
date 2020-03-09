## FOR LIVE
from viz.utils import *

#styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
'https://codepen.io/chriddyp/pen/brPBPO.css']

# Get files.  Currently from Github: switch this to get from ingestion DATABASE
data_url = 'https://github.com/dhardestylewis/HAND-TauDEM/tree/master/regions/Texas/Travis-10m'
geotiff_file = "/assets/images/leaflet_example/travis.tif" #prj_travis tz850.tiff
bounding_box_file = 'https://github.com/dhardestylewis/HAND-TauDEM/blob/master/regions/Texas/Travis-10m/Travis-DEM-10m-HUC120902050408bufdd-info.json'
GEOTIFF_ID = "geotiff-id-github"
GEOTIFF_MARKER_ID = "geotiff-marker-id-github"

# Mapbox setup
mapbox_url = "https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{{z}}/{{x}}/{{y}}{{r}}?access_token={access_token}"
mapbox_token ="pk.eyJ1IjoibHBlYXJzb24tbWFwcyIsImEiOiJjazRhZDh5djQwMnpuM2dud3RpbXp2MGNrIn0.ohZKBd1TFwW85VjKje4DAg"  # settings.MAPBOX_TOKEN
mapbox_ids = ["light-v9", "dark-v9", "streets-v9", "outdoors-v9", "satellite-streets-v9"]

# Element mapbox_ids
BASE_LAYER_ID = "base-layer-id"
BASE_LAYER_DROPDOWN_ID = "base-layer-drop-down-id"

#Generate map functions
def render_geotiff():
    color_domain = dict(domainMin=00, domainMax=30, colorscale=['blue', 'purple', 'red'])
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'},
               center=[30.1844199, -97.8200228],
               zoom = 10,
               children=[
                   dl.TileLayer(id=BASE_LAYER_ID),
                   dl.GeoTIFFOverlay(id=GEOTIFF_ID, interactive=True, url=geotiff_file,  opacity=0.8,
                                     **color_domain),
                   dl.Colorbar(width=200, height=20, **color_domain, unit="Feet", style={'color': 'black'}),
                   html.Div(id=GEOTIFF_MARKER_ID)
               ]),
    ]

def register_geotiff():
    @app.callback(Output(GEOTIFF_MARKER_ID, 'children'),
                  [Input(GEOTIFF_ID, 'click_lat_lng_val')])
    def geotiff_marker(x):
        if x is not None:
            lat, lon, val = x
            return dl.Marker(position=[lat, lon], icon={
                "iconUrl": "https://github.com/thedirtyfew/dash-leaflet/tree/master/assets/thermometer.png",
                "iconSize": [40, 40],
                "iconAnchor": [20, 36]
            }, children=[
                dl.Tooltip('{:.1f}°C'.format(val))
            ])
        else:
            return None
# Layout
def generate_layout(thread_id):
    dlayout=html.Div([
        html.P('Exmaple Overlay of Geotiff data'),
        html.P("Thread ID: "),
        html.Div([
            html.P('Map Base Layer'),
            dcc.Dropdown(
                id=BASE_LAYER_DROPDOWN_ID,
                options=[{"label": i, "value": mapbox_url.format(id=i, access_token=mapbox_token)} for i in mapbox_ids],
                value=mapbox_url.format(id="light-v9", access_token=mapbox_token)
            )
        ],style={'float':'left','width':'20%','margin-right':'15px'}),
        html.Div(render_geotiff(),style={'float':'left','width':'75%'})
    ])
    return dlayout

