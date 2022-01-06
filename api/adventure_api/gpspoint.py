from flask import (
    Blueprint, request
)
from adventure_api.db import get_db, db_execute
from flask_cors import cross_origin
from datetime import datetime

bp = Blueprint('gps', __name__, url_prefix='/gps')

@bp.route('/')
def index():
    return '',200

# SHOULD APPLY VALIDATION FIXES CURRENTLY THIS IS VERY DANGEROUS
@bp.route('/ID#<id>+TM#<measuretime>+DT#<measuredate>+LT#<float:latitude>+LN#<float:longitude>+AT#<float:altitude>+SP#<float:speed>+CO#<float:course>')
def post_gps(id, measuretime, measuredate, latitude, longitude, altitude, speed, course ):
    print(id, measuretime, measuredate, latitude, longitude, altitude, speed, course)
    command = """ INSERT INTO gpspoint
                  (id, date_created, latitude, longitude, altitude, speed, course)
                  VALUES
                  (%(id)s, %(date_created)s, %(latitude)s, %(longitude)s, %(altitude)s, %(speed)s, %(course)s);
              """
    params = {'id':id,
              'date_created':transform_date(measuretime, measuredate),
              'latitude':latitude,
              'longitude':longitude,
              'altitude':altitude,
              'speed':speed,
              'course':course
              }
    db_execute(command, params, True)
    return '',200


def transform_date(measuretime, measuredate):
    return datetime.strptime(measuredate+" "+measuretime, '%Y-%m-%d %H:%M:%S')
