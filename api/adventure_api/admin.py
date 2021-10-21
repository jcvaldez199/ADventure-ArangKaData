from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, session, current_app
)
from werkzeug.exceptions import abort
import json
from werkzeug.security import check_password_hash, generate_password_hash
from adventure_api.db import get_db, db_execute
import functools

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

