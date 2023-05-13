from flask import Blueprint, request
from .helpers import validate_user_fields
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
        validate_user_fields(user=request.get_json())
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
    except:
        return '', 400
