from flask import jsonify, request, abort, url_for, g
from app import db
from app.users import bp
from app.models import User


@bp.route('/api/users')
def get_users():
    return jsonify({'users': [user.serialize for user in User.query.all()]})


@bp.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(404)
    return jsonify(user.serialize)


@bp.route('/api/users', methods=['POST'])
def create_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    if username is None or password is None or email is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify(user.serialize), 201,
            {'Location': url_for('users.get_users', id=user.id, _external=True)})
