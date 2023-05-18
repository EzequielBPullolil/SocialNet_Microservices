from flask import request
from src.exceptions import InvalidEschema
from src.validation_schemas import validate_user_schema


def validate_user_fields_middleware(func):
    '''
      Validates the fields
      are defined and valid,
      if the fields are invalid return InvalidSchema 
      json response

    '''
    def wrapper(*args, **kwargs):
        try:
            validate_user_schema(request.get_json())

            return func(*args, **kwargs)

        except InvalidEschema as excep_inf:
            return {
                'status': 'error',
                'message': 'Invalid json schema',
                'invalid_params': excep_inf.invalid_params,
                'missing_params': excep_inf.missing_params
            }, 400

    return wrapper
