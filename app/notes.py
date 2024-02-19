from flask import request, Response, session
from app.models import Note, SharedNote
from app import app, db
from app.utils import is_logged_in, get_current_user_notes, get_current_user_recieved_notes

# Get all current user notes
@app.get('/notes')
def get_all_notes():
    if is_logged_in():
        response = {}
        response.update(get_current_user_notes(session['id']))
        response.update(get_current_user_recieved_notes(session['id']))
        
        return Response(
            f"{response}",
            status=302,
            mimetype='application/json'
        )
    else:
        return 'Please login first!'
    
# Create a new note
@app.post('/notes/create')
def create_note():
    if is_logged_in():
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.get_json()

            title = json['title']
            content = json['content']

            new_note = Note(title=title, content=content, user_id=session['id'])
            db.session.add(new_note)
            db.session.commit()

            return Response (
                "{'message' : 'Note created successfully!'}",
                status=201,
                mimetype='application/json'
            )
    else:
        return 'Please login first!'


# Retrieve a specific note by its ID
@app.get('/notes/<int:id>')
def get_note_by_id(id):
    if is_logged_in():
        note = Note.query.filter_by(id=id, user_id=session['id']).first()

        n = note.__dict__
        res = {key: n[key] for key in n.keys() & {'id', 'title', 'content'}}

        return Response (
            f"{res}",
            status=201,
            mimetype='application/json'
        )
    else:
        return 'Please login first!'