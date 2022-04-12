import os
import pika
import time

from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy

db_path = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'flask_db.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), unique=True, nullable=False)

    def show(self):
        return self.text

def callback_add_note(ch, method, properties, body):
    print('callback_add_note handled')
    print(body)
    note_text = body
    new_note = Note(text=note_text)
    db.session.add(new_note)
    db.session.commit()
    return

def callback_delete_note(ch, method, properties, body):
    print('callback_delete_note handled')
    print(body)
    note_text = body
    notes_deleted = []
    for note_to_del in Note.query.filter_by(text=note_text):
        notes_deleted.append(note_to_del.show())
        db.session.delete(note_to_del)
    db.session.commit()

amqp_conn_url = os.environ.get('FLASK_AMQP_URL')
pika_params = pika.URLParameters(amqp_conn_url)
pika_params.heartbeat = 0
conn_attempts = 300
while conn_attempts > 0:
    conn_attempts -= 1
    try:
        pika_conn = pika.BlockingConnection(pika_params)
        conn_attempts = 0
    except pika.exceptions.AMQPConnectionError as e:
        print(amqp_conn_url)
        print('AMQPConnectionError. Attempts remaining: ' + str(conn_attempts))
        time.sleep(10)

channel = pika_conn.channel()
channel.queue_declare(queue='add_note')
channel.queue_declare(queue='delete_note')

this_is_prod = True
flask_env = os.environ.get('FLASK_ENV')
if flask_env and flask_env == 'development':
    this_is_prod = False
else:
    channel.basic_consume(queue='add_note', auto_ack=True, on_message_callback=callback_add_note)
    channel.basic_consume(queue='delete_note', auto_ack=True, on_message_callback=callback_delete_note)

@app.route('/')
def hello_world():
    show_api = ['initDb', 'showAll', 'addNote text', 'deleteNotes text']    
    return '<p>API:<br/>' + '<br/>'.join(show_api) + '</p>'

@app.route('/initDb/')
def init_db():
    db.create_all()
    return '<p>Init Completed!</p>'

@app.route('/addNote/')
def add_note():
    note_text = request.args.get('text', default='Note', type=str)
    new_note = Note(text=note_text)
    db.session.add(new_note)
    db.session.commit()
    sent_message = ''
    if this_is_prod:
        channel.basic_publish(exchange='', routing_key='add_note', body=note_text)
        sent_message = 'Sent add_note ' + str(note_text)
    return '<p>' + note_text + ' - Added. ' + sent_message + '</p>'

@app.route('/deleteNotes/')
def delete_note():
    note_text = request.args.get('text', type=str)
    notes_deleted = []
    for note_to_del in Note.query.filter_by(text=note_text):
        notes_deleted.append(note_to_del.show())
        db.session.delete(note_to_del)
    db.session.commit()
    sent_message = ''
    if this_is_prod:
        channel.basic_publish(exchange='', routing_key='delete_note', body=note_text)
        sent_message = 'Sent delete_note ' + str(note_text)
    return '<p>' + '<br/>'.join(notes_deleted) + ' - Deleted. ' + sent_message + '</p>'

@app.route('/showAll/')
def say_i_run_on_flask():
    existing_notes = Note.query.all()
    notes_text = []
    for n in existing_notes:
        notes_text.append(n.show())
    return '<p>' + '<br/>'.join(notes_text) + '</p>'

if __name__ == "__main__":
    flask_env = os.environ.get('FLASK_ENV')
    if flask_env and flask_env == 'development':
        app.run(debug=True, host='0.0.0.0')

