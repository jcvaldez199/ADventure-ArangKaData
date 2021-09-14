from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session, send_from_directory, current_app, send_file
)
from werkzeug.exceptions import abort
from adventure.auth import login_required
from adventure.db import get_db, db_execute
from werkzeug.utils import secure_filename

import json
import os


bp = Blueprint('video', __name__, url_prefix='/video')


@bp.route('/', methods=('GET', 'POST'))
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
            command = """INSERT INTO video (filename, userid, hash)
                         VALUES (%(filename)s, %(userid)s, %(hash)s);
                      """
            params = {'filename':fname,'userid':g.user['id'],'hash':fname} 
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
