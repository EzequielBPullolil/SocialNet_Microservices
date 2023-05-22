from src.exceptions import AlreadyRegisteredEmail
from src import Session
from src.models import User
import datetime

from src.helpers.email_manager import EmailManager
from src.helpers.password_manager import PasswordManager


class RegisterService:
    '''
    This class encapsulates all the logic of registering a user
    '''
    password_manager = PasswordManager()
    email_manager = EmailManager()

    def register(self, register_data):
        '''
            Register user if the email is not in use and 
            persist an user with encrypted password

            Args: 
                register_data(dict): The register data
                    - 'email': The user email
                    - 'name':  The user name
                    - 'password': The user password
            Return:
                - user_data(dict)
                    - id: The id of register user
                    - name: The name of register user
                    - email: The email of register user

            Raises:
                - AlreadyRegisteredEmail
        '''
        self.__is_avaible_the_email(register_data['email'])

        self.__encrypt_password(register_data['password'])
        user_id = self.__persist_user(register_data)

        return {
            'id': user_id,
            'name': register_data['name'],
            'email': register_data['email']
        }

    def __is_avaible_the_email(self, email):
        '''
            Raises an exception if the email ins not avaible
        '''
        if (not self.email_manager.is_avaible_the_email(email)):
            raise AlreadyRegisteredEmail()

    def __persist_user(self, user_data):
        '''
        Persist user with encrypted password in database 
        and return they user id


        Args: 
                register_data(dict): The register data
                    - 'email': The user email
                    - 'name':  The user name
                    - 'password': The user password
        Return:
            user_id(int): The persisted user id
        '''
        user = User(name=user_data['name'],
                    email=user_data['email'],
                    password=self.encrypted_password)
        session = Session()
        session.add(user)
        session.commit()
        user_id = user.id
        session.close()

        return user_id

    def __encrypt_password(self, password):
        '''
            Encrypt password and save it in encrypted_password property 
        '''
        self.encrypted_password = self.password_manager.encrypt_password(
            password)
