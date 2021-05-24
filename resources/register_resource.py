from common import BaseResource
from common.exception import HttpException
from flask_restful import reqparse

from models.user import User

success = {"code": "0", "message": "OK"}

base_parser = reqparse.RequestParser()
base_parser.add_argument('username', type=str)
base_parser.add_argument('email', type=str, required=True)
base_parser.add_argument('password', type=str, required=True)

class RegisterResource(BaseResource):
    def __init__(self) -> None:
        super().__init__()
        self.register_parser = base_parser.copy()
        self.register_parser.add_argument('firstname', type=str)
        self.register_parser.add_argument('lastname', type=str)

    def post(self):
        args = self.register_parser.parse_args()
        user = User.query.filter_by(email=args.email).first()
        if user:
            raise HttpException(code='003', message='User already defined', http_status=401)

        user = User(email=args['email'], password=args['password'],
                    username=args['username'], firstname=args['firstname'], lastname=args['lastname'])
        user.save()
        response = {"status": "200", 'user_id': user.user_id}
        response.update(success)
        return response
