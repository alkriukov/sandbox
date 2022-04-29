import os, json

from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import UniqueConstraint, or_, and_
from dataclasses import dataclass


db_path = os.environ.get('DB_PATH')
if not db_path:
    db_path = 'mysql://main:main@localhost:18003/db_main'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migration_dir = 'migrations_' + str(db_path.rsplit('/', 1)[-1])
migrate = Migrate(app, db, directory=migration_dir)

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


class ElElementNotFoundError(Exception):
    pass

class ElementAlreadyExistsError(Exception):
    pass

class IncorrectInputValueError(Exception):
    pass


def apiShowTags():
    resp_text = ''
    resp_status = 200
    db_changed = False
    try:
        current_tags = Tag.query.all()
        tags_to_show = []
        for t in current_tags:
            tags_to_show.append(str(t.text))
        resp_text = ' '.join(tags_to_show)
    except Exception as e:
        resp_text = 'Cannot process request ' + str(e.__class__.__name__) + ' ' + str(e)
        resp_status = 500
    return Response(response=resp_text, status=resp_status), db_changed

def apiChangeTags(request_method, request_data, tagname):
    resp_text = ''
    resp_status = 200
    db_changed = False
    try:
        if not tagname or len(tagname)<=1:
            raise IncorrectInputValueError('Specified tag name is too short')
        if request_method == 'GET':
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
            resp_text = '#' + ' #'.join(tag_names)
        elif request_method == 'PUT':
            tag_exists_already = db.session.query(Tag).filter_by(text=tagname).first()
            if tag_exists_already:
                raise ElementAlreadyExistsError(str(tagname) + ' already exists')
            db.session.add(Tag(text=tagname))
            resp_text = str(tagname) + ' added'
            db.session.commit()
            db_changed = True
        elif request_method == 'POST':
            try:
                json_body = json.loads(request_data)
                new_text = str(json_body['text'])
                if not new_text or len(new_text)<=1:
                    raise IncorrectInputValueError('Specified text value is too short')
                db.session.query(Tag).filter_by(text=tagname).update({'text': new_text})
                resp_text = str(tagname) + ' > ' + str(new_text)
                db.session.commit()
            except KeyError:
                resp_text = str(json.loads(request_data)) + ' should have "text" key'
                resp_status = 400
            db_changed = True
        elif request_method == 'DELETE':
            tag_to_del = Tag.query.filter_by(text=tagname).first()
            if not tag_to_del:
                raise ElElementNotFoundError(resp_text = str(tagname) + ' not found')
            for c in TagConnect.query.filter(or_(TagConnect.base_id==tag_to_del.id, TagConnect.next_id==tag_to_del.id)):
                db.session.delete(c)
            for v in VoteConnect.query.filter(or_(VoteConnect.base_id==tag_to_del.id, VoteConnect.vote_id==tag_to_del.id)):
                db.session.delete(v)
            db.session.delete(tag_to_del)
            resp_text = str(tagname) + ' deleted'
            db.session.commit()
            db_changed = True
        else:
            resp_text = 'Unsupported request method'
            resp_status = 400
    except ElementAlreadyExistsError as e:
        resp_text = str(e.__class__.__name__) + ' ' + str(e)
    except ElElementNotFoundError as e:            
        resp_text = str(e.__class__.__name__) + ' ' + str(e)
    except json.decoder.JSONDecodeError as e:
        resp_text = 'Cannot load json from ' + str(request_data)
        resp_status = 400
    except Exception as e:
        resp_text = 'Cannot process request ' + str(e.__class__.__name__) + ' ' + str(e)
        resp_status = 500
    return Response(response=resp_text, status=resp_status), db_changed

def apiChangeConnections(request_method, request_data):
    resp_text = ''
    resp_status = 200
    db_changed = False
    try:
        if request_method == 'GET':
            current_conn = TagConnect.query.all()
            conn_to_show = []
            for c in current_conn:
                base_name = str(Tag.query.get(c.base_id).text)
                next_name = str(Tag.query.get(c.next_id).text)
                conn_to_show.append(base_name + ' > ' + next_name)
            resp_text = '\n'.join(conn_to_show)
        elif request_method == 'PUT':
            try:
                json_body = json.loads(request_data)
                base_tag = Tag.query.filter_by(text=json_body['base']).first()
                if not base_tag:
                    raise ElElementNotFoundError(str(json_body['base']) + ' not found')
                next_tag = Tag.query.filter_by(text=json_body['next']).first()
                if not next_tag:
                    raise ElElementNotFoundError(str(json_body['next']) + ' not found')
                con_exists_already = TagConnect.query.filter(
                    and_(TagConnect.base_id==base_tag.id, TagConnect.next_id==next_tag.id)).first()
                if con_exists_already:
                    raise ElementAlreadyExistsError(str(base_tag.text) + ' > ' + str(next_tag.text) + ' already exists')
                db.session.add(TagConnect(base_id=base_tag.id, next_id=next_tag.id))
                resp_text = str(base_tag.text) + ' > ' + str(next_tag.text)
                db.session.commit()
                db_changed = True
            except KeyError as e:
                resp_text = str(json.loads(request_data)) + ' should have "base" and "next" keys'
                resp_status = 400
        elif request_method == 'DELETE':
            try:
                json_body = json.loads(request_data)
                base_tag = Tag.query.filter_by(text=json_body['base']).first()
                if not base_tag:
                    raise ElElementNotFoundError(str(json_body['base']) + ' not found')
                next_tag = Tag.query.filter_by(text=json_body['next']).first()
                if not next_tag:
                    raise ElElementNotFoundError(str(json_body['next']) + ' not found')
                con_to_del = TagConnect.query.filter(
                    and_(TagConnect.base_id==base_tag.id, TagConnect.next_id==next_tag.id))
                record_deleted = False
                for c in con_to_del:
                    db.session.delete(c)
                    record_deleted = True
                if not record_deleted:
                    raise ElElementNotFoundError(str(base_tag.text) + ' > ' + str(next_tag.text) + ' not found')
                resp_text = str(base_tag.text) + ' > ' + str(next_tag.text) + ' deleted'
                db.session.commit()
                db_changed = True
            except KeyError as e:
                resp_text = str(json.loads(request_data)) + ' should have "base" and "next" keys'
                resp_status = 400
        else:
            resp_text = 'Unsupported request method'
    except ElementAlreadyExistsError as e:
        resp_text = str(e.__class__.__name__) + ' ' + str(e)
    except ElElementNotFoundError as e:            
        resp_text = str(e.__class__.__name__) + ' ' + str(e)
    except json.decoder.JSONDecodeError as e:
        resp_text = 'Cannot load json from ' + str(request_data)
        resp_status = 400
    except Exception as e:
        resp_text = 'Cannot process request ' + str(e.__class__.__name__) + ' ' + str(e)
        resp_status = 500
    return Response(response=resp_text, status=resp_status), db_changed

