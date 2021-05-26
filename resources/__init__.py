from common.api import BaseApi

from resources.login_resource import LoginResource
from resources.register_resource import RegisterResource


def init_resources(app):
    auth_api = BaseApi(app, prefix="/auth")

    auth_api.add_resource(RegisterResource, '/register')
    auth_api.add_resource(LoginResource, '/login')
