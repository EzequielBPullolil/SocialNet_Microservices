from src.exceptions import InvalidEschema
from src.validation_schemas import validate_user_schema
import pytest


class TestValidateUserSchema:
    '''
      Verify validation schemas 
    '''

    def test_valid_user_schema(self):
        valid_schema = {
            'name': 'Alex',  # >= 4 length
            'password': 'abdfghi8#',  # >= 8 length
            'email': 'anemail@test.com'
        }

        validate_user_schema(valid_schema)
