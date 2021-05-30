from common.validation import RegisterRequestDTO

from common import BaseResource, success
from common.exception import UserAlreadyExistError
from models.user import User


class RegisterResource(BaseResource):
    def __init__(self) -> None:
        super().__init__()
        self.request_models['post'] = RegisterRequestDTO

    def post(self, request: RegisterRequestDTO):
        print('Request:', request)
        user = User.query.filter_by(email=request.email).first()
        if user:
            raise UserAlreadyExistError()

        user = User(email=request.email, password=request.password,
                    username=request.username, firstname=request.firstname, lastname=request.lastname)
        user.save()
        response = {'user_id': user.user_id}
        response.update(success)
        return response
