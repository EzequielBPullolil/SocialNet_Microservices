import jsonschema

from src.exceptions import InvalidEschema
from src.helpers import invalid_params_message, missing_params_message


user_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 4
        },
        "password": {
            "type": "string",
            "minLength": 8,
            "anyOf": [
                {"pattern": ".*[0-9].*"},
                {"pattern": ".*[!@#$%^&*()_\\-+=~`\\[\\]{}|\\\\:;\"'<>,.?/].*"}
            ]
        },
        "email": {
            "title": "Email address",
            "type": "string",
            "pattern": "^\\S+@\\S+\\.\\S+$",
            "format": "email",
            "minLength": 6,
            "maxLength": 127
        }
    },
    "required": ["name", "email", "password"],
}

validator = jsonschema.Draft7Validator(user_schema)


def validate_user_schema(instance):
    '''
        Validates user schema usig jsonchema validate
        if the schema is invalid raises exception with 
        custom error messages
        raises InvalidSchema
    '''

    try:
        validator.validate(instance)
    except jsonschema.exceptions.ValidationError as e_info:
        errors = list(validator.iter_errors(instance))
        invalid_params = invalid_params_message(errors)
        missing_params = missing_params_message(e_info)
        raise InvalidEschema(invalid_params, missing_params)
