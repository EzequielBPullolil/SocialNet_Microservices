import copy
import datetime
import jwt
from src.helpers.email_manager import EmailManager
from src.helpers.rsa_manager import RsaManager

from src.helpers.user_verifier import UserVerifier
from src.models import AuthToken
from src import Session


class TokenManager:
    '''
    This class encapsulates all the logic of generating,
    authenticating, and persisting the token.
    '''
    user_verifier = UserVerifier()
    email_manager = EmailManager()
    rsa_manager = RsaManager()

    def generate_token(self, credentials):
        '''
          Generate a token and persist it in the database related to the user_Id 

          Args: 
            credentials (dict): Credentials to generate a token
              The expected keys are:
                - 'email': The user email
                - 'user_id': The user id
              The optionals keys are
                - 'exp': Allows specify how long the token expires
          Returns: 
            str: The generated token
        '''

        # Verify user_id
        self.user_verifier.verify_by_id(credentials['user_id'])

        self.email_manager.email_belongs_to_user(
            email=credentials['email'], id=credentials['user_id'])
        # generate token
        payload = self.__generate_payload(credentials)

        token = jwt.encode(payload,
                           self.rsa_manager.get_private_key(),
                           algorithm='RS256')
        # persist auth_token

        self.__persist_auth_token(token, credentials['user_id'])
        return token

    def authenticate_token(self, token):
        '''
          Authenticates the token passed by parameter using its rsa public key

          The rsa public key is obtained from the token database registry.
        '''
        finded_token = self.__find_token_in_db(token)
        public_key = finded_token.public_key_rsa
        jwt.decode(finded_token.token,
                   public_key,
                   algorithms=['RS256'])

    def __generate_payload(self, credentials):
        '''
          Generates a payload of the credentials.
          By default, if the dictation credentials do not have the 'exp' key,
          it generates a token with an expiration time of 30 minutes.
          Args: 
            credentials (dict): Credentials to generate a token
              The expected keys are:
                - 'email': The user email
                - 'user_id': The user id
              The optionals keys are
                - 'exp': Allows specify how long the token expires
        '''

        payload = copy.copy(credentials)
        if (not 'exp' in credentials):
            payload['exp'] = datetime.timedelta(
                minutes=30) + datetime.datetime.utcnow()

        return payload

    def __persist_auth_token(self, token, user_id):
        '''
          Persist the JWT token in the auth token table with the RSA Public key

          Args:
            - token: The generated JWT token
            - user_id: The user id

          Returns; None
        '''
        session = Session()
        session.add(
            AuthToken(user_id=user_id,
                      token=token,
                      public_key_rsa=self.rsa_manager.get_public_key())
        )

        session.commit()
        session.close()

    def __find_token_in_db(self, token):
        '''
          Looks up the token record in the AuthToken table and returns it

          Args:
            - token(str): The token that is stored in auth_token

          Return: 
            - AuthToken
        '''
        session = Session()

        token = session.query(AuthToken).filter_by(token=token).first()
        session.close()
        return token
