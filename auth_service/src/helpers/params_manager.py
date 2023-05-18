
def missing_params_message(error) -> dict:
    '''
        Describes all the required params was
        missing
    '''
    missing_params = []
    if ('name' in error.message):
        missing_params.append('name')

    if ('password' in error.message):
        missing_params.append('password')

    if ('email' in error.message):
        missing_params.append('email')
    return missing_params


def invalid_params_message(errors) -> dict:
    '''
        Describes an dict of all the invalid params
        and they detailed errors
    '''
    message = {}
    for error in errors:
        if ('name' in error.path):
            message['name'] = invalid_name_message(error)
        if ('password' in error.path):
            message['password'] = invalid_password_message(error)
        if ('email' in error.path):
            message['email'] = invalid_email_message(error)

    return message


def invalid_email_message(email) -> dict:
    '''
            Describes custom message for invalid password
    '''
    email_message = {}
    if ('pattern' in str(email.validator)):
        email_message['message'] = 'Invalid email format'

    return email_message


def invalid_password_message(password) -> dict:
    '''
        Describes custom message for invalid password
    '''
    password_message = {}
    if ('anyOf' in str(password.validator)):
        password_message['message'] = 'The password field must have at least 1 symbol or at least 1 number'
    if ('minLength' in str(password.validator)):
        password_message['message'] = 'The password field must have at least 8 characters'
    return password_message


def invalid_name_message(name) -> dict:
    '''
        Describes custom message for invalid name
    '''
    name_message = {}

    if ('minLength' in str(name.validator)):
        name_message['message'] = 'The name field must have at least 4 characters'
    if ('required' in str(name.validator)):
        name_message['message'] = 'The name field must have at least 4 characters'

    return name_message
