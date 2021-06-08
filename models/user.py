import uuid
from datetime import datetime

import bcrypt

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), index=True)
    username = db.Column(db.String(32))
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(256))
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    create_time = db.Column(db.DateTime)
    last_modified_time = db.Column(db.DateTime)

    def __init__(self, email, password, username=None, firstname=None, lastname=None) -> None:
        super().__init__()

        uid = uuid.uuid4()
        self.user_id = uid.hex

        self.email = email
        self.username = username
        self.password = self._hash_password(password)
        self.firstname = firstname
        self.lastname = lastname

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def _hash_password(self, password: str):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def change_password(self, new_password):
        self.password = self._hash_password(new_password)
        db.session.commit()

    def save(self):
        self.create_time = datetime.now()
        self.last_modified_time = datetime.now()

        db.session.add(self)
        db.session.commit()

# class Order(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     create_time = db.Column(db.DateTime)
#     price = db.Column(db.Float)
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
#                            nullable=False)
#     product = db.relationship(
#         'Product', backref=db.backref('products', lazy=True))


# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64))

# def insert_data():
#     user = User(username="zeevac", password="123456",
#                 firstname="safa", lastname="yildirim")
#     product = Product(name="macbook pro")
#     order = Order(create_time=datetime.now(), price=15000, product=product)
#     db.session.add(user)
#     db.session.add(product)
#     db.session.add(order)
#     db.session.commit()
