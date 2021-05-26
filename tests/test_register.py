import json

from tests.base import BaseTestCase


class TestRegister(BaseTestCase):
    def test_registration(self):
        """ Test for user registration """
        response = self.dummy_register()
        data = json.loads(response.data.decode())
        self.assertIsNotNone(data['user_id'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_register_with_already_registered_user(self):
        """ Test registration with already registered email"""

        self.create_dummy_user()
        response = self.dummy_register()
        data = json.loads(response.data.decode())
        self.assertTrue(data['code'] == '113')
        self.assertTrue(
            data['message'] == 'User already exist.')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_register_with_illegal_request(self):
        """ Test registration with illegal request information"""
        self.create_dummy_user()
        response = self.dummy_register(email="")
        data = json.loads(response.data.decode())
        self.assertEqual(data['code'], '005')
        self.assertEqual(data['message'], 'Email field is mandatory.')
        self.assertEqual(response.status_code, 400)
