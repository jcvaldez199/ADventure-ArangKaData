import psycopg2
import subprocess
import psycopg2.extras
from adventure_api.db import db_execute, get_db, close_db, get_gps_collection
from werkzeug.security import generate_password_hash
from flask import current_app, g
from flask.cli import with_appcontext
import pymongo
import gpxpy

def setup_db(fname):
    database = get_db()
    cursor = database.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    with current_app.open_resource(fname) as script:
        cursor.execute(script.read().decode('utf8'))
    return


def edit_customer(userid):
    try:
        command = """ UPDATE customer SET password
                      = %(password)s
                      WHERE id = %(userid)s;
                  """
        params = {'password':generate_password_hash("test"), 'userid':userid}
        db_execute(command, params, True).close()
    except Exception as e:
        print(e)
    return

def edit_admin():
    try:
        command = """ UPDATE admin SET password = %(password)s
                      WHERE username = 'admin';
                  """
        params = {'password':generate_password_hash("admin")}
        db_execute(command, params, True).close()
    except Exception as e:
        print(e)
    return

def reset_collection():
    myclient = pymongo.MongoClient("mongodb://localhost:27017")
    mydb = myclient["mydb"]
    collection = mydb["adventure_gps"]
    collection.drop()

def fill_collection(routename, filename):
    myclient = pymongo.MongoClient("mongodb://localhost:27017")
    mydb = myclient["mydb"]
    collection = mydb["adventure_gps"]

    points = []
    f = open(filename, 'r')
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
    insertlist = [ {"locindex":idx, "loc":point, "routename":routename} for idx, point in enumerate(unique_points) ]
    get_gps_collection().insert_many(insertlist)
    get_gps_collection().create_index( [ ("loc","2dsphere"), ("locindex",1) ] )
    f.close()

def test_setup(app):
    with app.app_context():
        setup_db("schema.sql")
        edit_customer(1)
        edit_customer(2)
        edit_admin()
        reset_collection()
        fill_collection("EDSA",current_app.config['VIDEOS']+"/EDSA.gpx")
        fill_collection("CRMT",current_app.config['VIDEOS']+"/CRMT.gpx")

