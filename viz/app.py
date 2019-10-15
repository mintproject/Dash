import dash
from sqlalchemy import create_engine
import os

external_stylesheets = []

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True


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

engine = create_engine(engine_string)