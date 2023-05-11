from unittest import TestCase


class TestAuthRoutes:
    '''
        This test verifies that flask /auth routes works correctly

        Using the following test cases as a guide:
            - Valid post request for auth/register response status 201

    '''

    def test_valid_post_request_for_auth_register_route_response_http_status_201(self, client):
        '''
          A valid post request for auth_register consists of: 
            fields:
              name - length > 4
              password - length > 8 
              email - contain '@'

        '''
        register_data = {
            'name': 'Alan',
            'password': '12345678',
            'email': 'test@mail.com'
        }
        response = client.post('/auth/register', json=register_data)

        assert response.status_code == 201
