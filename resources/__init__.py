import flask_restful


from flask_restful import Api
from .register_resource import RegisterResource


def init_resources(app):
    auth_api = Api(app, prefix="/auth")

    auth_api.add_resource(RegisterResource, '/register')
