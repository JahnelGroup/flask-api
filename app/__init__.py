from flask import Flask
from flask_httpauth import HTTPBasicAuth
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
from flask.logging import default_handler
import app.filters as filters_util
import logging


db = SQLAlchemy()
migrate = Migrate()
auth = HTTPBasicAuth()
ma = Marshmallow()
filters = filters_util


def create_app(config_class=Config):
    application = Flask(__name__)
    application.config.from_object(config_class)

    db.init_app(application)
    ma.init_app(application)
    migrate.init_app(application, db)

    from app.error import bp as error_bp
    application.register_blueprint(error_bp)

    from app.authentication import bp as authentication_bp
    application.register_blueprint(authentication_bp, url_prefix="/api")

    from app.registration import bp as registration_bp
    application.register_blueprint(registration_bp, url_prefix="/api")

    from app.user import bp as user_bp
    application.register_blueprint(user_bp, url_prefix="/api")

    CORS(application, resources={r"/*": {"origins": "*"}})

    application.logger.setLevel('INFO') # Configurable log level

    # Remove default logger
    application.logger.removeHandler(default_handler)

    # Doing this duplicates the log stream, but allows for custom logs
    lh = logging.StreamHandler()
    lh.setFormatter(logging.Formatter("level \"%(levelname)s\", %(message)s"))
    application.logger.addHandler(lh)

    return application


from app import models, schemas
