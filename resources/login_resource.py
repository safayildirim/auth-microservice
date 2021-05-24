from flask_restful import Resource

from models.user import User
from .register_resource import base_parser
from services import jwt_util

login_parser = base_parser.copy()
login_parser.remove_argument('username')


class LoginResource(Resource):
    def post(self):
        try:
            args = login_parser.parse_args()
            user = User.query.filter_by(email=args.email).first()
            if user is None:
                response = {
                    'status': '404',
                    'message': 'User is not found.'
                }
                return response, 404
            if user.check_password(args.password):
                auth_token = jwt_util.encode_auth_token(user.id)
                if auth_token:
                    response = {
                        "status": "200",
                        'token': auth_token
                    }
                    return response, 200
            else:
                response = {
                    'status': '401',
                    'message': 'Email or password does not match.'
                }
                return response, 401

        except Exception as e:
            print(e)
            response = {
                'status': '500',
                'message': 'Try again'
            }
            return response, 500
