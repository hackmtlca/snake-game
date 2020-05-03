from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy
from src.secrets import JWT_SECRET
import src.routes
import os
import shutil
import glob
import jwt

# Checks if the tmp folder is already init. If not, create folder and copy content over.
if not os.path.exists('./tmp'):
    os.mkdir('./tmp')
    for f in glob.glob(os.path.join('./data', '*.*')):
        shutil.copy(f, './tmp')

# Creates the flask app.
app = Flask(__name__)

# Removes the logging, less overhead.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Generates path to the database file (has to be absolute).
path = ('sqlite:///' + os.path.join(os.path.abspath(os.getcwd()), 'tmp/database.db')).replace('\\', '/')

app.config['SQLALCHEMY_DATABASE_URI'] = path

# Connects database to app.
db = SQLAlchemy(app)

# Method that injects into the `g` variable the logged in state and the user. This make this information available for each view.
@app.before_request
def inject_user_state():
    from src.api.users import Users

    try:
        user = Users.query.filter_by(user_id=jwt.decode(request.cookies.get('session'), JWT_SECRET)['user_id']).first()

        if user == None:
            raise Exception()

        g.user = user
        g.logged_in = True
    except Exception as e:
        g.user = None
        g.logged_in = False

if __name__ == '__main__':
    from src.api.users import users
    from src.routes import routes

    # Registers the API blueprints.
    app.register_blueprint(users)
    app.register_blueprint(routes)

    # Remove debug mode once in production.
    app.run(debug=True, host='0.0.0.0', port=80)
