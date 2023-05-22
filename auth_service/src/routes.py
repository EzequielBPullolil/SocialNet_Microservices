from src.services.login import LoginService
from src.middlewares.validate_fields import validate_user_fields_middleware
from flask import Blueprint, request
from .services.register import register_service
from src.exceptions import BadLoginCredentials
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


@auth_bp.route('/login', methods=['POST'])
def login():
    '''
        Validates login credentials and 
        response with token cookie
    '''
    try:
        login_service = LoginService()
        login_service.login(request.get_json())
        return {
        }, 201
    except BadLoginCredentials:
        return {}, 400
