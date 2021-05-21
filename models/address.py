from operator import add
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
db = SQLAlchemy(app)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    street = db.Column(db.String(64)) 
    country = db.Column(db.String(4))

db.create_all()
address = Address(street="atasehir", country="tr")
db.session.add(address)
db.session.commit()