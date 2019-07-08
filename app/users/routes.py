from flask import jsonify
from app.users import bp
from app.models import User


@bp.route('/api/users')
def index():
    return jsonify({'users': [u.serialize for u in User.query.all()]}), 200
