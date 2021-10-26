import sqlite3

import click
import psycopg2
import psycopg2.extras
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        if eval(current_app.config["USE_RDS"]):
            g.db = psycopg2.connect(dbname=current_app.config["DB_NAME"],
                                    host=current_app.config["DB_URI"],
                                    port=current_app.config["DB_PORT"],
                                    user=current_app.config["DB_USER"],
                                    password=current_app.config["DB_PASSWORD"]
                                    )
        else:
            g.db = psycopg2.connect(dbname="adventure")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def db_execute(command, params, commit=False):
    db = get_db()
    cursor = db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute(command, params)
    if commit:
       db.commit()
    return cursor

def db_retest():
    db = get_db()
    cursor = db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute(open("schema.sql", "r").read())
    return
