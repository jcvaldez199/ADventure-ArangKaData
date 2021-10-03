from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session, send_from_directory, current_app, send_file
)
from werkzeug.exceptions import abort
from adventure.auth import login_required
from adventure.db import get_db, db_execute
from werkzeug.utils import secure_filename

import json
import os, sys
import ffmpeg


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
    return jsonify(videos)

@bp.route('/upload', methods=['GET','POST'])
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
            # SAVE VIDEO - returns filename, thumnnailname
            _, thumbnailpath = save_video(file)

            fname = file.filename
            command = """INSERT INTO video (filename, userid, thumbnail)
                         VALUES (%(filename)s, %(userid)s, %(thumbnail)s);
                      """
            params = {'filename':fname,
                      'userid':g.user['id'],
                      'thumbnail':thumbnailpath
                      }
            db_execute(command, params, True)
            flash('Video successfully uploaded and displayed below')
            filename = secure_filename(file.filename)
            return render_template('video/upload.html', filename=filename)

def save_video(file):

    filename = secure_filename(file.filename)
    videopath = os.path.join(current_app.config['VIDEOS'], filename)
    file.save(videopath)
    thumbnailpath = generate_thumbnail(videopath, filename)
    return videopath, thumbnailpath

def generate_thumbnail(videopath, videoname):

    # remove filename extension and add jpef
    thumbnailpath = videopath[::-1].split(".",1)[-1][::-1] + "_thumbnail.jpeg"
    probe = ffmpeg.probe(videopath)
    time = float(probe['streams'][0]['duration']) // 2
    width = probe['streams'][0]['width']
    try:
        (
            ffmpeg
            .input(videopath, ss=time)
            .filter('scale', width, -1)
            .output(thumbnailpath, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)
    return videoname+"_thumbnail.jpeg"


# SHOULD APPLY VALIDATION FIXES CURRENTLY THIS IS VERY DANGEROUS
@bp.route('/display/<filename>')
@login_required
def display_vid(filename):
    return send_file(current_app.config['VIDEOS']+"/"+filename)
