from datetime import datetime
from src import Session
from src.models import User
from src.helpers.password_manager import PasswordManager


class TestLoginEndpoint:
    '''
    Test for verify the correct operation of Login endpoint


    Use the followin next testcases:
      - valid request for endpoint login response with status 201 and cookie auth_token
      - request endpoint with bad credentials response with status 400 and json with status error
      - Making a request to the login endpoint with the credentials of a user who is already logged in closes the previous session
    '''

    def generate_user_credentials(self):
        '''
          Persist an user and save they
          login credentials 
        '''
        password_manager = PasswordManager()
        email = 'user_login_test@loginendpoint_test.com',
        password = 'password_test'

        session = Session()
        user = User(
            name='',
            email=email,
            password=password_manager.encrypt_password(password),
            created_at=datetime.now()
        )
        session.add(user)
        session.commit()
        self.user_credentials = {
            'email': email,
            'password': password
        }
        session.close()

    def test_valid_request_for_login_endpoint_response_http_status_201(self, client):
        '''
          Makes a request to the endpoint login with valid user credentials
          and verify
        '''
        self.generate_user_credentials()
        response = client.post('/auth/login', json=self.user_credentials)
        assert response.status_code == 201
