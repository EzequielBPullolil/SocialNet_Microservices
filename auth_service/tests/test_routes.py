import copy
import json
from unittest import TestCase


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
        'email': 'test@mail.com'
    }

    def test_valid_post_request_for_auth_register_endpoint_response_http_status_201(self, client):
        '''
          A valid post request for auth_register consists of: 
            fields:
              name - length >= 4
              password - length > 8 
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

    def test_post_request_auth_register_endpoint_with_invalid_or_missing_name_param_response_http_status_400(self, client):
        '''
          Verify if parse a invalid name response with bad request and status_code 400
          and the expected error json
          keys (status, message, missing_parameters, invalid_parameters)

          example invalid name case:
          {
            'status': 'error',
            'message': 'Bad request, At least one parameter is invalid.'
            'missing_parameters': 
            'invalid_parameters': {
              'name': 'name',
              'value': 'a',
              'reason': 'The field must have a minimum length of 4',
            }
          }
          example missing name case:
          {
            'status': 'error',
            'message': 'Bad request, Missing at least one parameter.',
            'missing_parameters': ['name'],
            'invalid_parameters':'',
          }
        '''

        invalid_name_data = copy.copy(self.register_data)
        invalid_name_data['name'] = 'a'
        response = client.post('/auth/register', json=invalid_name_data)

        assert response.status_code == 400

        invalid_name_data['name'] = ''
        response = client.post('/auth/register', json=invalid_name_data)
        assert response.status_code == 400
