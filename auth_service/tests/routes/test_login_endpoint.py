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

    def test_valid_request_response_http_status_201(self, client, test_user):
        '''
          Makes a request to the endpoint login with valid user credentials
          and verify
        '''
        response = client.post('/auth/login', json=test_user)
        assert response.status_code == 201

        json_body = response.get_json()

        assert json_body['status'] == 'success'
        assert json_body['message'] == 'Successful login'
        assert json_body['token'] != None

    def test_request_with_bad_credentials_response_with_status_400(self, client):
        '''
          Makes a request with credentials of unregistered user
        '''
        response = client.post('/auth/login', json={
            'email': 'no_registeredemail@test.com',
            'password': 'a-asd__sadadd'
        })
        assert response.status_code == 400
