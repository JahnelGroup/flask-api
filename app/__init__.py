from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)

from app import routes, models
