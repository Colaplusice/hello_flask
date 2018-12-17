import pytest

import os
from app import create_app, db


def pytest_sessionstart(session):
    os.environ["FLASK_ENV"] = "testing"
    from app import create_app

    create_app()


@pytest.fixture(scope="session")
def app():
    from flask import current_app

    yield current_app


@pytest.fixture
def client():
    app = create_app("testing")
    client = app.test_client()
    db.create_all()
    yield client
    db.drop_all()
