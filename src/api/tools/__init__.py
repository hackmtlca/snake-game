from flask import Blueprint, redirect, request, make_response
import os
import glob
import shutil

tools = Blueprint('tools', __name__, url_prefix='/api/tools')

# Method to reset the database.
@tools.route('/reset', methods=['GET', 'POST'])
def reset():
    # Checks if there is a database. If so, delete.
    if os.path.exists('./tmp/database.db'):
        os.remove('./tmp/database.db')

    # Copies the files from data.
    for f in glob.glob(os.path.join('./data', '*.*')):
        shutil.copy(f, './tmp')

    # Revokes the sessions token.
    response = make_response(redirect('/'))
    response.delete_cookie('session')
    return response