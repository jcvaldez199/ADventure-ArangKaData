from flask import (
    Blueprint, request, jsonify
)
from adventure_api.db import get_db, db_execute, get_gps_collection
from flask_cors import cross_origin
from datetime import datetime

bp = Blueprint('gps', __name__, url_prefix='/gps')

@bp.route('/')
def index():
    return '',200

# SHOULD APPLY VALIDATION FIXES CURRENTLY THIS IS VERY DANGEROUS
#@bp.route('/ID#<id>+TM#<measuretime>+DT#<measuredate>+LT#<float:latitude>+LN#<float:longitude>+AT#<float:altitude>+SP#<float:speed>+CO#<float:course>')
@bp.route('/id=<int:id>+lat=<float:latitude>+lon=<float:longitude>', methods=['POST'])
def post_gps(id, latitude, longitude):
    if request.method == 'POST':

        # CHECK ASSIGNED ROUTE
        loc_command = 'SELECT routename FROM rpi WHERE id = %(id)s'
        params = {'id':id}
        routename = db_execute(loc_command, params).fetchone()
        if routename:
            routename = routename['routename']
        else:
            error = "RPI not registered"
            return error, 200

        # LOCATION QUERY
        loc_query={
            "loc": {
                "$nearSphere": {
                    "$geometry":{
                        "type":"Point",
                        "coordinates":[longitude, latitude]
                    },
                    "$minDistance": 0,
                    "$maxDistance": 1
                }
            },
            "routename":routename
        }
        locs = get_gps_collection().find(loc_query)
        if locs.count() < 1:
            error = "Too far from route"
            return error, 200
        else:
            locindex = locs[0]['locindex']
            loc_command = """SELECT locname FROM location
                              WHERE routename   = %(routename)s
                                AND startindex <= %(locindex)s
                                AND lastindex  >= %(locindex)s
                                AND locname    != 'Entire'
                          """
            params = {'routename':routename,
                      'locindex':locindex
                      }
            locnames = db_execute(loc_command, params).fetchall()
            return jsonify(locnames)
        return 'error', 200


        # TODO: GPS tracker for vehicles
        #command = """ INSERT INTO gpspoint
        #              (id, date_created, latitude, longitude, altitude, speed, course)
        #              VALUES
        #              (%(id)s, %(date_created)s, %(latitude)s, %(longitude)s, %(altitude)s, %(speed)s, %(course)s);
        #          """
        #params = {'id':id,
        #          'date_created':transform_date(measuretime, measuredate),
        #          'latitude':latitude,
        #          'longitude':longitude,
        #          'altitude':altitude,
        #          'speed':speed,
        #          'course':course
        #          }
        #db_execute(command, params, True)
    return '',200


def transform_date(measuretime, measuredate):
    return datetime.strptime(measuredate+" "+measuretime, '%Y-%m-%d %H:%M:%S')
