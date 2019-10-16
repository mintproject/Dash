from urllib.parse import urlparse, parse_qs
import os
from sqlalchemy import create_engine

def parse_search(search):
    query = urlparse(search).query
    query_dict = parse_qs(query)
    print(query_dict)
    if "thread_id" in query_dict:
        return query_dict["thread_id"][0]
    return 'b2oR7iGkFEzVgimbNZFO'



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