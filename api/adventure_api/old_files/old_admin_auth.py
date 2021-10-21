import functools
import psycopg2

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from adventure.db import get_db, db_execute

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        command = 'SELECT * FROM customer WHERE username = %(username)s'
        params = {'username':username}
        cursor = db_execute(command, params)
        user = cursor.fetchone()

	# temporarily disable password hashing
        if user is None:
            error = 'Incorrect username.'
        elif not user['password'] == password:
            error = 'Incorrect password.'
        #elif not check_password_hash(user['password'], password):
        #    error = 'Incorrect password.'

        cursor.close()
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            if user['isadmin']:
               return redirect(url_for('approval.index')) 
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        command = 'SELECT * FROM customer WHERE id = %(id)s'
        params = {'id':user_id} 
        cursor = db_execute(command, params)
        g.user = cursor.fetchone()
        cursor.close()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


