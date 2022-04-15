
import os, pika, time, json

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint, or_, and_
from dataclasses import dataclass

from waitress import serve

db_path = os.environ.get('DB_PATH')
if not db_path:
    db_path = 'mysql://main:main@db_main:3306/db_main'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@dataclass
class Tag(db.Model):
    id: int
    text: str
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), unique=True, nullable=False)

@dataclass
class TagConnect(db.Model):
    id: int
    base_id: int
    next_id: int
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


@app.route('/api/tags/', methods=['GET'])
def showTags():
    current_tags = Tag.query.all()
    tags_to_show = []
    for t in current_tags:
        tags_to_show.append(str(t.text))
    return ' '.join(tags_to_show)

@app.route('/api/tag/<tagname>/', methods=['GET', 'PUT', 'POST', 'DELETE'])
def changeTag(tagname):
    resp_text = ''
    if request.method == 'GET':
        tags = [ Tag.query.filter_by(text=tagname).first() ]
        tag_names = [ tagname ]
        for tag in tags:
            for tag_connection in TagConnect.query.filter_by(base_id=tag.id):
                new_tag = Tag.query.get(tag_connection.next_id)
                tags.append(new_tag)
                tag_names.append(new_tag.text)
        resp_text = ' '.join(tag_names)
    elif request.method == 'PUT':
        db.session.add(Tag(text=tagname))
        db.session.commit()
        resp_text = str(tagname) + ' added'
    elif request.method == 'POST':
        json_body = json.loads(request.get_data())
        new_text = str(json_body['text'])
        db.session.query(Tag).filter_by(text=tagname).update({'text': new_text})
        db.session.commit()
        resp_text = str(tagname) + ' > ' + str(new_text)
    elif request.method == 'DELETE':
        tag_to_del = Tag.query.filter_by(text=tagname).first()
        con_to_del = TagConnect.query.filter(or_(TagConnect.base_id==tag_to_del.id, TagConnect.next_id==tag_to_del.id))
        for c in con_to_del:
            db.session.delete(c)
        db.session.delete(tag_to_del)
        db.session.commit()
        resp_text = str(tagname) + ' deleted'
    else:
        resp_text = 'Unsupported request method'
    return resp_text

@app.route('/api/connection/', methods=['GET', 'PUT', 'DELETE'])
def changeConnection():
    resp_text = ''
    if request.method == 'GET':
        current_conn = TagConnect.query.all()
        conn_to_show = []
        for c in current_conn:
            base_tag_name = Tag.query.get(c.base_id)
            next_tag_name = Tag.query.get(c.next_id)
            conn_to_show.append(str(base_tag_name) + '>' + str(next_tag_name))
        resp_text = ' '.join(conn_to_show)
    elif request.method == 'PUT':
        json_body = json.loads(request.get_data())
        base_tag = Tag.query.filter_by(text=json_body['base']).first()
        next_tag = Tag.query.filter_by(text=json_body['next']).first()
        db.session.add(TagConnect(base_id=base_tag.id, next_id=next_tag.id))
        db.session.commit()
        resp_text = str(base_tag.text) + ' > ' + str(next_tag.text)
    elif request.method == 'DELETE':
        json_body = json.loads(request.get_data())
        base_tag = Tag.query.filter_by(text=json_body['base']).first()
        next_tag = Tag.query.filter_by(text=json_body['next']).first()
        con_to_del = TagConnect.query.filter(and_(TagConnect.base_id==base_tag.id, TagConnect.next_id==next_tag.id))
        for c in con_to_del:
            db.session.delete(c)
        db.session.commit()
        resp_text = str(base_tag.text) + ' > ' + str(next_tag.text) + ' deleted'
    else:
        resp_text = 'Unsupported request method'
    return resp_text



if __name__ == "__main__":
    if this_is_prod:
        serve(app, host='0.0.0.0', port=5000)
    else:        
        app.run(debug=True, host='0.0.0.0')


