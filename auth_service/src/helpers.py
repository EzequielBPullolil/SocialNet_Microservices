from . import Session
from .models import User


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
