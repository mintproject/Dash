import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import numpy as np

from viz.app import app

layout = html.Div([
    html.H1(children='Cat Happiness Data'),
    html.Img(src='/assets/cat.jpg')
])