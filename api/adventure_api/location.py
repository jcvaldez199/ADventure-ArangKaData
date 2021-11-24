from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session, send_from_directory, current_app, send_file
)
from werkzeug.exceptions import abort
from adventure_api.db import get_db, db_execute, get_gps_collection
from werkzeug.utils import secure_filename
from flask_jwt_extended import ( get_jwt_identity, jwt_required )

import json
import os, sys
from flask_cors import cross_origin

bp = Blueprint('location', __name__, url_prefix='/location')

@bp.route('/')
@jwt_required()
def index():
    db = get_db()
    command = """SELECT * FROM location"""
    params = {}
    locations = db_execute(command, params).fetchall()
    return jsonify(locations)

# SHOULD APPLY VALIDATION FIXES CURRENTLY THIS IS VERY DANGEROUS
#@bp.route('/<routename>', methods=['GET'])
#def send_route_points(routename):
#    ret_pts = []
#    for x in get_gps_collection().find({"routename":routename},{"_id":0,"loc":1}):
#        ret_pts.append(x["loc"])
#    return jsonify(ret_pts)

@bp.route('/send', methods=['POST'])
@jwt_required()
def send():
    if request.method == 'POST':
        req_form = request.get_json()
        location = req_form['location']
        route = req_form['route']
        startindex = req_form['startindex']
        lastindex = req_form['lastindex']
        error = None

        if (not location):
            error = 'missing field.'

        if error is not None:
            flash(error)

        else:
            command = """INSERT INTO location (userid, locname, routename, startindex, lastindex)
                         VALUES (%(userid)s, %(locname)s, %(routename)s, %(startindex)s, %(lastindex)s);
                      """
            params = {
                'userid'     :get_jwt_identity(),
                'locname'    :location,
                'routename'  :route,
                'startindex' :startindex,
                'lastindex'  :lastindex
            }
            db_execute(command, params, True)
            return jsonify({"locname":location})

