from crypt import methods
from dataclasses import dataclass
import os, pika, time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

from waitress import serve

db_path = 'mysql://main:main@db_main:3306/db_main'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@dataclass
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), unique=True, nullable=False)

@dataclass
class TagConnect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    base_id = db.Column(db.Integer, nullable=False)
    next_id = db.Column(db.Integer, nullable=False)
    UniqueConstraint('base_id', 'next_id', name='base_next_unique')

this_is_prod = True
flask_env = os.environ.get('FLASK_ENV')
if flask_env and flask_env == 'development':
    this_is_prod = False

@app.route('/')
def index():
    return '<p>Hello</p>'

@app.route('/initDb/', methods=['GET'])
def init_db():
    db.create_all()
    return '<p>Init Completed!</p>'

@app.route('/api/tags', methods=['GET'])
def showTags():
    current_tags = Tag.query.all()
    tags_to_show = []
    for t in current_tags:
        tags_to_show.append(str(t.text))
    return '<p>' + '<br/>'.join(tags_to_show) + '</p>'

@app.route('/api/tag/<tagname>', methods='PUT')
def addTag(tagname):
    new_tag = Tag(text=tagname)
    db.session.add(new_tag)
    db.session.commit()
    return '<p>' + str(tagname) + ' added</p>'

if __name__ == "__main__":
    if this_is_prod:
        serve(app, host='0.0.0.0', port=5000)
    else:        
        app.run(debug=True, host='0.0.0.0')


