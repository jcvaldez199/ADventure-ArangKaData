from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session, current_app
)
from werkzeug.exceptions import abort
import json
from werkzeug.security import check_password_hash, generate_password_hash
from adventure_api.db import get_db, db_execute, get_gps_collection
from werkzeug.utils import secure_filename
import functools
import gpxpy
import gpxpy.gpx
import os, ast

bp = Blueprint('admin', __name__, url_prefix='/admin')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('admin.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/')
@login_required
def index():
    command = """SELECT * FROM request
                 WHERE (approved = False AND date_created > date_decision)
                    OR (date_decision IS NULL);
              """
    requests = db_execute(command, {}).fetchall()
    return render_template('admin/index.html', requests=requests)

@bp.route('/<int:id>/show', methods=('GET', 'POST'))
@login_required
def show(id):

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

    req = get_request(id)
    customer = get_customer(req['userid'])
    if request.method == 'POST':
        decision = eval(request.form['decision'])
        remarks = request.form['remarks']
        error = None

        if (not remarks):
            error = 'missing field.'

        if error is not None:
            flash(error)

        else:
            command = """ UPDATE request SET (approved, remarks, date_decision)
                          = (%(decision)s, %(remarks)s, CURRENT_TIMESTAMP)
                          WHERE id = %(id)s;
                      """
            params = {'decision':decision
                      ,'id':id
                      ,'remarks':remarks
                     }
            db_execute(command, params, True)
            return redirect(url_for('admin.index'))
    return render_template('admin/show.html', request=req, customer=customer)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if eval(current_app.config["USE_RDS"]):
        print("yeah")
    else:
        print("nay")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        command = 'SELECT * FROM admin WHERE username = %(username)s'
        params = {'username':username}
        cursor = db_execute(command, params)
        user = cursor.fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        cursor.close()
        if error is None:
            session.clear()
            session['admin_name'] = user['username']
            return redirect(url_for('admin.index'))

        flash(error)

    return render_template('admin/login.html')

@bp.before_app_request
def load_logged_in_user():
    admin_name = session.get('admin_name')
    if admin_name is None:
        g.user = None
    else:
        command = 'SELECT * FROM admin WHERE username = %(username)s'
        params = {'username':admin_name}
        cursor = db_execute(command, params)
        g.user = cursor.fetchone()
        cursor.close()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.index'))
#
#
#          ROUTE INSERTION
#
#

@bp.route('/test', methods=['GET'])
@login_required
def leaftest():
    ret_pts = []
    for x in get_gps_collection().find({"routename":'EDSA'},{"_id":0,"loc":1}):
        ret_pts.append(x["loc"])
    center=ret_pts[len(ret_pts)//2]
    return render_template('admin/leaftest.html', coords=ret_pts, center=center)

@bp.route('/upload_route', methods=('GET','POST'))
@login_required
def upload_gpx_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No gpx file selected for uploading')
            return redirect(request.url)
        else:
            routename = file.filename
            filepath = save_route(file)
            insertlist = generate_points(filepath, routename)
            ret_pts = [ x["loc"][::-1] for x in insertlist ]
            center=ret_pts[len(ret_pts)//2]
            return render_template('admin/showroute.html',coords=ret_pts, center=center)
    return render_template('admin/route.html')

@bp.route('/show_route', methods=['POST'])
@login_required
def commit_route():
    if request.method == 'POST':
        if 'routename' not in request.form:
            flash('No routename')
            return redirect(request.url)
        else:
            routename = request.form['routename']
            coords = ast.literal_eval(request.form["coords"])
            insertlist = [{"loc":point, "routename":routename} for point in coords ]
            get_gps_collection().insert_many(insertlist)

            # insert route
            command = """INSERT INTO route (name)
                         VALUES (%(name)s);
                      """
            params = {'name':routename}
            db_execute(command, params, True)

            ## insert location
            customer_command = 'SELECT * FROM customer'
            customers = db_execute(customer_command, {}).fetchall()
            for c in customers:
                command = """INSERT INTO location (userid, locname, routename, startindex, lastindex)
                             VALUES (%(userid)s, %(locname)s, %(routename)s, %(startindex)s, %(lastindex)s);
                          """
                params = {
                    'userid'     :c['id'],
                    'locname'    :"ENTIRE",
                    'routename'  :routename,
                    'startindex' :0,
                    'lastindex'  :len(insertlist) -1
                }
                db_execute(command, params, True)
            flash('Successfully uploaded GPX file')
            return redirect(url_for('admin.index'))

def generate_points(gpx_file_location, routename):
    """
    Parses GPX file to output array of objects
    """
    points = []
    f = open(gpx_file_location, 'r')
    gpx = gpxpy.parse(f)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'time': point.time,
                })
    # filter unique points based on time
    unique_points = list({point['time']:[point['longitude'], point['latitude']] for point in points}.values())
    insertlist = [ {"locindex": idx, "loc":point, "routename":routename} for idx, point in enumerate(unique_points) ]
    f.close()
    return insertlist

def save_route(file):
    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['VIDEOS'], filename)
    file.save(filepath)
    return filepath


# RPI STUFF

@bp.route('/rpi', methods=['GET'])
@login_required
def rpi_handler():
    command = """SELECT id FROM rpi;
              """
    rpis = db_execute(command, {}).fetchall()
    return render_template('admin/rpi.html', rpis=rpis)

@bp.route('/<int:id>/rpi_show', methods=('GET', 'POST'))
@login_required
def rpi_show(id):

    def get_rpi(id):
        command = """ SELECT *
                      FROM rpi
                      WHERE id = %(id)s;"""
        params = {'id':id}
        rpi = db_execute(command, params).fetchone()
        return rpi

    def get_routes():
        command = """ SELECT * FROM route;
                  """
        routes = db_execute(command, {}).fetchall()
        return routes

    rpi = get_rpi(id)
    routes = get_routes()
    if request.method == 'POST':
        newroute = request.form['newroute']
        error = None

        if (not newroute):
            error = 'missing field.'

        if error is not None:
            flash(error)

        else:
            command = """ UPDATE rpi SET routename
                          = %(newroute)s
                          WHERE id = %(id)s;
                      """
            params = {'newroute':newroute
                      ,'id':id
                     }
            db_execute(command, params, True)
            return redirect(url_for('admin.rpi_handler'))
    return render_template('admin/rpi_show.html', rpi=rpi, routes=routes)



