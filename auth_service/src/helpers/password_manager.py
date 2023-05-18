import bcrypt


class PasswordManager:
    salt = bcrypt.gensalt()

    def encrypt_password(self, password: str):
        '''
          Return an encrypted password
        '''
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), self.salt
        )

        return hashed_password.decode('utf-8')

    def check_password(self, password: str, hashed_password: str) -> bool:
        '''
            Return true if the password is the same
        '''
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
