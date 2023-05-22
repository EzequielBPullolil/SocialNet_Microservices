class AlreadyRegisteredEmail(Exception):
    pass


class RequestExceptions(Exception):
    pass


class MissingParameter(RequestExceptions):
    message = 'Bad request, Missing at least one parameter'


class InvalidParameter(RequestExceptions):
    message = 'Bad request, At least one parameter is invalid'


class InvalidEschema(RequestExceptions):
    def __init__(self, invalid_params, missing_params, *args: object) -> None:
        super().__init__(*args)
        self.invalid_params = invalid_params
        self.missing_params = missing_params


class BadLoginCredentials(RequestExceptions):
    pass
