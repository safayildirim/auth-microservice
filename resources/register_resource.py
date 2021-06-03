from common import BaseResource, success
from common.validation import Field
from common.exception import UserAlreadyExistError
from models.user import User


class RegisterRequestDTO:
    email = Field.String(not_blank=True, is_email=True)
    password = Field.String(not_blank=False, min_len=8, max_len=16)
    username = Field.String(min_len=2, max_len=25)
    firstname = Field.String()
    lastname = Field.String()

    def __str__(self) -> str:
        return "{\n\temail: %s, \n\tusername: %s, \n\tpassword: %s, \n\tfirstname: %s\n\tlastname: %s\n}" % (self.email, self.username, self.password, self.firstname, self.lastname)


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
