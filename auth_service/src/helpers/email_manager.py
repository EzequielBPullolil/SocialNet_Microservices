from src import Session
from src.models import User


class EmailManager:
    '''
      It is responsible for managing all operations
      related to email address
    '''

    def is_avaible_the_email(self, email):
        '''
        Returns if the email is avaible
        '''
        session = Session()
        response = session.query(
            User
        ).filter_by(email=email).first()
        session.close()
        return (
            response == None
        )
