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

    def compare(self, password: str, hashed_password: str) -> bool:
        '''
            Compare the clean password with the encrypted one
        '''
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
