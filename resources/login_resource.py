from common import BaseResource, success
from common.exception import WrongCredentialsError, UserNotFoundError
from models.user import User
from services import jwt_util
from resources.register_resource import base_parser

login_parser = base_parser.copy()
login_parser.remove_argument('username')


class LoginResource(BaseResource):
    def post(self):
        args = login_parser.parse_args()
        user = User.query.filter_by(email=args.email).first()
        if user is None:
            raise UserNotFoundError()
        if user.check_password(args.password):
            auth_token = jwt_util.encode_auth_token(user.id)
            if auth_token:
                response = {
                    'token': auth_token
                }
                return response.update(success)
        else:
            raise WrongCredentialsError()
