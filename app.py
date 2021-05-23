from resources import init_resources
from flask.app import Flask
from flask_bcrypt import Bcrypt
from models import create_db
from models.user import insert_data

app = Flask(__name__)
app.app_context().push()
flask_bcrypt = Bcrypt()


def create_app() -> Flask:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
    flask_bcrypt.init_app(app)
    create_db(app)
    insert_data()
    init_resources(app)
    return app