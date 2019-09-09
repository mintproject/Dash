import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from models import *
import importlib

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    try:
        print(pathname)
        model_name = str(pathname).replace('/', '')
        model = importlib.import_module(".%s" % model_name, 'models')
        return model.layout
    except Exception as err:
        print(err)
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
