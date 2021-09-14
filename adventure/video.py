from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session
)
from werkzeug.exceptions import abort
import json
from adventure.auth import login_required
from adventure.db import get_db, db_execute


bp = Blueprint('video', __name__, url_prefix='/video')

@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload_vid():
    db = get_db()
    if request.method == 'POST':
        fname = request.form['filename']
        error = None

        if not fname:
            error = 'missing field.'

        if error is not None:
            flash(error)

        else:
            db.execute(
                # filename is the hash for now
                'INSERT INTO video (filename, userid, hash)'
                ' VALUES (%s, %s, %s)',
                (fname, g.user['id'], fname)
            )
            db.commit()
            return redirect(url_for('request.send'))
    return render_template('video/upload.html')

