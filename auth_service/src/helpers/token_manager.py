import copy
import datetime
import jwt

from src.helpers.user_verifier import UserVerifier
from src.models import AuthToken


class TokenManager:
    '''
    This class encapsulates all the logic of generating,
    authenticating, and persisting the token.
    '''
    user_verifier = UserVerifier()

    def generate_token(self, credentials):
        '''
          Generate token and persist in database 

          if not exist user with the user_id parsed in credentials param
          raise exception
        '''

        # Verify user_id
        self.user_verifier.verify_by_id(credentials['user_id'])

        # generate token
        payload = self.__generate_payload(credentials)

        token = jwt.encode(payload, self.__private_key(), algorithm='RS256')
        # persist auth_token
        return token

    def __private_key(self):
        '''
          Describe the private RSA key
        '''
        with open('private_key.pem', 'rb') as f:
            return f.read()

    def __generate_payload(self, credentials):
        '''
          Generates payload for token generation
        '''

        payload = copy.copy(credentials)
        payload['exp'] = datetime.timedelta(
            minutes=30) + datetime.datetime.utcnow()

        return payload
