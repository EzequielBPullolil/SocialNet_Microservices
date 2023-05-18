
from src.exceptions import InvalidEschema
from src.middlewares.validate_fields import validate_user_fields_middleware
from src.validation_schemas import validate_user_schema
from flask import Blueprint, request
from .services.register import register_service
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
@validate_user_fields_middleware
def register():
    '''
        Persist and user before validate_fields_middleware
    '''
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
