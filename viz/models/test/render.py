# dash libs
from dash.dependencies import Input, Output, State

# dash components
import dash_html_components as html

## FOR LIVE
from viz.app import app

## Parse search
from viz.utils import parse_search


#styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
'https://codepen.io/chriddyp/pen/brPBPO.css']

layout = html.Div([
    html.Div(id='test_thread_id')
])


@app.callback(Output(component_id="test_thread_id", component_property='children'),
    inputs=[
        Input('url', component_property='pathname'),
        Input('url', component_property='search')
    ]
)
def obtain_thread_id(pathname, search):
    thread_id = parse_search(search)
    return thread_id

