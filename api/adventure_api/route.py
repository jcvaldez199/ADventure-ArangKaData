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

bp = Blueprint('route', __name__, url_prefix='/route')

@bp.route('/')
@jwt_required()
def index():
    db = get_db()
    command = """SELECT * FROM route"""
    params = {}
    routes = db_execute(command, params).fetchall()
    return jsonify(routes)

# SHOULD APPLY VALIDATION FIXES CURRENTLY THIS IS VERY DANGEROUS
@bp.route('/<routename>', methods=['GET'])
def send_route_points(routename):
    ret_pts = []
    for x in get_gps_collection().find({"routename":routename},{"_id":0,"loc":1}):
        ret_pts.append(x["loc"])
    return jsonify(ret_pts)



