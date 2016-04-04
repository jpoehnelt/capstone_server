# -*- coding: utf-8 -*-
"""
    tests.conftest
    ~~~~~~~~~~~~~~

    Test fixtures and what not
"""

from capstone_server import app as _app, db as _db
import pytest


@pytest.fixture(scope='session')
def app(request):
    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)

    return _app

@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/test'

    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def request_ctx(app, request_jwt):
    headers = request_jwt
    return app.test_request_context("/", headers=headers)
