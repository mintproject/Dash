# dash libs
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import json
import time

# dash interactive states
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# dash components
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt

# Plotting graphics
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

## FOR LIVE
from viz.app import app
##

#styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
'https://codepen.io/chriddyp/pen/brPBPO.css']

# set connection string
user = 'viz'
password = 'Zc2D63rSbIko6d'
DATABASE_URI = 'postgres+psycopg2://{}:{}@aws1.mint.isi.edu:5432/publicingestion'.format(user,password)
con = create_engine(DATABASE_URI)


## threadid.  Change to get this from url when avilable.
thread_id = 'b2oR7iGkFEzVgimbNZFO'

layout = html.Div([
    html.H1(children='Loaded me up')
])
