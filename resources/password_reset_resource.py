import json
import uuid
from datetime import timedelta

import redis
from flask_restful import reqparse
from kafka import KafkaProducer

from common import BaseResource, success
from common.exception import UserNotFoundError, InvalidTokenError
from models.user import User

parser = reqparse.RequestParser()
parser.add_argument('email')
redis_db = redis.Redis()


class PasswordResetResource(BaseResource):
    def post(self):
        args = parser.parse_args()
        user = User.query.filter_by(email=args.email).first()
        if user is not None:
            generated_link = self.generate_reset_link(args.email)
            self.send_email_info_to_kafka(args.email, generated_link)
            return success
        raise TypeError()

    def put(self):
        args = parser.parse_args()
        new_password = args.password
        password_reset_token = redis_db.exists(args.token)
        if password_reset_token is None:
            raise InvalidTokenError()
        user = User.query.filter_by(email=redis_db.get(password_reset_token).decode('utf-8')).first()
        if user is None:
            raise UserNotFoundError()
        user.change_password(new_password)


def send_email_info_to_kafka(email, link):
    message = {'from': 'our_email@gmail.com', 'to': email, 'subject': link}
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda m: json.dumps(m).encode('utf-8'))
    producer.send('send-email', message)
    producer.close()


def generate_reset_link(email):
    token = str(uuid.uuid4())
    generated_link = "localhost:8080/reset-password/{}".format(token)
    create_and_save_pr_object(email, token)
    return generated_link


def create_and_save_pr_object(email, token):
    redis_db.setex(token, timedelta(minutes=10), email)
