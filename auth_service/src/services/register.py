from src import Session
from src.models import User
import datetime


def register_service(user_data: dict):
    '''
        Persist an user to database
    '''
    user = User(name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'],
                created_at=datetime.datetime.now())

    session = Session()

    session.add(user)
    session.commit()

    session.close()
