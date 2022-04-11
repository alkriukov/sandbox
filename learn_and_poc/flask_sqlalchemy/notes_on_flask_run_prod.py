from waitress import serve

import notes_on_flask

serve(notes_on_flask.app, host='0.0.0.0', port=8001)

