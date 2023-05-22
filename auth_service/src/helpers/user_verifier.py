from src import Session
from src.models import User


class UserVerifier:
    '''
    Esta clase se encarga de verificar la existencia de usuarios 
    '''

    def verify_by_id(self, id):
        '''
        Verify if exist an user with the id [id]

        if not exist raises exception
        '''
        session = Session()
        user = session.query(User).filter_by(id=id).first()
        session.close()

        if (user == None):
            raise Exception
