from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy
import src.api.users
import src.api.tools
import src.routes
import os
import shutil
import glob
from src.secrets import JWT_SECRET
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
    try:
        g.user = jwt.decode(request.cookies.get('session'), JWT_SECRET)
        g.logged_in = True
    except:
        g.user = None
        g.logged_in = False

if __name__ == '__main__':
    # Registers the API blueprints.
    app.register_blueprint(src.api.users.users)
    app.register_blueprint(src.api.tools.tools)
    app.register_blueprint(src.routes.routes)

    # Remove debug mode once in production.
    app.run(debug=True, host='0.0.0.0', port=80)
