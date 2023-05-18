from src.exceptions import AlreadyRegisteredEmail
from src import Session
from src.models import User
import datetime

from src.helpers import is_registered_email, PasswordManager


def register_service(user_data: dict):
    '''
        Encrypt the password and persist user 
        to database
    '''
    password_manager = PasswordManager()
    if (is_registered_email(user_data['email'])):
        raise AlreadyRegisteredEmail()

    encrypted_password = password_manager.encrypt_password(
        user_data['password']
    )

    user = User(name=user_data['name'],
                email=user_data['email'],
                password=encrypted_password,
                created_at=datetime.datetime.now())

    session = Session()
    session.add(user)
    session.commit()

    user_id = user.id
    session.close()

    return user_id
