import psycopg2
import subprocess
import psycopg2.extras
from adventure_api.db import db_execute, get_db, close_db
from werkzeug.security import generate_password_hash
from flask import current_app, g
from flask.cli import with_appcontext

def setup_db(fname):
    database = get_db()
    cursor = database.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    with current_app.open_resource(fname) as script:
        cursor.execute(script.read().decode('utf8'))
    return


def edit_customer():
    try:
        command = """ UPDATE customer SET (password)
                      = (%(password)s)
                      WHERE id = 1;
                  """
        params = {'password':generate_password_hash("test")}
        db_execute(command, params, True).close()
    except Exception as e:
        print(e)
    return

def edit_admin():
    try:
        command = """ UPDATE admin SET (password)
                      = (%(password)s)
                      WHERE username = 'admin';
                  """
        params = {'password':generate_password_hash("admin")}
        db_execute(command, params, True).close()
    except Exception as e:
        print(e)
    return

def test_setup(app):
    with app.app_context():
        setup_db("schema.sql")
        edit_customer()
        edit_admin()

