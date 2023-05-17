from . import Session
from .exceptions import MissingParameter, InvalidParameter
from .models import User


class EmailValidator:
    '''
        Class was validate email
    '''

    def validate_domain(self, email: str):
        '''
            Validates email domain
        '''
        return len(self.get_email_domain(email)) >= 6

    def get_email_domain(self, email: str):
        '''
            Return email domain
        '''
        domain_start = 1 + email.find('@')
        domain_end = email.find('.')

        if (domain_end == -1 or domain_start == 0):
            return None

        return email[domain_start:domain_end]


class UserFieldsValidator:
    emailValidator = EmailValidator()

    def __init__(self, user_fields: dict):
        self.user_fields = user_fields
        self.missing_parameters = []
        self.invalid_parameters = []

    def validate_fields(self):
        '''
        Validates that the JSON object representing a user has all the required fields and that
        the fields have the correct data types.

            Args: 
            user (dict): an json object
                - name (str): user name
                    * len >= 4
                - password (str): user password
                    * len > 9
                - email (str): user email
                    * contains '@'

            Raises: [MissingParameter, InvalidParameter] 
        '''
        self.validate_name()
        self.validate_password()
        self.validate_email()

    def validate_name(self):
        '''
            Validates if name is not None and have len of 4
        '''
        if (self.user_fields.get('name') == None):
            self.missing_parameters.append('name')
            raise MissingParameter()

        if (len(self.user_fields['name']) < 4):
            self.invalid_parameters.append(
                InvalidParameterInfo(
                    name='name',
                    value=self.user_fields['name'],
                    reason='The field must have a minimum length of 4')
            )
            raise InvalidParameter()

    def validate_password(self):
        '''
            Validates if name is not None and have len of 4
        '''
        if (self.user_fields.get('password') == None):
            self.missing_parameters.append('password')
            raise MissingParameter()

        if (len(self.user_fields['password']) < 8):
            self.invalid_parameters.append(
                InvalidParameterInfo(
                    name='password',
                    value=self.user_fields['password'],
                    reason='The field must have a minimum length of 8')
            )
            raise InvalidParameter()

    def validate_email(self):
        '''
            Validate if email is not empty and
            the email name and domain have length >= 6
        '''
        if (self.user_fields.get('email') == None):
            self.missing_parameters.append('email')
            raise MissingParameter()

        if (not self.emailValidator.validate_domain(self.user_fields['email'])):
            self.invalid_parameters.append(
                InvalidParameterInfo(
                    name='email',
                    value=self.user_fields['email'],
                    reason='The field must have a minimum length of 6 in email domain'
                )
            )
            raise InvalidParameter

    def get_invalid_parameters(self):
        '''
            Returns all invalid parameters
        '''
        return self.invalid_parameters

    def get_missing_parameters(self):
        return self.missing_parameters


def InvalidParameterInfo(name: str, value: str, reason: str) -> dict:
    '''
        Describes why the parameter are invalid
    '''
    return {
        'name': name,
        'value': value,
        'reason': reason
    }


def is_registered_email(email):
    '''
      Return if exist an user registered with email
    '''
    session = Session()
    response = session.query(
        User
    ).filter_by(email=email).first()
    session.close()
    return (
        response != None
    )


def invalid_params_message(errors) -> dict:
    '''
        Describes an dict of all the invalid params
        and they detailed errors
    '''
    message = {}
    for error in errors:
        if ('name' in error.path):
            message['name'] = invalid_name_message(error)
        if ('email' in error.path):
            message['email'] = invalid_email_message(error)
    return message

def invalid_email_message(email) -> dict:
    '''
            Describes custom message for invalid password
    '''
    email_message = {}
    if ('pattern' in str(email.validator)):
        email_message['message'] = 'Invalid email format'

    return email_message
def invalid_name_message(name) -> dict:
    '''
        Describes custom message for invalid name
    '''
    name_message = {}

    if ('minLength' in str(name.validator)):
        name_message['message'] = 'The name field must have at least 4 characters'

    return name_message
