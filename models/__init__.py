from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_db(app):
    db.init_app(app)
    db.create_all()
