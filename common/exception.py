
class HttpException(Exception):

    def __init__(self, code: str, message: str, http_status: int) -> None:
        self.code = code
        self.message = message
        self.http_status = http_status
        super().__init__(self.code, self.message, self.http_status)

    def get_body(self) -> dict:
        return {'code': self.code, 'message': self.message}
