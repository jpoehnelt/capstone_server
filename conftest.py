# -*- coding: utf-8 -*-
"""
    tests.conftest
    ~~~~~~~~~~~~~~

    Test fixtures and what not
"""

from capstone_server import app as _app
import pytest


@pytest.fixture(scope='function')
def app():
    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    return _app


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def request_ctx(app, request_jwt):
    headers = request_jwt
    return app.test_request_context("/", headers=headers)
