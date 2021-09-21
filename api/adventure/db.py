import sqlite3

import click
import psycopg2
import psycopg2.extras
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(dbname="adventure")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    cursor = get_db().cursor()
    
    with current_app.open_resource('schema.sql') as script:
        cursor.execute(script.read().decode('utf8'))
   
    cursor.close()


def db_execute(command, params, commit=False):
    db = get_db()
    cursor = db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute(command, params)
    if commit:
       db.commit()
    return cursor


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
