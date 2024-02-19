from flask import session
from app.models import Note, SharedNote

# To cheack whether user logged in or not
def is_logged_in():
    return 'id' in session

# To get recieved notes using note id
def get_current_user_recieved_notes(reciever_id):
    list_of_recieved_notes = []

    recieved_notes_details = SharedNote.query.filter_by(reciever_id = reciever_id).all()

    if len(recieved_notes_details) != 0:
        for recieved_notes_detail in recieved_notes_details:
            note = Note.query.filter_by(id=recieved_notes_detail.note_id).first()
            n = note.__dict__
            res = {key: n[key] for key in n.keys() & {'id', 'title', 'content'}}
            list_of_recieved_notes.append(res)
            return {'recieved notes' : list_of_recieved_notes}
    else:
        return {'recieved notes': "No recieved note avalaible"}


# To get recieved notes using user id
def get_current_user_notes(user_id):
    list_of_notes = []

    notes = Note.query.filter_by(user_id=user_id).all()
    if len(notes) != 0:
        for note in notes:
            n = note.__dict__
            res = {key: n[key] for key in n.keys() & {'id', 'title', 'content'}}
            list_of_notes.append(res)

        return {'notes' : list_of_notes}
    else:
        return {'notes': "No note avalaible"}