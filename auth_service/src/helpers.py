from . import Session
from .models import User


def validate_user_fields(user: dict):
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

        Raises: ValueError 
    '''

    if (len(user['name']) < 4):
        raise ValueError()


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
