import pytest
from src.app import app


@pytest.fixture
def flask_app():
    global app
    app.testing = True
    client = app.test_client()

    yield app


@pytest.fixture()
def client(flask_app):
    return flask_app.test_client()
