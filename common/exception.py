class HttpException(Exception):

    def __init__(self, code: str, message: str, http_status: int) -> None:
        self.code = code
        self.message = message
        self.http_status = http_status

    def get_body(self) -> dict:
        return {'code': self.code, 'message': self.message}


class WrongCredentialsError(HttpException):
    def __init__(self) -> None:
        super().__init__("111", "Username or password is wrong.", 400)


class UserNotFoundError(HttpException):
    def __init__(self) -> None:
        super().__init__("112", "User is not found.", 404)


class UserAlreadyExistError(HttpException):
    def __init__(self) -> None:
        super().__init__("113", "User already exist.", 400)
