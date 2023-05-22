class RsaManager:

    def get_public_key(self):
        '''
          Return the public RSA key
        '''
        file = open('public_key.pem', 'rb')
        return file.read()

    def get_private_key(self):
        '''
          Return the private RSA key
        '''
        file = open('private_key.pem', 'rb')
        return file.read()
