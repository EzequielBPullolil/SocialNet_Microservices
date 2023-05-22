from datetime import datetime

import pytest
from src.helpers.password_manager import PasswordManager
from src.services.register import RegisterService
from src.models import User
from src import Session
from sqlalchemy import text

from src.exceptions import AlreadyRegisteredEmail


class TestRegisterService:
    '''
        This test verifies that RegisterService works correctly

        Using the following test cases as a guide:
            - Successful register_service call persists a user in the database
            - Cant register the same user email
    '''
    password_manager = PasswordManager()
    register_service = RegisterService()

    def test_successful_register_service_call_persist_a_user_in_the_database(self):
        '''
            Call register_service function and verify if user was persisted
        '''
        userData = {
            'name': '',
            'password': '',
            'email': 'test@email.com'
        }
        self.register_service.register(userData)
        session = Session()
        persisted_user = session.query(
            User).filter_by(email=userData['email']).first()
        session.close()
        assert persisted_user != None

    def test_cant_register_user_with_the_same_email(self, test_user):
        '''
            Call register_service parse an already registered email
            raises exception
        '''

        with pytest.raises(AlreadyRegisteredEmail):
            self.register_service.register(
                {
                    'name': '',
                    'password': '',
                    'email': test_user['email']
                }
            )

    def test_successful_register_persist_user_with_encrypted_password(self):
        userData = {
            'name': 'ezequiel',
            'password': 'ezequiel_password',
            'email': 'encryptedPasswordUser@email.com'
        }
        self.register_service.register(userData)
        session = Session()
        persisted_user = session.query(
            User).filter_by(email=userData['email']).first()

        assert userData['password'] != persisted_user.password

        assert self.password_manager.compare(
            userData['password'],
            persisted_user.password
        ) == True

        session.close()
