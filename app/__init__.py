from flask import Flask
from flask_httpauth import HTTPBasicAuth
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
auth = HTTPBasicAuth()
ma = Marshmallow()


def create_app(config_class=Config):
    application = Flask(__name__)
    application.config.from_object(config_class)

    db.init_app(application)
    ma.init_app(application)
    migrate.init_app(application, db)

    from app.authentication import bp as authentication_bp
    application.register_blueprint(authentication_bp, url_prefix="/api")

    from app.user import bp as user_bp
    application.register_blueprint(user_bp, url_prefix="/api")

    CORS(application, resources={r"/*": {"origins": "http://localhost:4200"}})

    return application


from app import models, schemas
