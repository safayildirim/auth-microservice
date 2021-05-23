import flask_restful


from flask_restful import Api
from .auth import RegisterResource, LoginResource


def init_resources(app):
    auth_api = Api(app, prefix="/auth")

    auth_api.add_resource(LoginResource, '/login')
    auth_api.add_resource(RegisterResource, '/register')
