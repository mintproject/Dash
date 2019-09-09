import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
import pandas as pd
import plotly.graph_objs as go
import numpy as np


layout = html.Div([
    html.H1(children='Cat Happiness Data'),
    html.Img(src='/assets/cat.jpg')
])