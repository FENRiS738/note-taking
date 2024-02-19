from flask import request, Response, session
from app.models import SharedNote, User
from app import app, db
from app.utils import is_logged_in

# Share the note with other users
@app.post('/notes/share')
def share_note():
    try:
        if is_logged_in():
            content_type = request.headers.get('Content-Type')
            if (content_type == 'application/json'):
                json = request.get_json()

                reciever_email = json['reciever_email']
                note_id = json['note_id']

                user = User.query.filter_by(email=reciever_email).first()

                new_note = SharedNote(sender_id=session['id'], reciever_id=user.id, note_id=note_id)
                db.session.add(new_note)
                db.session.commit()

                return Response (
                    "{'message' : 'Note shared successfully!'}",
                    status=201,
                    mimetype='application/json'
                )
        else:
            return Response(
                "{'message' : 'Please login first!'}",
                status=401,
                mimetype='application/json'
            )
    except Exception as ex:
        return {
            'message' : 'Some thing went wrong!',
            'error' : ex.message
        }