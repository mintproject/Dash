import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from viz.utils import  parse_search
from viz.app import app

from viz.models.cycles_parallel import render as render_cycles_parallel
from viz.models.cycles import render as render_cycles
from viz.models.economic.render import layout as layout_economic
from viz.models.economic_dynamic.render import layout as layout_economic_dynamic
from viz.models.upload.render import layout as layout_upload

THREAD_ID = "thread_id"

#Render format: pass in threadid
CYCLES_PARALLEL = "cycles_parallel"
CYCLES = "cycles"
UPLOAD = "upload"

# Hard Coded Data
ECONOMIC = "economic"
ECONOMIC_DYNAMIC = "economic_dynamic"

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

    return '404'
