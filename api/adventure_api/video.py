from flask import (
    Blueprint,  g, redirect, render_template, request, url_for, jsonify, session, send_from_directory, current_app, send_file
)
from werkzeug.exceptions import abort
from adventure_api.db import get_db, db_execute
from werkzeug.utils import secure_filename
from flask_jwt_extended import ( get_jwt_identity, jwt_required )

from .utils import check_valid_filename

import boto3
import json
import os, sys
import ffmpeg
from flask_cors import cross_origin

bp = Blueprint('video', __name__, url_prefix='/video')

@bp.route('/')
@jwt_required()
def index():

    """ Return all Videos of user in JWT
    """

    db = get_db()
    command = """SELECT * FROM video
                 WHERE userid = %(userid)s;
              """
    params = {'userid':get_jwt_identity()}
    videos = db_execute(command, params).fetchall()
    return jsonify(videos)

@bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_vid():

    """ Uploads a new Video
    """

    if request.method == 'POST':
        db = get_db()
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if (not file.filename == '') and (check_valid_filename(file.filename)):
            # SAVE VIDEO - returns filename, thumbnailname
            _, thumbnailpath = save_video(file)

            fname = file.filename
            command = """INSERT INTO video (filename, userid, thumbnail)
                         VALUES (%(filename)s, %(userid)s, %(thumbnail)s);
                      """
            params = {'filename':fname,
                      'userid':get_jwt_identity(),
                      'thumbnail':thumbnailpath
                      }
            db_execute(command, params, True)
            filename = secure_filename(file.filename)
            return jsonify(params)
        else:
            return "Invalid file", 404

def save_video(file):
    filename = secure_filename(file.filename)
    videopath = os.path.join(current_app.config['VIDEOS'], filename)
    thumbnailpath = None
    file.save(videopath)
    thumbnailpath = generate_thumbnail(videopath, filename)
    if eval(current_app.config["USE_S3"]):
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(Filename=videopath, Bucket=current_app.config["S3_BUCKET_NAME"], Key=filename)
        tb_path_raw = os.path.join(current_app.config['VIDEOS'], thumbnailpath)
        with current_app.open_resource(tb_path_raw) as f:
            s3.Bucket(current_app.config["S3_BUCKET_NAME"]).put_object(Key=thumbnailpath, Body=f)
        if os.path.exists(videopath):
            os.remove(videopath)
        if os.path.exists(tb_path_raw):
            os.remove(tb_path_raw)
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
    return videoname[::-1].split(".",1)[-1][::-1] + "_thumbnail.jpeg"

@bp.route('/display/<filename>')
def display_vid(filename):

    """ Displays a video via filename
    """

    if eval(current_app.config["USE_S3"]):
        s3 = boto3.client('s3')
        gen_url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': current_app.config["S3_BUCKET_NAME"], 'Key': filename},
            ExpiresIn=3600
        )
        return redirect(gen_url, code=302)
    return send_file(current_app.config['VIDEOS']+"/"+secure_filename(filename))

@bp.route('/delete/<filename>', methods=['POST'])
@jwt_required()
def delete_vid(filename):

    """ Deletes a video via filename
        TODO: Delete the actual file as well
    """
    error = None

    if eval(current_app.config["USE_S3"]):
        s3 = boto3.client('s3')
        return '',200

    fname = secure_filename(filename)
    command = """ DELETE FROM video
                  WHERE filename = %(fname)s AND
                  NOT EXISTS (SELECT * FROM request WHERE request.videoname = video.filename) AND
                  userid = %(userid)s;
              """
    params = {'fname':fname,
              'userid':get_jwt_identity()}
    curs = db_execute(command, params, True)
    if curs.rowcount < 1:
        error = "A request currently contains this video, please delete all requests with this video first."

    if error:
        return error,406

    return jsonify({'fname':filename})

@bp.route('/rename/<filename>')
@jwt_required()
def rename_vid(filename):

    """ Renames a video via filename
    """

    req_form = request.get_json()
    newname = secure_filename(req_form['newname'])
    oldname = secure_filename(filename)
    if (not newname):
        return jsonify(error=str("Invalid file")), 404

    if eval(current_app.config["USE_S3"]):
        s3 = boto3.client('s3')
        return '',200

    command = """ UPDATE video SET filename = %(fname)s
                  WHERE userid = %(userid)s AND filename = %(oldname)s;
              """
    params = {'oldname':oldname,
              'newname':newname,
              'userid':get_jwt_identity()
              }
    db_execute(command, params, True)
    return '',200

