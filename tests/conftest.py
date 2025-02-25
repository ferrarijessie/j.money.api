import pytest

from sqlalchemy_utils import create_database, database_exists

from app import create_app, init_api, register_routes
from database import db as _db
from auth import login_manager
from .fixtures import *

TEST_DATABASE_URI = "mysql://root:password123@jmoney_db:3306/test_jmoney"

@pytest.fixture(scope="function")
def app():
    app = create_app(test_config={
        "TESTING": True,
        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI,
        'SERVER_NAME': 'localhost'
    })
    
    if not database_exists(TEST_DATABASE_URI):
        create_database(TEST_DATABASE_URI)

    api = init_api(app)
    register_routes(api)
    
    with app.app_context():
        login_manager.init_app(app)
        _db.create_all()
        yield app

        # Close the database session and drop all tables after the session
        _db.session.remove()
        _db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
