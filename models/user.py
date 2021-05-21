from db import get_db

db = get_db()


class User:
    def __init__(self, id, username, password, role="user"):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
