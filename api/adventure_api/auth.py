import functools
import psycopg2

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from adventure_api.db import get_db, db_execute

from flask_jwt_extended import ( create_access_token, get_jwt_identity, jwt_required )

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    # get username and password here
    req = request.get_json()
    username = req['username']
    password = req['password']
    error = None

    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'

    if error is None:
        try:
            command = """INSERT INTO customer (username, password)
                         VALUES (%(username)s, %(password)s);
                      """
            params = {'username':username,
                      'password':generate_password_hash(password)
                      }
            db_execute(command, params, True).close()
            # TEMPORARILY GIVE USER DEFAULT LOCATIONS
            temp_give_locations(username)
        #except db.IntegrityError:
        except Exception as e:
            print(e)
        else:
            return '',204


def temp_give_locations(username):

    command = 'SELECT * FROM customer WHERE username = %(username)s'
    params = {'username':username}
    cursor = db_execute(command, params)
    userid = cursor.fetchone()

    command = """INSERT INTO location (routename, locname, userid)
                 VALUES (%(routename)s, %(locname)s, %(userid)s);
              """
    params = {'routename':"Route A",
              'locname' : "Location Alpha",
              'userid' : userid['id']
              }
    db_execute(command, params, True).close()
    command = """INSERT INTO location (routename, locname, userid)
                 VALUES (%(routename)s, %(locname)s, %(userid)s);
              """
    params = {'routename':"Route A",
              'locname' : "Location Beta",
              'userid' : userid['id']
              }
    db_execute(command, params, True).close()


@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        error = None
        command = 'SELECT * FROM customer WHERE username = %(username)s'
        params = {'username':username}
        cursor = db_execute(command, params)
        user = cursor.fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        cursor.close()
        if error is None:
            access_token = create_access_token(identity=user['id'])
            return jsonify(access_token=access_token)

        return jsonify({'error':error})

        # handle the error here

# requiring the token for accessing 
def user_token_required(route):
    @functools.wraps(route)
    def wrapped_route(**kwargs):
        check_token = False
        if check_token:
            return jsonify(error="not authorized")

        return route(**kwargs)

    return wrapped_route

