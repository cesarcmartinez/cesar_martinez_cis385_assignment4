from flask import Flask, request, jsonify, make_response
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import ForeignKey

# Load environment variables
load_dotenv()

# Initialize flask app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['POSTGRES_DB_CONNECTION_STRING']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(50))

    # define constructor
    def __init__(self, username, password):
        self.username = username
        self.password = password

# User Schema


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password')


# Initialize User schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey(User.id))
    title = db.Column(db.String(50))
    body = db.Column(db.String(255))

    # define constructor
    def __init__(self, userId, title, body):
        self.userId = userId
        self.title = title
        self.body = body

# Note Schema


class NoteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'userId', 'title', 'body')


# Initialize Note schema
note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

# Create a User


@app.route('/user', methods=['POST'])
def add_user():
    name = request.json['username']
    password = request.json['password']

    newUser = User(name, password)
    db.session.add(newUser)
    db.session.commit()
    # return jsonify(newUser)
    return user_schema.jsonify(newUser)

# Update User


@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    username = request.json['username']
    password = request.json['password']

    updateUser = User.query.get(id)
    updateUser.username = username
    updateUser.password = password
    db.session.commit()
    return user_schema.jsonify(updateUser)

# Get Users


@app.route('/user', methods=['GET'])
def get_customers():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

# Get User


@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    single_user = User.query.get(id)
    return user_schema.jsonify(single_user)

# Delete user


@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    delete_user = User.query.get(id)
    db.session.delete(delete_user)
    db.session.commit()

    return user_schema.jsonify(delete_user)

# Create a Note


@app.route('/user/<id>/note', methods=['POST'])
def add_note(id):
    userId = id
    title = request.json['title']
    body = request.json['body']

    newNote = Note(userId, title, body)
    db.session.add(newNote)
    db.session.commit()
    # return jsonify(newNote)
    return note_schema.jsonify(newNote)

# Get Note


@app.route('/user/<id>/notes/<noteId>', methods=['GET'])
def get_note(id, noteId):
    single_note = Note.query.filter_by(id=noteId).first()
    return note_schema.jsonify(single_note)

# Get Notes by User


@app.route('/user/<id>/note', methods=['GET'])
def get_notesByUser(id):
    user_notes = Note.query.filter_by(userId=id)
    results = notes_schema.dump(user_notes)
    return jsonify(results)

# Get Notes by Title


@app.route('/user/<id>/note/<title>', methods=['GET'])
def get_notesByTitle(id, title):
    noteByTitle = Note.query.filter_by(title=title).first()
    return note_schema.jsonify(noteByTitle)

# Update Note by NoteId


@app.route('/user/<id>/note/<noteId>', methods=['PUT'])
def update_noteByNoteId(id, noteId):
    title = request.json['title']
    body = request.json['body']

    single_note = Note.query.get(noteId)
    single_note.title = title
    single_note.body = body

    db.session.commit()
    return note_schema.jsonify(single_note)

# Update Note by Title


@app.route('/user/<id>/notes/<title>', methods=['PUT'])
def update_noteByTitle(id, title):
    titleFromPM = request.json['title']
    body = request.json['body']

    noteByTitle = Note.query.filter_by(title=title).first()
    noteByTitle.title = titleFromPM
    noteByTitle.body = body

    db.session.commit()
    return note_schema.jsonify(noteByTitle)

# Delete Note by NoteId


@app.route('/user/<id>/notes/<noteId>', methods=['DELETE'])
def delete_by_noteId(id, noteId):
    delete_note = Note.query.get(noteId)

    db.session.delete(delete_note)
    db.session.commit()
    return note_schema.jsonify(delete_note)

# Login


@app.route('/login', methods=['GET'])
def login():
    username = request.form['username']
    password = request.form['password']

    userDetails = User.query.filter_by(username=username).first()
    login_username = userDetails.username
    login_password = userDetails.password
    if login_username == username and login_password == password:
        return make_response('Login successful')
    else:
        return make_response('Login unsuccessful')


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
