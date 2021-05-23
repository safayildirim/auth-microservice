from flask import request
from flask_restful import Resource

from models.user import User
from services import jwt_util


class LoginResource(Resource):
    def post(self):
        try:
            user = User.query.filter_by(email=request.json.get('email')).first()
            if user is None:
                response = {
                    'status': '401',
                    'message': 'User is not found.'
                }
                return response, 401
            if user.check_password(request.json.get('password')):
                auth_token = jwt_util.encode_auth_token(user.id)
                if auth_token:
                    response = {
                        "status": "200",
                        'token': auth_token.decode('UTF-8')
                    }
                    return response, 200
            else:
                response = {
                    'status': '401',
                    'message': 'Email or password does not match.'
                }
                return response, 401

        except Exception as e:
            print(e)
            response = {
                'status': '500',
                'message': 'Try again'
            }
            return response, 500
