import json
import unittest

from app import app
from models import db
from models.user import User
from tests.base import BaseTestCase


class TestAuthBlueprint(BaseTestCase):

    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    email='test@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertIsNotNone(data['user_id'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        user = User(
            email='test@gmail.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    email='test@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == '401')
            self.assertTrue(
                data['message'] == 'User already exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            resp_register = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    email='test@gmail.com',
                    password='123456'
                )),
                content_type='application/json',
            )
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == '200')
            self.assertTrue(data_register['user_id'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 200)
            # registered user login
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='test@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == '200')
            self.assertTrue(data['token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_registered_user_login_with_wrong_password(self):
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            resp_register = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    email='test@gmail.com',
                    password='123456'
                )),
                content_type='application/json',
            )
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == '200')
            self.assertTrue(data_register['user_id'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 200)
            # registered user login
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='test@gmail.com',
                    password='wrong-password'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == '401')
            self.assertTrue(data['message'] == 'Email or password does not match.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
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
            self.assertTrue(data['status'] == '404')
            self.assertTrue(data['message'] == 'User is not found.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main(app)
