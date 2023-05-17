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

    def test_invalid_name_raise_error(self):
        '''
            Verify if parse an schema with short nname raise
            exception and the error message is the expected
        '''
        shcema_with_invalid_name = {
            'name': 'Ale',
            'password': 'abdfghi#',  # >= 8 length
            'email': 'an_email@test.com'
        }
        with pytest.raises(InvalidEschema) as e_info:
            validate_user_schema(shcema_with_invalid_name)

        name_message = e_info.value.invalid_params['name']
        assert 'The name field must have at least 4 characters' in name_message['message']

    def test_invalid_email_raise_error(self):
        '''
            Verify if parse an schema with invalid email raise InvalidEschema
            and if the message is the expected for invalid email
        '''
        schema_with_invalid_email = {
            'name': 'Aled',  # >= 4 length
            'password': 'abdfghi8#',  # >= 8 length
            'email': 'anemail.com'
        }

        with pytest.raises(InvalidEschema) as e_info:
            validate_user_schema(schema_with_invalid_email)

        assert e_info.value.invalid_params['email']['message'] == 'Invalid email format'
