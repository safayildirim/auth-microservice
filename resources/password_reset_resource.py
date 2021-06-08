import json
import uuid
from importlib.resources import Resource

from flask_restful import reqparse
from kafka import KafkaProducer

from common.exception import UserNotFoundError, InvalidTokenError
from models.password_reset import PasswordReset
from models.user import User

parser = reqparse.RequestParser()


class PasswordResetResource(Resource):
    def post(self):
        args = parser.parse_args()
        user = User.query.filter_by(email=args.email).first()
        if user is not None:
            generated_link = self.generate_reset_link(args.email)
            self.send_email_info_to_kafka(args.email, generated_link)

    def put(self):
        args = parser.parse_args()
        new_password = args.password
        password_reset_object = PasswordReset.query.filter_by(token=args.token).first()
        if password_reset_object is None or not password_reset_object.validate_token():
            raise InvalidTokenError()
        user = User.query.filter_by(email=password_reset_object.email).first()
        if user is None:
            raise UserNotFoundError()
        user.change_password(new_password)

    def send_email_info_to_kafka(self, email, link):
        message = {'from': 'our_email@gmail.com', 'to': email, 'subject': link}
        producer = KafkaProducer(bootstrap_servers=['localhost:8080'],
                                 value_serializer=lambda m: json.dumps(m).encode('utf-8'))
        producer.send('send-email', message)
        producer.close()

    def generate_reset_link(self, email):
        token = uuid.uuid4()
        generated_link = "localhost:8080/reset-password/{}".format(token)
        self.create_and_save_pr_object(email, token)
        return generated_link

    def create_and_save_pr_object(self, email, token):
        pr_object = PasswordReset(email=email, token=token)
        pr_object.save()
