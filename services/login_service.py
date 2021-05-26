from flask.wrappers import Response

from common.exception import WrongCredentialsError
from models.user import User
from services import make_response


class LoginService:

    def login(self, request: dict) -> Response:
        username = request.get('username')
        password = request.get('password')

        user = User.query.filter_by(username=username).first()

        if user is None:
            raise WrongCredentialsError()

        if not user.check_password(password):
            raise WrongCredentialsError()

        token = user.get_token()

        return make_response(body={"token": token})
