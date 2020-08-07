from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
import os
from sqlalchemy import create_engine
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table 
import dash_leaflet as dl

import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

##New Libraries
from sqlalchemy import create_engine
import json
import time
import datetime as dt

# For File Upload
import base64
import io

## FOR LIVE
from viz.app import app
from viz.app import engine



def parse_search(search, key):
    query = urlparse(search).query
    query_dict = parse_qs(query)
    if key in query_dict:
        print("loading {}".format(query_dict[key][0]))
        return query_dict[key][0]
    return None

# ACCESS TOKENS FOR OTHER PRODUCTS
# Mapbox setup
mapbox_url = "https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{{z}}/{{x}}/{{y}}{{r}}?access_token={access_token}"
mapbox_token = os.environ['MAPBOX_TOKEN']
mapbox_ids = ["light-v9", "dark-v9", "streets-v9", "outdoors-v9", "satellite-streets-v9"]


# DATABASE CONNECTION INFORMATION
DATABASES = {
    'production':{
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': os.environ['DATABASE_HOSTNAME'],
        'PORT': 5432,
    },
}

# DATABASES = {
#     'production':{
#         'NAME': 'publicingestion',
#         'USER': 'testing',
#         'PASSWORD': '',
#         'HOST': 'aws1.mint.isi.edu',
#         'PORT': 5432,
#     },
# }

# choose the database to use
db = DATABASES['production']

# construct an engine connection string
engine_string = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
    user = db['USER'],
    password = db['PASSWORD'],
    host = db['HOST'],
    port = db['PORT'],
    database = db['NAME'],
)

con = create_engine(engine_string)
