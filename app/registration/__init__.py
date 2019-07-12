from flask import Blueprint

bp = Blueprint('registration', __name__)

from app.registration import registration_routes
