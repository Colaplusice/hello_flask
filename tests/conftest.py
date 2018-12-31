import pytest

import os
from app import create_app, db


#
# def pytest_sessionstart(session):
#     from app import create_app
#     create_app()
#
#
#
# @pytest.fixture(scope="session")
# def app():
#     from flask import current_app
#     print('213')
#     yield current_app
#

#

@pytest.fixture
def client():
    os.environ["FLASK_ENV"] = "testing"
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    db.create_all()
    client = app.test_client()
    yield client
    db.drop_all()
    ctx.pop()
