import os
from waitress import serve

import notes_on_flask

flask_env = os.environ.get('FLASK_ENV')
if flask_env and flask_env == 'production':
    serve(notes_on_flask.app, host='0.0.0.0', port=8001)
