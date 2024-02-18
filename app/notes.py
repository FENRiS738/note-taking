from flask import request, Response, session
from app.models import Note
from app import app, db

@app.post('/dashboard//user/<int:id>/note')
def create_note(id):
    if session['id'] == id:
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.get_json()

            title = json['title']
            content = json['content']
            user_id = id

            new_note = Note(title=title, content=content, user_id=user_id)
            db.session.add(new_note)
            db.session.commit()

            return Response (
                "{'message' : 'Note created successfully!'}",
                status=201,
                mimetype='application/json'
            )

@app.get('/dashboard/user/<int:id>')
def get_all_notes(id):
    if session['id'] == id:
        notes = Note.query.filter_by(user_id=id).all()

        list_of_notes = []

        for note in notes:
            n = note.__dict__
            res = {key: n[key] for key in n.keys() & {'id', 'title', 'content'}}
            list_of_notes.append(res)

        response = {
            'notes' : list_of_notes
        }

        if notes:
            return Response(
                f"{response}",
                status=302,
                mimetype='application/json'
            )
        else:
            return Response(
                "{'message': 'Notes not found!'}",
                status=204,
                mimetype='application/json'
            )
    else:
        return 'Please login first!'