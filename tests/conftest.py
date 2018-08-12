import pytest
from app import create_app, db


@pytest.fixture
def client():
    app = create_app('testing')
    client = app.test_client()
    db.create_all()
    yield client


