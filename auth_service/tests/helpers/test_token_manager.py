import jwt
from src.helpers.token_manager import TokenManager
from src.models import AuthToken
from src import Session


class TestTokenManager:
    '''
        This test verifies that TokenManager works correctly

        Using the following test cases as a guide:
            - generate_token method generates valid token
              * assertions: 
                1. is token valid
                2. is encrypted with RSA
            - validate_token raise exception if
              - the token is invalid
              - the token is expired
    '''
    token_manager = TokenManager()
    with open('public_key.pem', 'rb') as f:
        public_key = f.read()

    def test_generate_token_generate_valid_token(self, test_user):
        '''
          Verify if generate_token method generated a
          encrypted WITH RSA token 
        '''
        credentials = {
            "user_id": test_user['user_id'],
            "email": test_user['email']
        }

        token = self.token_manager.generate_token(credentials)
        assert token != None
        # Verify if the token is encrypted using RSA
        header = jwt.get_unverified_header(token)
        assert header['alg'] == 'RS256'

        # Verify the token content
        decoded_token = jwt.decode(
            token, self.public_key,  algorithms=['RS256'])

        assert decoded_token['user_id'] == credentials['user_id']
        assert decoded_token['email'] == credentials['email']

    def test_auth_token_is_persisted(self, test_user):
        '''
            Verify if after generate token is persisted auth_token row 
            with test_user.id
        '''
        credentials = {
            "user_id": test_user['user_id'],
            "email": test_user['email']
        }
        self.token_manager.generate_token(credentials)
        session = Session()
        response = session.query(AuthToken).filter_by(
            user_id=test_user['user_id']).first()

        assert response != None
