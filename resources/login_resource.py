from flask_restful import Resource

from common import errors
from models.user import User
from services import jwt_util
from .register_resource import base_parser

login_parser = base_parser.copy()
login_parser.remove_argument('username')


class LoginResource(Resource):
    def post(self):
        try:
            args = login_parser.parse_args()
            user = User.query.filter_by(email=args.email).first()
            if user is None:
                return errors['UserNotFoundError']
            if user.check_password(args.password):
                auth_token = jwt_util.encode_auth_token(user.id)
                if auth_token:
                    response = {
                        'status': '200',
                        'token': auth_token
                    }
                    return response
            else:
                return errors['WrongCredentialError']
        except Exception as e:
            print(e)
            response = {
                'status': '500',
                'message': 'Try again'
            }
            return response, 500
