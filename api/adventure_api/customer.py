from flask import (
    Blueprint, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from flask.json import JSONEncoder
from adventure_api.db import get_db, db_execute
from flask_jwt_extended import ( get_jwt_identity, jwt_required )

bp = Blueprint('customer', __name__, url_prefix='/customer')

@bp.route('/metrics', methods=['GET'])
@jwt_required()
def metrics():

    if request.method == 'GET':
        command = "SELECT * FROM metrics WHERE userid = %(userid)s"
        params = {'userid':get_jwt_identity()}
        metrics = db_execute(command, params).fetchall()
        return jsonify(metrics)
