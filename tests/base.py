from flask import current_app
from flask_testing import TestCase

from app import create_app


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        return current_app

    def setUp(self):
        create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
