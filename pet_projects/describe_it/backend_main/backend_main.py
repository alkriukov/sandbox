import os, pika, time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from waitress import serve

db_path = 'postgresql://root:root@db_main:5432/main'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), unique=True, nullable=False)

    def show(self):
        return self.text

this_is_prod = True
flask_env = os.environ.get('FLASK_ENV')
if flask_env and flask_env == 'development':
    this_is_prod = False

@app.route('/')
def index():
    return '<p>Hello</p>'

if __name__ == "__main__":
    if this_is_prod:
        serve(app, host='0.0.0.0', port=5000)
    else:        
        app.run(debug=True, host='0.0.0.0')


