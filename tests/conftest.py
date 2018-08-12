import pytest
import os


# 配置测试环境
def pytest_sessionstart(session):
    os.environ['FLASK_ENV'] = 'testing'
    from app import create_app
    create_app()


@pytest.fixture(scope='session')
def app():
    from flask import current_app
    yield current_app


# from app import create_app

# app=create_app('testing')


def client(app):
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client
    ctx.pop()
