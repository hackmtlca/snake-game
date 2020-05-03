from flask import Blueprint, redirect, request, make_response
from app import db
from src.errors import LOGIN_ERROR
import hashlib
from src.secrets import PASSWORD_SALT, JWT_SECRET
import jwt

users = Blueprint('users', __name__, url_prefix='/api/users')

# Simple password hashing using SHA256 + Salting.
def salted_sha256(password: str) -> str:
    m = hashlib.sha256()
    m.update((password + PASSWORD_SALT).encode('utf-8'))
    return m.hexdigest()

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    @property
    def init_password(self):
        # Asserts that there is an init_password.
        raise AttributeError('Password not readable')
    
    @init_password.setter
    def init_password(self, init_password):
        self.password = salted_sha256(init_password)

    def check_password(self, password):
        return self.password == salted_sha256(password)

# Attempts to read the information from the session.
# If it fails, it simply redirects home.
@users.route('/me', methods=['GET'])
def me():
    try:
        return jwt.decode(request.cookies.get('session'), JWT_SECRET, algorithm='HS256')
    except:
        return redirect('/')
    
# Generates a JWT Token using a JWT_SECRET and redirects the user home.
def generate_session(user_id: int, username: str) -> str:
    response = make_response(redirect('/'))
    response.set_cookie('session', jwt.encode({'user_id': user_id, 'username': username}, JWT_SECRET, algorithm='HS256'), httponly=True)
    return response

@users.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Gets user with same useraname.
    user = Users.query.filter_by(username=username).first()

    # If the user is none or the password is incorrect, throw error.
    if user == None or not user.check_password(password):
        return redirect('/login?error=' + LOGIN_ERROR.INVALID_USERNAME_PASSWORD.value)
    else:
        return generate_session(user.user_id, user.username)

@users.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    # Checks if there is already a user with the current name.
    if Users.query.filter_by(username=username).first():
        return redirect('/login?error=' + LOGIN_ERROR.USERNAME_EXIST.value)
    else:
        # Adds the user to the database then creates a session token.
        user = Users(username=username, init_password=password)
        db.session.add(user)
        db.session.commit()
        return generate_session(user.user_id, user.username)

@users.route('/logout', methods=['GET'])
def logout():
    # Simply revokes session token.
    response = make_response(redirect('/'))
    response.delete_cookie('session')
    return response