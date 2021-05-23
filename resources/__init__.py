from flask_restful import Api

from .login_resource import LoginResource
from .register_resource import RegisterResource


def init_resources(app):
    auth_api = Api(app, prefix="/auth")

    auth_api.add_resource(RegisterResource, '/register')
    auth_api.add_resource(LoginResource, '/login')
