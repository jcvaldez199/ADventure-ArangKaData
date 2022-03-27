import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .temp_setup import test

class PrefixMiddleware(object):

    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):

        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        VIDEOS=os.path.join(app.instance_path, 'videos'),
        JWT_SECRET_KEY=os.environ.get("JWT_SECRET"),
        #SQLALCHEMY_DATABASE_URI=os.environ.get("DB_URI"),
        #SQLALCHEMY_TRACK_MODIFICATIONS=False,
        APPLICATION_ROOT="/api",

        # database config
        DB_PASSWORD=os.environ.get("DB_PASSWORD"),
        DB_URI=os.environ.get("DB_URI"),
        DB_NAME=os.environ.get("DB_NAME"),
        DB_PORT=os.environ.get("DB_PORT"),
        DB_USER=os.environ.get("DB_USER"),
        USE_S3=os.environ.get("USE_S3"),
        USE_RDS=os.environ.get("USE_RDS"),
        ALLOWED_FILENAMES=os.environ.get("ALLOWED_FILENAMES"),
        S3_BUCKET_NAME=os.environ.get("S3_BUCKET_NAME"),
    )
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/api')
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

    # run testing setup
    test.test_setup(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import video
    app.register_blueprint(video.bp)

    from . import route
    app.register_blueprint(route.bp)

    from . import location
    app.register_blueprint(location.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import request
    app.register_blueprint(request.bp)

    from . import gpspoint
    app.register_blueprint(gpspoint.bp)

    from . import customer
    app.register_blueprint(customer.bp)

    return app
