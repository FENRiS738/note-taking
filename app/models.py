from datetime import datetime
from app import db
import bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self,username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id


class SharedNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serder_id = db.Column(db.Integer, nullable=False)
    reciever_id = db.Column(db.Integer, nullable=False)
    note_id = db.Column(db.Integer, nullable=False)
    shared_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, sender_id, reciever_id, note_id):
        self.serder_id = sender_id
        self.reciever_id = reciever_id
        self.note_id = note_id

class NoteVersionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modified_title = db.Column(db.String(128), nullable=False)
    modified_content = db.Column(db.Text, nullable=False)
    modified_by = db.Column(db.Integer, nullable=False)
    note_id = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __init__(self, modified_title, modified_content, modified_by, note_id):
        self.modified_title = modified_title
        self.modified_content = modified_content
        self.modified_by = modified_by
        self.note_id = note_id