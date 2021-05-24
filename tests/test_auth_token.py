import json
import unittest

from base import BaseTestCase
from models import db
from models.user import User
from services.jwt_util import encode_auth_token, verify_token


class TestAuthToken(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            email='test@gmail.com',
            password='123456',
        )
        auth_token = encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))

    def test_verify_token(self):
        db.session.query(User).filter(User.email == "test@gmail.com").delete()
        db.session.commit()
        user = User(
            email='test@gmail.com',
            password='123456'
        )
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='test@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
        data = json.loads(response.data.decode())
        auth_token = data['token']
        user_id = verify_token(auth_token)
        self.assertTrue(user_id, str)
        self.assertTrue(user_id == user.id)


if __name__ == '__main__':
    unittest.main()
