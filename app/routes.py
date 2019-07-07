from flask import jsonify
from app import application
from app.models import User


@application.route('/api/users')
def index():
    return jsonify({'users': [u.to_json() for u in User.query.all()]}), 200
