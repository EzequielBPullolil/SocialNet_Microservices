from flask import Blueprint, request
from .services.login import LoginService
from .services.register import RegisterService

from src.exceptions import BadLoginCredentials
from src.middlewares.validate_fields import validate_user_fields_middleware
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
@validate_user_fields_middleware
def register():
    '''
        Persist and user before validate_fields_middleware
    '''
    register_service = RegisterService()
    user_data = register_service.register(request.get_json())
    return {
        'status': 'success',
        'message': 'User successfully registered',
        'data': user_data
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
            'status': 'success',
            'message': 'Successful login',
            'token': ''
        }, 201
    except BadLoginCredentials:
        return {}, 400
