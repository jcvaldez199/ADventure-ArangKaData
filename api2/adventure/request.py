from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session, send_file, current_app
)
from werkzeug.exceptions import abort
import json
from adventure.auth import login_required
from adventure.db import get_db, db_execute

bp = Blueprint('request', __name__)

@bp.route('/')
def index():
    user_id = session.get('user_id')

    if user_id is None:
       return redirect(url_for('auth.login'))
    command = 'SELECT * FROM request WHERE userid = %(userid)s '
    params = {'userid':g.user['id']} 
    requests = db_execute(command, params).fetchall()
    return render_template('request/index.html', requests=requests)

@bp.route('/send', methods=('GET', 'POST'))
@login_required
def send():
    loc_command = 'SELECT * FROM location WHERE userid = %(userid)s '
    vid_command = 'SELECT filename FROM video WHERE userid = %(userid)s '
    params = {'userid':g.user['id']} 
    videos = db_execute(vid_command, params).fetchall()
    locations = db_execute(loc_command, params).fetchall()

    if request.method == 'POST':
        video = request.form['video']
        location = json.loads(request.form['location'])
        error = None

        if (not video) or (not location):
            error = 'missing field.'

        if error is not None:
            flash(error)

        else:
            command = """ INSERT INTO request (ruestoutename, userid, videoname, locname)
                          VALUES (%(routename)s, %(userid)s, %(videoname)s, %(locname)s);
                      """
            params = {'routename':location['routename'],
                      'userid':g.user['id'],
                      'videoname':video,
                      'locname':location['locname']}
            db_execute(command, params, True)
            return redirect(url_for('request.index'))

    return render_template('request/send.html', locations=locations, videos=videos)

@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    loc_command = 'SELECT * FROM location WHERE userid = %(userid)s '
    vid_command = 'SELECT filename FROM video WHERE userid = %(userid)s '
    params = {'userid':g.user['id']} 
    videos = db_execute(vid_command, params).fetchall()
    locations = db_execute(loc_command, params).fetchall()

    if request.method == 'POST':
        video = request.form['video']
        location = json.loads(request.form['location'])
        error = None

        if (not video) or (not location):
            error = 'missing field.'

        if error is not None:
            flash(error)

        else:
            command = """ UPDATE request SET (routename, videoname, locname)
                                           = (%(routename)s, %(videoname)s, %(locname)s)
                          WHERE id = %(id)s;
                      """
            params = {'routename':location['routename'],
                      'videoname':video,
                      'id':id,
                      'locname':location['locname']}
            db_execute(command, params, True)
            return redirect(url_for('request.show', id=id))

    return render_template('request/send.html', locations=locations, videos=videos)

def get_vid_hash(fname):
    command = """ SELECT hash, userid
                  FROM video
                  WHERE filename = %(filename)s AND userid = %(userid)s;"""
    params = {'filename':fname, 'userid':g.user['id']}
    vid = db_execute(command, params).fetchone()
    if vid is None:
        abort(404, f"Video {fname} doesn't exist.")

    if vid['userid'] != g.user['id']:
        abort(403)

    return vid['hash']

def get_request(id):
    command = """ SELECT *
                  FROM request
                  WHERE id = %(id)s AND userid = %(userid)s;"""
    params = {'id':id, 'userid':g.user['id']}
    req = db_execute(command, params).fetchone()
    return req

def get_routes():
    command = "SELECT * FROM route"
    routes = db_execute(command, {}).fetchall()
    return routes

@bp.route('/<int:id>/show', methods=('GET', 'POST'))
@login_required
def show(id):
    req = get_request(id)
    if request.method == 'POST':
       command = """ UPDATE request SET (date_created)
                     = (CURRENT_TIMESTAMP)
                     WHERE id = %(id)s;
                 """
       params = {'id':id}
       db_execute(command, params, True)
       return redirect(url_for('request.index'))

    return render_template('request/show.html', request=req)

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
                ' VALUES (%s, %s)',
                (rname, lname)
            )
            db.commit()
            return redirect(url_for('request.send'))
    return render_template('location/create.html', routes=routes, locations=locations)

def get_locations():
    locations = get_db().execute(
        'SELECT *'
        ' FROM location'
    ).fetchall()
    return locations

