import os

from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_migrate import Migrate

from auth import login_manager, CustomSessionInterface
from database import db
from api.expenses.model import *
from api.incomes.model import *
from api.savings.model import *
from api.auth.model import *


def register_routes(api):
    from api import register_routes
    register_routes(api)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = "heyheyheyhey"
    cors = CORS(app)
    app.config.from_pyfile('/app/settings/settings.py', silent=False)
    app.session_interface = CustomSessionInterface()

    # configure the app    
    app.config.from_mapping(
        secret_key='dev',
    )
    
    if test_config is not None:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    db.init_app(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

def init_api(app):
    return Api(app, version='1.0', title='jMoney API',
        description='A Rest API to manage personal finances',
    )


app = create_app()
api = init_api(app)
login_manager.init_app(app)

migrate = Migrate(app, db)
register_routes(api)
