class AlreadyRegisteredEmail(Exception):
    pass


class RequestExceptions(Exception):
    pass


class MissingParameter(RequestExceptions):
    message = 'Bad request, Missing at least one parameter'


class InvalidParameter(RequestExceptions):
    message = 'Bad request, At least one parameter is invalid'
