from distutils import errors
from email.mime import base
import os, pika, time, json

from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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
migrate = Migrate(app, db)

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

@dataclass
class VoteConnect(db.Model):
    id: int
    base_id: int
    vote_id: int
    upvotes: int
    downvotes: int
    id = db.Column(db.Integer, primary_key=True)
    base_id = db.Column(db.Integer, nullable=False)
    vote_id = db.Column(db.Integer, nullable=False)
    upvotes = db.Column(db.Integer, nullable=False)
    downvotes = db.Column(db.Integer, nullable=False)
    UniqueConstraint('base_id', 'vote_id', name='base_vote_unique')


this_is_prod = True
flask_env = os.environ.get('FLASK_ENV')
if flask_env and flask_env == 'development':
    this_is_prod = False


class TagNotFoundException(Exception):
    pass

class IncorrectVotesValue(Exception):
    pass


@app.route('/')
def index():
    testing = ['API:',
        '/api/tags/- GET',
        '/api/votes/ - GET POST',
        '/api/tag/<tagname>/ - GET PUT POST DELETE',
        '/api/connection/ - GET PUT DELETE',
        '/api/vote/up/ - PUT',
        '/api/vote/down/ - PUT',
        ]
    return 'Hello'


@app.route('/api/tags/', methods=['GET'])
def showTags():
    return_resp = ''
    try:
        current_tags = Tag.query.all()
        tags_to_show = []
        for t in current_tags:
            tags_to_show.append(str(t.text))
        return_resp = ' '.join(tags_to_show)
    except Exception as e:
        return_resp = Response(response='Cannot process request ' + str(e.__class__.__name__) + ' ' + str(e), status=500)
    return return_resp

@app.route('/api/votes/', methods=['GET', 'POST'])
def setVotes():
    return_resp = ''
    try:
        if request.method == 'GET':
            current_votes = VoteConnect.query.all()
            votes_to_show = []
            for c in current_votes:
                base_name = str(Tag.query.get(c.base_id).text)
                vote_name = str(Tag.query.get(c.vote_id).text)
                upvotes = str(c.upvotes)
                downvotes = str(c.downvotes)
                votes_to_show.append(base_name + ' > ' + vote_name + ' +' + upvotes + ' -' + downvotes)
            return_resp = '\n'.join(votes_to_show)
        elif request.method == 'POST':
            try:
                json_body = json.loads(request.get_data())
                base_tag = Tag.query.filter_by(text=json_body['base']).first()
                if not base_tag:
                    raise TagNotFoundException(str(json_body['base']) + ' not found')
                vote_tag = Tag.query.filter_by(text=json_body['vote']).first()
                if not vote_tag:
                    raise TagNotFoundException(str(json_body['vote']) + ' not found')
                up_or_down = json_body['up_or_down']
                try:
                    votes = int(json_body['votes'])
                except ValueError:
                    raise IncorrectVotesValue("votes should be integer")
                con_to_vote = VoteConnect.query.filter(
                    and_(VoteConnect.base_id==base_tag.id, VoteConnect.vote_id==vote_tag.id)).first()
                if con_to_vote:
                    if up_or_down == 'up':
                        con_to_vote.upvotes = votes
                    elif up_or_down == 'down':
                        con_to_vote.downvotes = votes
                else:
                    if up_or_down == 'up':
                        con_to_vote = VoteConnect(base_id=base_tag.id, vote_id=vote_tag.id, upvotes=votes, downvotes=0)
                    else:
                        con_to_vote = VoteConnect(base_id=base_tag.id, vote_id=vote_tag.id, upvotes=0, downvotes=votes)
                    db.session.add(con_to_vote)
                db.session.commit()
                base_name = str(Tag.query.get(con_to_vote.base_id).text)
                vote_name = str(Tag.query.get(con_to_vote.vote_id).text)
                upvotes = str(con_to_vote.upvotes)
                downvotes = str(con_to_vote.downvotes)
                return_resp = base_name + ' > ' + vote_name + ' +' + upvotes + ' -' + downvotes
            except KeyError:
                return_resp = Response(response=str(json.loads(request.get_data())) + \
                    ' should have "base", "vote", "up_or_down" and "votes" keys',
                    status=400)
        else:
            return_resp = 'Unsupported request method'
    except json.decoder.JSONDecodeError as e:
        return_resp = Response(response='Cannot load json from ' + str(request.get_data()), status=400)
    except IncorrectVotesValue as e:
        return_resp = Response(response=str(e.__class__.__name__) + ' ' + str(e), status=400)
    except TagNotFoundException as e:            
        return_resp = Response(response=str(e.__class__.__name__) + ' ' + str(e), status=400)
    except Exception as e:
        return_resp = Response(response='Cannot process request ' + str(e.__class__.__name__) + ' ' + str(e), status=500)
    return return_resp

