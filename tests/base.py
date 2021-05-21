from flask import app
from flask_testing import TestCase

from db import get_db


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        return app

    def setUp(self):
        db = get_db()
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db = get_db()
        db.session.remove()
        db.drop_all()
