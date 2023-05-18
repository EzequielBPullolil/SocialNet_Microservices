import copy
import pytest
from sqlalchemy import text
from src import Session


class TestAuthRoutes:
    '''
        This test verifies that flask /auth routes works correctly

        Using the following test cases as a guide:
            - Valid post request for auth/register response status 201
            - bad request:
              -request auth/register endpoint with invalid name response http status 400

    '''
    register_data = {
        'name': 'Alan',
        'password': '12345678',
        'email': 'test23@mail23.com'
    }

    @pytest.fixture(autouse=True)
    def before_each(self):
        '''
          Delete all rows of users table
        '''
        session = Session()
        session.execute(
            text('DELETE FROM "users"')
        )
        session.commit()
        session.close()

    def test_valid_post_request_for_register_endpoint_response_http_status_201(self, client):
        '''
          Verify if a valid post request response with the following expected
          data: status, message and data

          A valid post request for auth_register consists of: 
            fields:
              name - length >= 4
              password - length >= 8 with numbers, symbols or characters
              email - contain '@'
        '''
        response = client.post('/auth/register', json=self.register_data)
        # Verify status_code and response type
        assert response.status_code == 201
        assert response.content_type == 'application/json'

        # Verify json response key values
        json_response = response.get_json()
        assert 'success' in json_response['status']
        assert 'User successfully registered' in json_response['message']
        assert json_response['data'] != None

        # Verify if response_data match with user fields
        data_response = json_response['data']
        assert data_response['id'] != None
        assert data_response['name'] == self.register_data['name']
        assert data_response['email'] == self.register_data['email']

    def test_post_request_register_endpoint_with_short_password_response_http_status_400(self, client):
        '''
        Verify if parse an short password response with status code 400 and
        the expected json response
        '''
        data_with_short_password = copy.copy(self.register_data)
        data_with_short_password['password'] = 'abcdf#3'  # password length < 8

        response = client.post('/auth/register', json=data_with_short_password)

        assert response.status_code == 400
        json_response = response.get_json()

        assert json_response['status'] == 'error'
        assert json_response['message'] == 'Invalid json schema'

        password_error = json_response['invalid_params']['password']

        assert password_error['message'] == 'The password field must have at least 8 characters'

    def test_post_request_register_endpoint_with_short_name_response_http_status_400(self, client):
        '''
          Verify if parse an short name param response with error status 400
          and the json response have the expecteds keys with they values
        '''

        # Verify invalid name error response
        invalid_name_data = copy.copy(self.register_data)
        invalid_name_data['name'] = 'a'
        response = client.post('/auth/register', json=invalid_name_data)
        assert response.status_code == 400
        json_response = response.get_json()

        assert json_response['status'] == 'error'
        assert json_response['message'] == 'Invalid json schema'

        name_error = json_response['invalid_params']['name']

        assert name_error['message'] == 'The name field must have at least 4 characters'

    def test_post_request_register_endpoint_with_only_lettters_password_response_http_status_code_400(self, client):
        '''
        Verify if parse an password without number or symbol
        response with status code 400 and the expected json response
        '''
        data_with_only_letters_password = copy.copy(self.register_data)
        # password with only letters
        data_with_only_letters_password['password'] = 'abcdfghk'

        response = client.post('/auth/register',
                               json=data_with_only_letters_password)

        assert response.status_code == 400
        json_response = response.get_json()

        assert json_response['status'] == 'error'
        assert json_response['message'] == 'Invalid json schema'

        password_error = json_response['invalid_params']['password']

        assert password_error['message'] == 'The password field must have at least 1 symbol or at least 1 number'
        '''
          Verify if parse a invalid or missing password response with bad request and status_code 400
          and the expected error json
          keys (status, message, missing_parameters, invalid_parameters)

          example invalid name case:
          {
            'status': 'error',
            'message': 'Bad request, At least one parameter is invalid.'
            'missing_parameters': 
            'invalid_parameters': {
              'name': 'password',
              'value': '1234567',
              'reason': 'The field must have a minimum length of 8',
            }
          }
          example missing name case:
          {
            'status': 'error',
            'message': 'Bad request, Missing at least one parameter.',
            'missing_parameters': ['password'],
            'invalid_parameters':'',
          }
        '''
        # Verify invalid name error response
        invalid_password_data = copy.copy(self.register_data)
        invalid_password_data['password'] = '1234567'
        response = client.post('/auth/register', json=invalid_password_data)
        assert response.status_code == 400
        assert response.content_type == 'application/json'
        json_response = response.get_json()

        assert 'error' in json_response['status']
        assert 'Bad request, At least one parameter is invalid' in json_response['message']
        assert json_response['invalid_parameters'] == [
            {
                'name': 'password',
                'value': '1234567',
                'reason': 'The field must have a minimum length of 8',
            }
        ]

        # Verify missing name error response
        del invalid_password_data['password']
        response = client.post('/auth/register', json=invalid_password_data)
        assert response.status_code == 400
        assert response.content_type == 'application/json'
        json_response = response.get_json()

        assert 'error' in json_response['status']
        assert 'Bad request, Missing at least one parameter' in json_response['message']
        assert ['password'] == json_response['missing_parameters']

    def test_missing_any_required_param_response_status_code_400(self, client):
        '''
          Verify if missing any of the following next params (name, password, email) response with status code 400
          and the expected response
        '''
        required_params = ['name', 'password', 'email']

        for missing_param in required_params:
            user_schema = copy.copy(self.register_data)
            del user_schema[missing_param]

            response = client.post('/auth/register', json=user_schema)
            assert response.status_code == 400
            json_response = response.get_json()

            assert json_response['status'] == 'error'
            assert json_response['message'] == 'Invalid json schema'

            assert missing_param in json_response['missing_params']
