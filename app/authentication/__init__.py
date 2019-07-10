from flask import Blueprint

bp = Blueprint('authentication', __name__)

from app.authentication import authentication_service, authentication_routes
