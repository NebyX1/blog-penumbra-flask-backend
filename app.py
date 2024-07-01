from flask import Flask
from database.db import db
from database.config import DATABASE_CONNECTION_URI
from routes import endpoints
from flask_migrate import Migrate


app = Flask(__name__)


app.secret_key = "secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


migrate = Migrate(app, db)


# Aquí se registran las rutas
endpoints.init_app(app)
