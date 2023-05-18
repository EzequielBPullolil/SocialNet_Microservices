from datetime import datetime
from src.services.register import register_service
from src.models import User
from unittest import TestCase
from src import Session
from sqlalchemy import text

from src.exceptions import AlreadyRegisteredEmail


class TestRegisterService(TestCase):
    '''
        This test verifies that RegisterService works correctly

        Using the following test cases as a guide:
            - Successful register_service call persists a user in the database
            - Cant register the same user email
    '''

    def setUp(self) -> None:
        self.session = Session()
        self.registeredEmail = 'aregistered_email@test.com'

        self.session.add(
            User(
                '',
                self.registeredEmail,
                '',
                datetime.now()
            )
        )
        self.session.commit()

    def tearDown(self) -> None:
        self.session.execute(
            text('DELETe FROM "users"')
        )
        self.session.commit()

    def test_successful_register_service_call_persist_a_user_in_the_database(self):
        '''
            Call register_service function and verify if user was persisted
        '''
        userData = {
            'name': '',
            'password': '',
            'email': 'test@email.com'
        }
        register_service(user_data=userData)

        persisted_user = self.session.query(
            User).filter_by(email=userData['email']).first()
        self.assertIsNotNone(persisted_user)

    def test_cant_register_user_with_the_same_email(self):
        '''
            Call register_service parse an already registered email
            raises exception
        '''

        with self.assertRaises(AlreadyRegisteredEmail):
            register_service(
                user_data={
                    'name': '',
                    'password': '',
                    'email': self.registeredEmail
                }
            )

    def test_successful_register_persist_user_with_encrypted_password(self):
        userData = {
            'name': 'ezequiel',
            'password': 'ezequiel_password',
            'email': 'encryptedPasswordUser@email.com'
        }
        register_service(user_data=userData)

        persisted_user = self.session.query(
            User).filter_by(email=userData['email']).first()
        self.assertIsNotNone(persisted_user)

        self.assertNotEqual(
            userData['password'], persisted_user.password
        )

        self.assertTrue(
            self.password_manager.check_password(
                userData['password'],
                persisted_user.password
            )
        )
