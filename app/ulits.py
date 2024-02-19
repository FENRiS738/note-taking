from flask import session

def is_logged_in():
    return 'id' in session