from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session, send_file, current_app
)
from werkzeug.exceptions import abort
import json
import decimal
from flask.json import JSONEncoder
#from adventure_api.auth import login_required
from adventure_api.db import get_db, db_execute
from flask_jwt_extended import ( get_jwt_identity, jwt_required )

bp = Blueprint('request', __name__, url_prefix='/request')

class JsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return JSONEncoder.default(self, obj)

@bp.route('/')
@jwt_required()
def index():
    command = 'SELECT * FROM request WHERE userid = %(userid)s '
    params = {'userid':get_jwt_identity()}
    requests = db_execute(command, params).fetchall()
    return jsonify(requests)

# TEMPORARY ALL ROUTE
@bp.route('/all')
def show_all():
    command = 'SELECT * FROM request WHERE approved = True'
    params = {}
    requests = db_execute(command, params).fetchall()
    return jsonify(requests)

@bp.route('/send', methods=('GET', 'POST'))
@jwt_required()
def send():
    loc_command = 'SELECT * FROM location WHERE userid = %(userid)s '
    vid_command = 'SELECT filename FROM video WHERE userid = %(userid)s '
    params = {'userid':get_jwt_identity()}
    videos = db_execute(vid_command, params).fetchall()
    locations = db_execute(loc_command, params).fetchall()

    if request.method == 'POST':
        req_form = request.get_json()
        video = req_form['video']
        location = req_form['location']
        route = req_form['route']
        error = None

        if (not video) or (not location):
            error = 'missing field.'

        if error is not None:
            flash(error)

        else:
            command = """ INSERT INTO request (routename, userid, videoname, locname)
                          VALUES (%(routename)s, %(userid)s, %(videoname)s, %(locname)s);
                      """
            params = {'routename':route,
                      'userid':get_jwt_identity(),
                      'videoname':video,
                      'locname':location}
            db_execute(command, params, True)
            return ('', 204)

    current_app.json_encoder = JsonEncoder
    return jsonify(get_route_dict(locations),videos)

@bp.route('/edit/<int:id>', methods=['POST'])
@jwt_required()
def edit(id):
    params = {'userid':get_jwt_identity()}
    if request.method == 'POST':
        req_form = request.get_json()
        video = req_form['video']
        location = req_form['location']
        route = req_form['route']
        error = None

        if (not video) or (not location):
            error = 'missing field.'

        if error is not None:
            flash(error)

        else:
            command = """ UPDATE request SET (routename, videoname, locname, date_created)
                                           = (%(routename)s, %(videoname)s, %(locname)s, CURRENT_TIMESTAMP)
                          WHERE id = %(id)s;
                      """
            params = {'routename':route,
                      'videoname':video,
                      'id':id,
                      'locname':location}
            db_execute(command, params, True)
            return ('', 204)

def get_route_dict(location_dict):
    route_dict = {}
    for loc in location_dict:
        route_dict.setdefault(loc["routename"],[]).append(loc)
    return route_dict

def get_request(id):
    command = """ SELECT *
                  FROM request
                  WHERE id = %(id)s AND userid = %(userid)s;"""
    params = {'id':id, 'userid':get_jwt_identity()}
    req = db_execute(command, params).fetchone()
    return req

def get_routes():
    command = "SELECT * FROM route"
    routes = db_execute(command, {}).fetchall()
    return routes


# should be in location blueprint

@bp.route('/modify_location', methods=('GET', 'POST'))
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

