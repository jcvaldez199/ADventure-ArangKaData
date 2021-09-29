from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session, send_from_directory, current_app, send_file
)
from werkzeug.exceptions import abort
from adventure.auth import login_required
from adventure.db import get_db, db_execute
from werkzeug.utils import secure_filename

import json
import os


bp = Blueprint('video', __name__, url_prefix='/video_api')


@bp.route('/')
@login_required
def index():
    db = get_db()
    command = """SELECT filename FROM video
                 WHERE userid = %(userid)s;
              """
    params = {'userid':g.user['id']}
    videos = db_execute(command, params).fetchall()
    return render_template('video/index.html', videos=videos)

@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload_vid():
    db = get_db()
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        else:
            fname = file.filename
            command = """INSERT INTO video (filename, userid)
                         VALUES (%(filename)s, %(userid)s);
                      """
            params = {'filename':fname,'userid':g.user['id']}
            db_execute(command, params, True)
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['VIDEOS'], filename))
            flash('Video successfully uploaded and displayed below')
            return render_template('video/upload.html', filename=filename)
    return render_template('video/upload.html')

# SHOULD APPLY VALIDATION FIXES CURRENTLY THIS IS VERY DANGEROUS
@bp.route('/display/<filename>')
@login_required
def display_vid(filename):
    return send_file(current_app.config['VIDEOS']+"/"+filename)
