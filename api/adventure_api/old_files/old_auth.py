import functools
import psycopg2

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from adventure.db import get_db, db_execute

from flask_jwt_extended import ( create_access_token, get_jwt_identity, jwt_required )

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                command = "INSERT INTO customer (username, password) VALUES (%(username)s, %(password)s);"
                params = {'username':username, 'password':generate_password_hash(password)}
                db_execute(command, params, True).close()
            #except db.IntegrityError:
            except:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

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

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        cursor.close()
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            if user['isadmin']:
               return redirect(url_for('approval.index'))
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route("/token", methods=["POST"])
def token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

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


