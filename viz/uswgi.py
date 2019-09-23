from viz import app
from viz.index import *
application = app.server
application.config.suppress_callback_exceptions = True

if __name__ == "__main__":
    application.run()