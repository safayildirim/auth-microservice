from datetime import datetime, timedelta

from . import db


class PasswordReset(db.Model):
    email = db.Column(db.String(64), index=True, unique=True, nullable=False, primary_key=True)
    token = db.Column(db.String(256))
    expire_date = db.Column(db.DateTime)

    def __init__(self, email, token) -> None:
        super().__init__()
        self.email = email
        self.token = token

    def save(self):
        self.expire_date = datetime.now() + timedelta(minutes=10)

        db.session.add(self)
        db.session.commit()

    def validate_token(self):
        if datetime.now() <= self.expire_date:
            return True
        else:
            return False
