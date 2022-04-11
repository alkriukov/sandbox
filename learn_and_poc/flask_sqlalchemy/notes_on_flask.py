import os
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
    return '<p>' + note_text + ' - Added</p>'

@app.route('/deleteNotes/')
def delete_note():
    note_text = request.args.get('text', type=str)
    notes_deleted = []
    for note_to_del in Note.query.filter_by(text=note_text):
        notes_deleted.append(note_to_del.show())
        db.session.delete(note_to_del)
    db.session.commit()
    return '<p>' + '<br/>'.join(notes_deleted) + ' - Deleted</p>'

@app.route('/showAll/')
def say_i_run_on_flask():
    existing_notes = Note.query.all()
    notes_text = []
    for n in existing_notes:
        notes_text.append(n.show())
    return '<p>' + '<br/>'.join(notes_text) + '</p>'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

