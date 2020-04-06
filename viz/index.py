import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from viz.utils import  parse_search
from viz.app import app

# Hard Coded models
from viz.models.economic.render import layout as layout_economic
from viz.models.economic_dynamic.render import layout as layout_economic_dynamic
# from viz.models.test_layout.render import layout as layout_test_layout

# Models to take Thread ID
from viz.models.cycles_parallel import render as render_cycles_parallel
from viz.models.cycles import render as render_cycles
from viz.models.upload import render as render_upload
from viz.models.scatter_plot import render as render_scatter_plot
from viz.models.map_points import render as render_map_points
from viz.models.images import render as render_images
from viz.models.leaflet import render as render_leaflet
from viz.models.leaflet_demo import render as render_leaflet_demo # DEMO page for leaflet elements
#from viz.models.modflow import render as render_modflow

from viz.models.covid_texas import render as render_covid_texas

# from viz.models.test_render import render as render_test_render

THREAD_ID = "thread_id"

#Render format: pass in threadid
CYCLES_PARALLEL = "cycles_parallel"
CYCLES = "cycles"
UPLOAD = "upload"
SCATTER_PLOT = "scatter_plot"
MAP_POINTS = "map_points"
IMAGES = "images"
LEAFLET = "leaflet"
LEAFLET_DEMO = "leaflet_demo"  # Use for demoing dash leaflet mapping elements
#MODFLOW = "modflow"
# TEST_RENDER = "test_render"
COVID_TEXAS = "covid_texas"

# Hard Coded Data
ECONOMIC = "economic"
ECONOMIC_DYNAMIC = "economic_dynamic"
# TEST_LAYOUT = "test_layout"

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              inputs=[
                  Input('url', component_property='pathname'),
                  Input('url', component_property='search'),

              ])
def display_page(pathname, search):
    if pathname:
        model_name = str(pathname).replace('/', '')
        thread_id = parse_search(search, "%s" % THREAD_ID)
        if model_name == CYCLES_PARALLEL:
            return render_cycles_parallel.generate_layout(thread_id)
        elif model_name == CYCLES:
            return render_cycles.generate_layout(thread_id)
        elif model_name == ECONOMIC:
            return layout_economic_dynamic
        elif model_name == ECONOMIC_DYNAMIC:
            return layout_economic
        elif model_name == UPLOAD:
            return render_upload.generate_layout(thread_id)
        elif model_name == SCATTER_PLOT:
            return render_scatter_plot.generate_layout(thread_id)
        elif model_name == MAP_POINTS:
            return render_map_points.generate_layout(thread_id)
        elif model_name == IMAGES:
            return render_images.generate_layout(thread_id)
        elif model_name == LEAFLET:
            return render_leaflet.generate_layout(thread_id)
        elif model_name == LEAFLET_DEMO: # Test page: use for testing out new elements
            return render_leaflet_demo.generate_layout(thread_id)
#        elif model_name == MODFLOW:
#            return render_modflow.generate_layout(thread_id)
        elif model_name == COVID_TEXAS:
            return render_covid_texas.generate_layout(thread_id)

#         elif model_name == TEST_RENDER:
#             return render_test_render.generate_layout(thread_id)
#         elif model_name == TEST_LAYOUT:
#             return layout_test_layout
    return 'please enter valid visualization pathname'