@app.route('/api/tag/<tagname>/', methods=['GET', 'PUT', 'POST', 'DELETE'])
def changeTags(tagname):
    return_resp = ''
    try:
        if request.method == 'GET':
            requested_tag_in_db = Tag.query.filter_by(text=tagname).first()
            tag_names = [ tagname ]
            if requested_tag_in_db:
                print('requested tag in db')
                tags = [ requested_tag_in_db ]
                for tag in tags:
                    for tag_connection in TagConnect.query.filter_by(base_id=tag.id):
                        new_tag = Tag.query.get(tag_connection.next_id)
                        if new_tag.text not in tag_names:
                            tag_names.append(new_tag.text)
                            tags.append(new_tag)
            return_resp = ' '.join(tag_names)
        elif request.method == 'PUT':
            tag_exists_already = db.session.query(Tag).filter_by(text=tagname).first()
            if tag_exists_already:
                return_resp = str(tagname) + ' already exists'
            else:
                db.session.add(Tag(text=tagname))
                db.session.commit()
                return_resp = str(tagname) + ' added'
        elif request.method == 'POST':
            try:
                json_body = json.loads(request.get_data())
                new_text = str(json_body['text'])
                db.session.query(Tag).filter_by(text=tagname).update({'text': new_text})
                db.session.commit()
                return_resp = str(tagname) + ' > ' + str(new_text)
            except KeyError:
                return_resp = Response(response=str(json.loads(request.get_data())) + ' should have "text" key', status=400)
        elif request.method == 'DELETE':
            tag_to_del = Tag.query.filter_by(text=tagname).first()
            if not tag_to_del:
                raise TagNotFoundException(str(tagname) + ' not found')
            for c in TagConnect.query.filter(or_(TagConnect.base_id==tag_to_del.id, TagConnect.next_id==tag_to_del.id)):
                db.session.delete(c)
            for v in VoteConnect.query.filter(or_(VoteConnect.base_id==tag_to_del.id, VoteConnect.vote_id==tag_to_del.id)):
                db.session.delete(v)
            db.session.delete(tag_to_del)
            db.session.commit()
            return_resp = str(tagname) + ' deleted'
        else:
            return_resp = 'Unsupported request method'
    except json.decoder.JSONDecodeError as e:
        return_resp = Response(response='Cannot load json from ' + str(request.get_data()), status=400)
    except TagNotFoundException as e:            
        return_resp = Response(response=str(e.__class__.__name__) + ' ' + str(e), status=400)
    except Exception as e:
        return_resp = Response(response='Cannot process request ' + str(e.__class__.__name__) + ' ' + str(e), status=500)
    return return_resp

