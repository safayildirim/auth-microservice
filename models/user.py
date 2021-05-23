from datetime import datetime

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(256))
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime)
    price = db.Column(db.Float)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
        nullable=False)
    product = db.relationship('Product', backref=db.backref('products', lazy=True))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

def insert_data():
    user = User(username="zeevac", password="123456", firstname="safa", lastname="yildirim")
    product = Product(name="macbook pro")
    order = Order(create_time=datetime.now(), price=15000, product=product)
    db.session.add(user)
    db.session.add(product)
    db.session.add(order)
    db.session.commit()

