from datetime import datetime
from flask import Response, session, request
from app.utils import is_logged_in
from app.models import Note, NoteVersionHistory
from app import app, db

# Update an existing note
@app.put('/notes/<int:id>')
def update_note(id):
    if is_logged_in():
        note = Note.query.filter_by(id=id, user_id=session['id']).first()
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json') and note:
            json = request.get_json()

            new_title = json['title']
            new_content = json['content']

            note.title, note.content = new_title, new_content

            new_note_version_history = NoteVersionHistory(modified_title=new_title, modified_content=new_content, note_id=id, modified_by=session['id'])

            db.session.add(new_note_version_history)
            db.session.commit()
            return 'Note updated successfully!'
        else:
            return 'Note not found!'
    else:
        return 'Please login first!'

# GET all the changes associated with the note 
@app.get('/notes/version_history/<int:id>')
def note_version_history(id):
    if is_logged_in():
        note_version_history = NoteVersionHistory.query.filter_by(note_id = id).all()
        list_of_notes_version_history = []
        if len(note_version_history) != 0:

            for note in note_version_history:
                n = note.__dict__
                print(n)
                res = {key: n[key] for key in n.keys() & {'id', 'modified_title', 'modified_content', 'updated_at'}}
                res.update({'updated_at' : res['updated_at'].strftime('%Y-%m-%d, %I:%M:%S')})
                list_of_notes_version_history.append(res)

            response = {
                'notes' : list_of_notes_version_history
            }

            return Response(
                f"{response}",
                status=302,
                mimetype='application/json'
            )
        else:
            return Response(
                "{'message': 'Notes not found!'}",
                status=200,
                mimetype='application/json'
            )
    else:
        return 'Please login first!'