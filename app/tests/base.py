from flask import current_app
from flask_testing import TestCase

from app.main.db import get_db


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        return current_app

    def setUp(self):
        db = get_db()
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db = get_db()
        db.session.remove()
        db.drop_all()
