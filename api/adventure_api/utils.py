from flask import current_app, g
from flask.cli import with_appcontext

# Utility functions

def check_valid_filename(filename):
    """ Return True if filename has allowed extension
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_FILENAMES"]
