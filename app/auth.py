from flask import request, Response, session
from app import app, db
from app.models import User 

@app.route('/')
def server():
    return "Server is running!"

# Create a single user sign up
@app.post('/signup')
def register():
    try:
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.get_json()

            username = json['username']
            email = json['email']
            password = json['password']

            user = User.query.filter_by(email=email).first()
            
            if user:
                return Response (
                "{'message' : 'User already exists!'}",
                status=406,
                mimetype='application/json'
            )
                
            new_user = User(username=username, email=email, password=password)

            db.session.add(new_user)
            db.session.commit()

            return Response (
                "{'message' : 'User created successfully!'}",
                status=201,
                mimetype='application/json'
            )
    except Exception as ex:
        return {
            'message' : 'Some thing went wrong!',
            'error' : ex.message
        }
    

# Create a simple login
@app.post('/login')
def login():
    try:
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.get_json()

            email = json['email']
            password = json['password']

            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password):
                session['id'] = user.id
                session['username'] = user.username
                session['email'] = user.email

                response = {
                    'message' : 'User logged-in successfully!',
                    'user' : {
                        'id' : user.id,
                        'username' : user.username,
                        'email' : user.email,
                    }
                }

                return Response (
                        f"{response}",
                        status=202,
                        mimetype='application/json'
                    )
            else:
                return Response (
                        "{'message' : 'Please enter valid email & password !'}",
                        status=401,
                        mimetype='application/json'
                    )
    except Exception as ex:
        return {
            'message' : 'Some thing went wrong!',
            'error' : ex.message
        }

@app.get('/logout')
def logout():
    try:
        session.clear()
        return Response (
                        "{'message' : 'User logged-out successfully!'}",
                        status=200,
                        mimetype='application/json'
                    )
    except Exception as ex:
        return {
            'message' : 'Some thing went wrong!',
            'error' : ex.message
        }
