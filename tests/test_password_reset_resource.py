from resources.password_reset_resource import create_and_save_pr_object, redis_db, generate_reset_link
from tests.base import BaseTestCase


class TestPasswordResetResource(BaseTestCase):

    def test_generate_reset_link(self):
        email = 'test@gmail.com'
        generated_email = generate_reset_link(email)
        self.assertIsNotNone(generated_email)
        self.assertRegex(generated_email, '^localhost:8080/reset-password/')

    def test_create_and_save_pr_object(self):
        email = 'test@gmail.com'
        token = '122343423423'
        create_and_save_pr_object(email, token)
        response_email = redis_db.get(token)
        self.assertIsNotNone(response_email)
        self.assertEqual(email, response_email.decode('utf-8'))
