import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .models import db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        VIDEOS=os.path.join(app.instance_path, 'videos'),
        JWT_SECRET_KEY=os.environ.get("JWT_SECRET"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DB_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    jwt = JWTManager(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    @app.route('/')
    def index():
        return ("Hello World !", 200)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import video
    app.register_blueprint(video.bp)

    #from . import approval
    #app.register_blueprint(approval.bp)

    from . import request
    app.register_blueprint(request.bp)

    return app
