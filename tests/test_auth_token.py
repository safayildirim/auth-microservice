import unittest

from base import BaseTestCase
from app.main.db import get_db
from app.main.jwt_util import encode_auth_token, decode_auth_token
from app.main.models import User


class TestAuthToken(BaseTestCase):

    def test_encode_auth_token(self):
        db = get_db()
        user = User(
            id=1,
            username='test',
            password='123456',
            role="user"
        )
        db.session.add(user)
        db.session.commit()
        auth_token = encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        db = get_db()
        user = User(
            id=1,
            username='test',
            password='123456',
            role="user"
        )
        db.session.add(user)
        db.session.commit()
        auth_token = encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(decode_auth_token(auth_token) == 1)


if __name__ == '__main__':
    unittest.main()