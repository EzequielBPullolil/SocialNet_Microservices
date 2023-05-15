from flask import Blueprint, request
from src.exceptions import RequestExceptions
from .helpers import UserFieldsValidator
from .services.register import register_service
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    '''
        persist user if the json data is valid,
        else response status 400

        Args:
            - name (str): user name
                * len >= 4
            - password (str): user password
                * len > 9
            - email (str): user email
                * contains '@'
    '''
    user_fields_validator = UserFieldsValidator(user_fields=request.get_json())
    try:
        user_fields_validator.validate_fields()
        user_id = register_service(user_data=request.get_json())
        return {
            'status': 'success',
            'message': 'User successfully registered',
            'data': {
                'id': user_id,
                'name': request.get_json()['name'],
                'email': request.get_json()['email']
            }
        }, 201
    except RequestExceptions as excep_inf:
        return {
            'status': 'error',
            'message': excep_inf.message,
            'invalid_parameters': user_fields_validator.get_invalid_parameters(),
            'missing_parameters': user_fields_validator.get_missing_parameters()
        }, 400
