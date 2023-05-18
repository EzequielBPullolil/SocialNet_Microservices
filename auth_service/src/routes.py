
from src.exceptions import InvalidEschema
from src.validation_schemas import validate_user_schema
from flask import Blueprint, request
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
    try:
        validate_user_schema(request.get_json())
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
    except InvalidEschema as excep_inf:
        return {
            'status': 'error',
            'message': 'Invalid json schema',
            'invalid_params': excep_inf.invalid_params,
            'missing_params': excep_inf.missing_params

        }, 400
