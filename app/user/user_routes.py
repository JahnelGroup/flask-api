from flask import jsonify, abort, request, g, url_for
from marshmallow import ValidationError

from app import auth
from app.user import bp
from app.models import User
from app.schemas import UserSchema, UserRegistrationSchema
import app.user.user_service as user_service

#
# Create a user
#
@bp.route('/registerUser', methods=['POST'])
def register_user():
    try:
        body = UserRegistrationSchema().load(request.get_json())
        user = user_service.register(body, request.json.get('password'))
        return (UserSchema().dump(user), 201,
                {'Location': url_for('user.get_user', username=user.username, _external=True)})
    except ValidationError as err:
        return err.messages, 500


#
# Get current logged in user
#
@bp.route('/users/me')
@auth.login_required
def get_me():
    user = User.query.filter_by(username=g.user.username).first()
    if not user:
        abort(404)
    return jsonify(UserSchema().dump(user))


#
# Get a user by username
#
@bp.route('/users/<string:username>')
@auth.login_required
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    return jsonify(UserSchema().dump(user))


#
# Get all users
#
@bp.route('/users')
@auth.login_required
def get_users():
    users = User.query.all()
    if not users:
        abort(404)
    return jsonify(UserSchema().dump(users, many=True))


#
# Remove my account
#
@bp.route('/users/me', methods=['DELETE'])
@auth.login_required
def remove_user():
    user_service.delete_by_username(g.user.username)
    return '', 200