@app.route('/api/connection/', methods=['GET', 'PUT', 'DELETE'])
def changeConnections():
    return_resp = ''
    try:
        if request.method == 'GET':
            current_conn = TagConnect.query.all()
            conn_to_show = []
            for c in current_conn:
                base_name = str(Tag.query.get(c.base_id).text)
                next_name = str(Tag.query.get(c.next_id).text)
                conn_to_show.append(base_name + ' > ' + next_name)
            return_resp = '\n'.join(conn_to_show)
        elif request.method == 'PUT':
            try:
                json_body = json.loads(request.get_data())
                base_tag = Tag.query.filter_by(text=json_body['base']).first()
                if not base_tag:
                    raise TagNotFoundException(str(json_body['base']) + ' not found')
                next_tag = Tag.query.filter_by(text=json_body['next']).first()
                if not next_tag:
                    raise TagNotFoundException(str(json_body['next']) + ' not found')
                con_exists_already = TagConnect.query.filter(
                    and_(TagConnect.base_id==base_tag.id, TagConnect.next_id==next_tag.id)).first()
                if con_exists_already:
                    return_resp = str(base_tag.text) + ' > ' + str(next_tag.text) + ' already exists'
                else:
                    db.session.add(TagConnect(base_id=base_tag.id, next_id=next_tag.id))
                    db.session.commit()
                    return_resp = str(base_tag.text) + ' > ' + str(next_tag.text)
            except KeyError as e:
                return_resp = Response(response=str(json.loads(request.get_data())) + \
                    ' should have "base" and "next" keys',
                    status=400)
        elif request.method == 'DELETE':
            try:
                json_body = json.loads(request.get_data())
                base_tag = Tag.query.filter_by(text=json_body['base']).first()
                if not base_tag:
                    raise TagNotFoundException(str(json_body['base']) + ' not found')
                next_tag = Tag.query.filter_by(text=json_body['next']).first()
                if not next_tag:
                    raise TagNotFoundException(str(json_body['next']) + ' not found')
                con_to_del = TagConnect.query.filter(
                    and_(TagConnect.base_id==base_tag.id, TagConnect.next_id==next_tag.id))
                record_deleted = False
                for c in con_to_del:
                    db.session.delete(c)
                    record_deleted = True
                if record_deleted:
                    db.session.commit()
                    return_resp = str(base_tag.text) + ' > ' + str(next_tag.text) + ' deleted'
                else:
                    return_resp = str(base_tag.text) + ' > ' + str(next_tag.text) + ' not found'
            except KeyError as e:
                return_resp = Response(response=str(json.loads(request.get_data())) + \
                    ' should have "base" and "next" keys',
                    status=400)
        else:
            return_resp = 'Unsupported request method'
    except json.decoder.JSONDecodeError as e:
        return_resp = Response(response='Cannot load json from ' + str(request.get_data()), status=400)
    except TagNotFoundException as e:            
        return_resp = Response(response=str(e.__class__.__name__) + ' ' + str(e), status=400)
    except Exception as e:
        return_resp = Response(response='Cannot process request ' + str(e.__class__.__name__) + ' ' + str(e), status=500)
    return return_resp

def vote(base_tag_text, vote_tag_text, up_or_down):
    base_tag = Tag.query.filter_by(text=base_tag_text).first()
    if not base_tag:
        raise TagNotFoundException(str(base_tag_text) + ' not found')
    vote_tag = Tag.query.filter_by(text=vote_tag_text).first()
    if not vote_tag:
        raise TagNotFoundException(str(vote_tag_text) + ' not found')
    con_to_vote = VoteConnect.query.filter(
        and_(VoteConnect.base_id==base_tag.id, VoteConnect.vote_id==vote_tag.id)).first()
    if con_to_vote:
        if up_or_down == 'up':
            con_to_vote.upvotes += 1
        elif up_or_down == 'down':
            con_to_vote.downvotes += 1
    else:
        if up_or_down == 'up':
            db.session.add(
                VoteConnect(base_id=base_tag.id, vote_id=vote_tag.id, upvotes=1, downvotes=0))
        elif up_or_down == 'down':
            db.session.add(
                VoteConnect(base_id=base_tag.id, vote_id=vote_tag.id, upvotes=0, downvotes=1))
    db.session.commit()

@app.route('/api/vote/up/', methods=['PUT'])
def voteUp():
    return_resp = 'Vote Up'
    try:
        json_body = json.loads(request.get_data())
        vote(json_body['base'], json_body['vote'], 'up')
    except KeyError as e:
        return_resp = Response(response=str(json.loads(request.get_data())) + ' should have "base" and "vote" keys',
            status=400)
    except json.decoder.JSONDecodeError as e:
        return_resp = Response(response='Cannot load json from ' + str(request.get_data()), status=400)
    except TagNotFoundException as e:            
        return_resp = Response(response=str(e.__class__.__name__) + ' ' + str(e), status=400)
    except Exception as e:
        return_resp = Response(response='Cannot process request ' + str(e.__class__.__name__) + ' ' + str(e), status=500)
    return return_resp

@app.route('/api/vote/down/', methods=['PUT'])
def voteDown():
    return_resp = 'Vote Down'
    try:
        json_body = json.loads(request.get_data())
        vote(json_body['base'], json_body['vote'], 'down')
    except KeyError as e:
        return_resp = Response(response=str(json.loads(request.get_data())) + ' should have "base" and "vote" keys',
            status=400)
    except json.decoder.JSONDecodeError as e:
        return_resp = Response(response='Cannot load json from ' + str(request.get_data()), status=400)
    except TagNotFoundException as e:            
        return_resp = Response(response=str(e.__class__.__name__) + ' ' + str(e), status=400)
    except Exception as e:
        return_resp = Response(response='Cannot process request ' + str(e.__class__.__name__) + ' ' + str(e), status=500)
    return return_resp


if __name__ == "__main__":
    if this_is_prod:
        serve(app, host='0.0.0.0', port=5000)
    else:        
        app.run(debug=True, host='0.0.0.0')


