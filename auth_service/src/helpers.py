from . import Session
from .models import User


class UserFieldsValidator:
    def __init__(self, user_fields: dict):
        self.user_fields = user_fields
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

    def validate_name(self):
        '''
            Validates if name is not None and have len of 4
        '''
        if (len(self.user_fields['name']) < 4):
            self.invalid_parameters.append(
                InvalidParameterInfo(
                    name='name',
                    value=self.user_fields['name'],
                    reason='The field must have a minimum length of 4')
            )
            raise InvalidParameter()

    def get_invalid_parameters(self):
        '''
            Returns all invalid parameters
        '''
        return self.invalid_parameters

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
