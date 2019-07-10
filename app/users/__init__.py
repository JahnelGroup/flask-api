from flask import Blueprint

bp = Blueprint('users', __name__)

from app.users import users_routes
