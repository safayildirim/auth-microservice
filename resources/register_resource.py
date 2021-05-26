from flask_restful import reqparse

from common import BaseResource, success
from common.exception import UserAlreadyExistError
from common.validation import RegisterRequestDTO
from models.user import User

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

    @request(RegisterRequestDTO)
    def post(self, request):
        args = self.register_parser.parse_args()
        user = User.query.filter_by(email=args.email).first()
        if user:
            raise UserAlreadyExistError()

        user = User(email=args['email'], password=args['password'],
                    username=args['username'], firstname=args['firstname'], lastname=args['lastname'])
        user.save()
        response = {'user_id': user.user_id}
        response.update(success)
        return response
