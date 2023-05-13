from src.exceptions import AlreadyRegisteredEmail
from src import Session
from src.models import User
import datetime

from src.helpers import is_registered_email


def register_service(user_data: dict):
    '''
        Persist an user to database
    '''

    if (is_registered_email(user_data['email'])):
        raise AlreadyRegisteredEmail()

    user = User(name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'],
                created_at=datetime.datetime.now())

    session = Session()
    session.add(user)
    session.commit()

    user_id = user.id
    session.close()

    return user_id
