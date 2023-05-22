from src import Session
from src.exceptions import InvalidParameter
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

    def email_belongs_to_user(self, email, id):
        '''
            Verify if the email belongs to user with id
        '''
        session = Session()
        response = session.query(
            User
        ).filter_by(id=id).first()
        session.close()
        if (response.email != email):
            raise InvalidParameter
