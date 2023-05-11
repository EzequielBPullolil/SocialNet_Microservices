import copy
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

        assert response.status_code == 201

    def test_post_request_auth_register_endpoint_with_invalid_name_response_http_status_400(self, client):
        invalid_name_data = copy.copy(self.register_data)
        invalid_name_data['name'] = 'a'
        response = client.post('/auth/register', json=invalid_name_data)

        assert response.status_code == 400

        invalid_name_data['name'] = ''
        response = client.post('/auth/register', json=invalid_name_data)
        assert response.status_code == 400
