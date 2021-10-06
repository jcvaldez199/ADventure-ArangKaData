from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session, current_app
)
from werkzeug.exceptions import abort
import json
from adventure_api.db import get_db, db_execute
from flask_jwt_extended import ( get_jwt_identity, jwt_required )

bp = Blueprint('approval', __name__, url_prefix='/approval')

@bp.route('/')
@jwt_required()
def index():
    # NEED TO ONLY WORK FOR ADMIN ACCOUNTS
    if not check_admin(get_jwt_identity()):
       abort(403)

    command = """SELECT * FROM request
                 WHERE (approved = False AND date_created > date_decision)
                    OR (date_decision IS NULL);
              """
    requests = db_execute(command, {}).fetchall()
    return jsonify(requests)

@bp.route('/update', methods=['POST'])
@jwt_required()
def update():

    if not check_admin(get_jwt_identity()):
       abort(403)

    req_form = request.get_json()
    req_id = req_form['req_id']
    decision = req_form['decision']
    remarks = req_form['remarks']
    error = None

    if (not remarks):
        error = 'missing field.'

    if error is not None:
        return jsonify(error=error)

    else:
        command = """ UPDATE request SET (approved, remarks, date_decision)
                      = (%(decision)s, %(remarks)s, CURRENT_TIMESTAMP)
                      WHERE id = %(id)s;
                  """
        params = {'decision':decision
                  ,'id':req_id
                  ,'remarks':remarks
                 }
        db_execute(command, params, True)
        return '',204


def check_admin(userid):
    command = 'SELECT isAdmin FROM customer WHERE id = %(userid)s '
    params = {'userid':userid}
    return db_execute(command, params).fetchone()['isadmin']

@bp.route('/send', methods=('GET', 'POST'))
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
            command = """ INSERT INTO request (routename, userid, videohash, locname)
                          VALUES (%(routename)s, %(userid)s, %(videohash)s, %(locname)s);
                      """
            params = {'routename':location['routename'],
                      'userid':g.user['id'],
                      'videohash':get_vid_hash(video),
                      'locname':location['locname']}
            db_execute(command, params, True)
            return redirect(url_for('request.index'))

    return render_template('request/send.html', locations=locations, videos=videos)

def get_request(id):
    command = """ SELECT *
                  FROM request
                  WHERE id = %(id)s;"""
    params = {'id':id}
    req = db_execute(command, params).fetchone()
    return req

def get_customer(id):
    command = """ SELECT *
                  FROM customer
                  WHERE id = %(id)s;"""
    params = {'id':id}
    cust = db_execute(command, params).fetchone()
    return cust
