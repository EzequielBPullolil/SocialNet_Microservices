from datetime import datetime
import pytest
from sqlalchemy import text
from src import Session
from src.app import app
from src.helpers.password_manager import PasswordManager
from src.models import User


def pytest_configure():
    '''
        Delete all table rows
    '''
    session = Session()

    session.execute(
        text('DELETE FROM auth_token')
    )

    session.execute(
        text('DELETE FROM users')
    )

    session.commit()
    session.close()

    print("\n")
    print('DB RESET')
    print("\n")


@pytest.fixture
def flask_app():
    global app
    app.testing = True
    client = app.test_client()

    yield app


@pytest.fixture()
def client(flask_app):
    return flask_app.test_client()


@pytest.fixture()
def test_user():
    '''
        Persist an user with encrypted password 
        and return they email and password
    '''
    password_manager = PasswordManager()
    email = 'logintest@test_user.com'
    password = 'password_test'

    session = Session()
    user = User(
        name='',
        email=email,
        password=password_manager.encrypt_password(password)
    )
    session.add(user)
    session.commit()
    id = user.id
    session.close()
    return {
        'user_id': id,
        'email': email,
        'password': password
    }
