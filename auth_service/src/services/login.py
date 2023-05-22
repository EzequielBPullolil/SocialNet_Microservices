from src.exceptions import BadLoginCredentials
from src import Session
from src.helpers.password_manager import PasswordManager
from src.models import User


class LoginService:
    '''
    Service in charge of validating user credentials and creating a token
    '''

    def __init__(self) -> None:
        self.password_manager = PasswordManager()

    def login(self, user_credentials):
        '''
            Validates user credentials and 
            return an JWT token
        '''
        self.__validate_user_credentials(user_credentials)
        return ''

    def __validate_user_credentials(self, user_credentials):
        '''
            Search an user by email and compare passwords

            :user_credentials -> dict 
                email: str
                password: str
        '''
        self.__find_user_with_email(user_credentials['email'])
        self.__compare_user_password(user_credentials['password'])

    def __find_user_with_email(self, email):
        '''
            Find user with email {email}
            if they not exist raises BadLoginCredentials
        '''
        session = Session()
        response = session.query(User).filter_by(email=email).first()
        session.close()

        if response == None:
            raise BadLoginCredentials

        self.__user = response

    def __compare_user_password(self, password):
        '''
            Compares the password passed by parameter
            with the password of the user of the __user property
        '''

        if (not self.password_manager.compare(password, self.__user.password)):
            raise BadLoginCredentials
