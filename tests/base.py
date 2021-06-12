import json

from flask import current_app
from flask_testing import TestCase

from app import create_app
from models import db
from models.password_reset import PasswordReset
from models.user import User


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        return current_app

    def setUp(self):
        create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.session.query(User).filter(User.email == "test@gmail.com").delete()
        db.session.query(PasswordReset).filter(PasswordReset.email == "test@gmail.com").delete()
        db.session.commit()

    def tearDown(self):
        self.app_context.pop()

    def dummy_register(self, email="test@gmail.com", password="test"):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    email=email,
                    password=password
                )),
                content_type='application/json'
            )
            return response

    def create_dummy_user(self, email="test@gmail.com", password="test"):
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
