import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from viz.app import app
from viz.models import *
import importlib

from urllib.parse import urlparse, parse_qs   

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
        try:
            model_name = str(pathname).replace('/', '')
            query = urlparse(search).query
            query_dict = parse_qs(query)
            for k, v in query_dict.items():
                print("key: {}, value: {}".format(k,v))
            model = importlib.import_module(".{}".format(model_name), 'viz.models')
            model.load_data(query_dict)
            model = importlib.import_module(".{}.render".format(model_name), 'viz.models')            
            return model.layout
        except Exception as err:
            print("Error:", err)
        
    return '404'