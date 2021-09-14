from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session
)
from werkzeug.exceptions import abort
import json
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('request', __name__)

@bp.route('/')
def index():
    user_id = session.get('user_id')

    if user_id is None:
       return redirect(url_for('auth.login'))
    db = get_db()
    requests = db.execute(
        'SELECT *'
        ' FROM request r'
        ' WHERE userid = ? ',
        (g.user['id'],)
    ).fetchall()
    return render_template('request/index.html', requests=requests)

@bp.route('/send', methods=('GET', 'POST'))
@login_required
def send():
    db = get_db()
    videos = db.execute(
        'SELECT filename'
        ' FROM video'
        ' WHERE userid = ? ',
        (g.user['id'],)
    ).fetchall()

    locations = db.execute(
        'SELECT *'
        ' FROM location'
    ).fetchall()

    if request.method == 'POST':
        video = request.form['video']
        location = json.loads(request.form['location'])
        error = None

        if (not video) or (not location):
            error = 'missing field.'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'INSERT INTO request (routename, userid, videohash, locname)'
                ' VALUES (?, ?, ?, ?)',
                (location['routename'], g.user['id'], get_vid_hash(video) ,location['locname'])
            )
            db.commit()
            return redirect(url_for('request.index'))

    return render_template('request/send.html', locations=locations, videos=videos)

def get_vid_hash(fname):
    vid = get_db().execute(
        'SELECT hash, userid'
        ' FROM video v'
        ' WHERE v.filename = ? AND v.userid = ?',
        (fname,g.user['id'],)
    ).fetchone()

    if vid is None:
        abort(404, f"Video {fname} doesn't exist.")

    if vid['userid'] != g.user['id']:
        abort(403)

    return vid['hash']

def get_request(id):
    req = get_db().execute(
        'SELECT *'
        ' FROM request'
        ' WHERE id = ? AND userid = ?',
        (id,g.user['id'],)
    ).fetchone()

    return req

def get_routes():
    routes = get_db().execute(
        'SELECT *'
        ' FROM route'
    ).fetchall()
    return routes

def get_locations():
    locations = get_db().execute(
        'SELECT *'
        ' FROM location'
    ).fetchall()
    return locations

@bp.route('/<int:id>/show')
@login_required
def show(id):
    req = get_request(id)

    return jsonify(dict(req))

# should be in video blueprint

@bp.route('/upload_vid', methods=('GET', 'POST'))
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
                ' VALUES (?, ?, ?)',
                (fname, g.user['id'], fname)
            )
            db.commit()
            return redirect(url_for('request.send'))
    return render_template('video/upload.html')

# should be in location blueprint

@bp.route('/modify_location', methods=('GET', 'POST'))
@login_required
def modify_location():
    routes = get_routes()
    locations = get_locations()
    if request.method == 'POST':
        db = get_db()
        rname = request.form['route']
        lname = request.form['location']
        error = None

        if (not rname) or (not lname):
            error = 'missing field.'

        if error is not None:
            flash(error)

        else:
            db.execute(
                # filename is the hash for now
                'INSERT INTO location (routename, locname)'
                ' VALUES (?, ?)',
                (rname, lname)
            )
            db.commit()
            return redirect(url_for('request.send'))
    return render_template('location/create.html', routes=routes, locations=locations)
