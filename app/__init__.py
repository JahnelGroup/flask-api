from flask import Flask
from flask_httpauth import HTTPBasicAuth
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()
auth = HTTPBasicAuth()


def create_app(config_class=Config):
    application = Flask(__name__)
    application.config.from_object(config_class)

    db.init_app(application)
    migrate.init_app(application, db)

    from app.authentication import bp as authentication_bp
    application.register_blueprint(authentication_bp, url_prefix="/api")

    from app.users import bp as users_bp
    application.register_blueprint(users_bp, url_prefix="/api")

    return application


from app import models
