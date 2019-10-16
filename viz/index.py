import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from viz.app import app
from viz.models.test import render as render_test

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              inputs=[
                  Input('url', component_property='pathname'),
                  Input('url', component_property='search')
              ])
def display_page(pathname, search):
    if pathname:
        model_name = str(pathname).replace('/', '')
        if model_name == "test":
            return render_test.layout

    return '404'
