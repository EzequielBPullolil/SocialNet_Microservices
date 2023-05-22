import pytest
from src.exceptions import BadLoginCredentials
from src.services.login import LoginService
from unittest import TestCase


class TestLoginService:
    '''
    This test verifies that LoginService works correctly

    Using the following test cases as a guide:
        - Successful login return a JWT token
        - login an unregistered user raises BadLoginCredentials
    '''
    login_service = LoginService()

    def test_successful_login_return_JWT_token(self, test_user):
        '''
          The login method is called with valid login
          credentials and it is verified that it returns a token
        '''

        token = self.login_service.login(test_user)

    def test_bad_login_credentials_raises_exception(self):
        '''
          The login method is called with invalid login
          credentials raises BadLoginCredentials
        '''
        with pytest.raises(BadLoginCredentials):
            self.login_service.login({
                'email': 'nonregistered@email.com',
                'password': 'rsa_as'
            })
