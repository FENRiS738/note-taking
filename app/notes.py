from flask import request, Response, session
from app.models import Note
from app import app, db


@app.get('/notes')
def get_all_notes():
    try:
        if session['id']:
            notes = Note.query.filter_by(user_id=session['id']).all()
            list_of_notes = []
            if len(notes) != 0:

                for note in notes:
                    n = note.__dict__
                    res = {key: n[key] for key in n.keys() & {'id', 'title', 'content'}}
                    list_of_notes.append(res)

                response = {
                    'notes' : list_of_notes
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
    except Exception as ex:
        return 'Please login first!'
    

@app.post('/notes/create')
def create_note():
    try:
        if session['id']:
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
    except Exception as ex:
        return 'Please login first!'
    
@app.get('/notes/<int:id>')
def get_note_by_id(id):
    try:
        if session['id']:
                note = Note.query.filter_by(id=id).first()

                n = note.__dict__
                res = {key: n[key] for key in n.keys() & {'id', 'title', 'content'}}

                return Response (
                    f"{res}",
                    status=201,
                    mimetype='application/json'
                )
    except Exception as ex:
        return 'Please login first!'