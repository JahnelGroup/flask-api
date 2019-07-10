from flask import jsonify, abort, request, g, url_for
from app import auth, db
from app.user import bp
from app.models import User, UserSchema
import app.user.user_service as user_service

#
# Create a user
#
@bp.route('/registerUser', methods=['POST'])
def register_user():
    user = user_service.register(UserSchema().load(request.get_json()).data, request.json.get('password'))
    return (UserSchema().dump(user).data, 201,
            {'Location': url_for('user.get_user', username=user.username, _external=True)})


#
# Get current logged in user
#
@bp.route('/users/me')
@auth.login_required
def get_me():
    user = User.query.filter_by(username=g.user.username).first()
    if not user:
        abort(404)
    return jsonify(UserSchema().dump(user).data)


#
# Get a user by username
#
@bp.route('/users/<string:username>')
@auth.login_required
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    return jsonify(UserSchema().dump(user).data)


#
# Get all users
#
@bp.route('/users')
@auth.login_required
def get_users():
    users = User.query.all()
    if not users:
        abort(404)
    return jsonify(UserSchema().dump(users, many=True).data)


#
# Remove user
#
@bp.route('/users/me', methods=['DELETE'])
@auth.login_required
def remove_user():
    user_service.delete_by_username(g.user.username)
    return '', 200
