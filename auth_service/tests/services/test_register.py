from src.services.register import register_service
from src.models import User
from unittest import TestCase
from src import Session


class TestRegisterService(TestCase):
    '''
        This test verifies that RegisterService works correctly

        Using the following test cases as a guide:
            - Successful register_service call persists a user in the database
            - Cant register the same user email
    '''

    def setUp(self) -> None:
        self.session = Session()

    def tearDown(self) -> None:
        self.session.close()

    def test_successful_register_service_call_persist_a_user_in_the_database(self):
        '''
            Call register_service function and verify if user was persisted
        '''
        userData = {
            'email': 'test@email.com'
        }
        register_service(user_data=userData)

        persisted_user = self.session.query(
            User).filter_by(email=userData['email']).first()
        self.assertIsNotNone(persisted_user)
