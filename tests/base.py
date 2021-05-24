from flask import current_app
from flask_testing import TestCase

from app import create_app
from models import db
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
        db.session.commit()

    def tearDown(self):
        self.app_context.pop()