def apiSetVotes(request_method, request_data):
    resp_text = ''
    resp_status = 200
    db_changed = False
    try:
        if request_method == 'GET':
            current_votes = VoteConnect.query.all()
            votes_to_show = []
            for c in current_votes:
                base_name = str(Tag.query.get(c.base_id).text)
                vote_name = str(Tag.query.get(c.vote_id).text)
                upvotes = str(c.upvotes)
                downvotes = str(c.downvotes)
                votes_to_show.append(base_name + ' > ' + vote_name + ' +' + upvotes + ' -' + downvotes)
            resp_text = '\n'.join(votes_to_show)
        elif request_method == 'POST':
            try:
                json_body = json.loads(request_data)
                base_tag = Tag.query.filter_by(text=json_body['base']).first()
                if not base_tag:
                    raise ElElementNotFoundError(str(json_body['base']) + ' not found')
                vote_tag = Tag.query.filter_by(text=json_body['vote']).first()
                if not vote_tag:
                    raise ElElementNotFoundError(str(json_body['vote']) + ' not found')
                up_or_down = json_body['up_or_down']
                try:
                    votes = int(json_body['votes'])
                except ValueError:
                    raise IncorrectInputValueError("votes should be integer")
                con_to_vote = VoteConnect.query.filter(
                    and_(VoteConnect.base_id==base_tag.id, VoteConnect.vote_id==vote_tag.id)).first()
                upvotes = 0
                downvotes = 0
                if con_to_vote:
                    if up_or_down == 'up':
                        con_to_vote.upvotes = votes
                    elif up_or_down == 'down':
                        con_to_vote.downvotes = votes
                    upvotes = con_to_vote.upvotes
                    downvotes = con_to_vote.downvotes
                else:
                    if up_or_down == 'up':
                        con_to_vote = VoteConnect(base_id=base_tag.id, vote_id=vote_tag.id, upvotes=votes, downvotes=0)
                        upvotes = votes
                    else:
                        con_to_vote = VoteConnect(base_id=base_tag.id, vote_id=vote_tag.id, upvotes=0, downvotes=votes)
                        downvotes = votes
                    db.session.add(con_to_vote)
                resp_text = str(json_body['base']) + ' > ' + str(json_body['vote']) + ' +' + str(upvotes) + ' -' + str(downvotes)
                db.session.commit()
                db_changed = True
            except KeyError:
                resp_text = str(json.loads(request_data)) + ' should have "base", "vote", "up_or_down" and "votes" keys'
                resp_status = 400
        else:
            resp_text = 'Unsupported request method'
            resp_status = 400
    except ElementAlreadyExistsError as e:
        resp_text = str(e.__class__.__name__) + ' ' + str(e)
    except ElElementNotFoundError as e:            
        resp_text = str(e.__class__.__name__) + ' ' + str(e)
    except IncorrectInputValueError as e:
        resp_text = str(e.__class__.__name__) + ' ' + str(e)
        resp_status = 400
    except json.decoder.JSONDecodeError as e:
        resp_text = 'Cannot load json from ' + str(request_data)
        resp_status = 400
    except Exception as e:
        resp_text = 'Cannot process request ' + str(e.__class__.__name__) + ' ' + str(e)
        resp_status = 500
    return Response(response=resp_text, status=resp_status), db_changed

def apiVote(request_method, request_data, up_or_down):
    resp_text = 'Vote ' + up_or_down
    resp_status = 200
    db_changed = False
    try:
        json_body = json.loads(request_data)
        base_tag = Tag.query.filter_by(text=json_body['base']).first()
        if not base_tag:
            raise ElElementNotFoundError(str(json_body['base']) + ' not found')
        vote_tag = Tag.query.filter_by(text=json_body['vote']).first()
        if not vote_tag:
            raise ElElementNotFoundError(str(json_body['vote']) + ' not found')
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
        db_changed = True
    except KeyError as e:
        resp_text = str(json.loads(request_data)) + ' should have "base" and "vote" keys'
        resp_status = 400
    except json.decoder.JSONDecodeError as e:
        resp_text = 'Cannot load json from ' + str(request_data)
        resp_status = 400
    except ElElementNotFoundError as e:            
        resp_text = str(e.__class__.__name__) + ' ' + str(e)
        resp_status = 400
    except Exception as e:
        resp_text = 'Cannot process request ' + str(e.__class__.__name__) + ' ' + str(e)
        resp_status = 500
    return Response(response=resp_text, status=resp_status), db_changed
