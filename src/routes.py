from flask import Blueprint, redirect, request, render_template, send_from_directory, g
from src.errors import getLoginErrorMessage

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    # Simple example of using logged_in feature to change layout.
    if g.logged_in:
        return render_template('app.html')
    else:
        return render_template('home.html')

@routes.route('/tools')
def tools():
    return render_template('tools.html')

@routes.route('/public/<path:path>')
def public(path):
    return send_from_directory('./public', path)

@routes.route('/login')
def login():
    # If user is already logged in, simply redirect home.
    if g.logged_in:
        return redirect('/')

    error = request.args.get('error')

    # Depending if there is an error or not, change the render.
    if error:
        return render_template('login.html', error_message=getLoginErrorMessage(error))
    else:
        return render_template('login.html')

@routes.route('/logout')
def logout():
    # Logout using the api (simple redirect).
    return redirect('/api/users/logout')