from flask import jsonify, abort, request, g, url_for
from marshmallow import ValidationError

from app import auth, api
from app.user import bp
from app.models import User
from app.schemas import UserSchema, UserRegistrationSchema, PostSchema
import app.user.user_service as user_service


#
# Get all users
#
@bp.route('/users')
@auth.login_required
@api.is_admin
def get_users():
    users = User.query.all()
    return jsonify(UserSchema().dump(users, many=True))


#
# Get current logged in user
#
@bp.route('/users/me')
@auth.login_required
def get_me():
    return get_user(g.user.username)


#
# Get a user by username
#
@bp.route('/users/<string:username>')
@auth.login_required
def get_user(username):
    if g.user.username != username and not g.user.is_admin():
        abort(401)

    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    return jsonify(UserSchema().dump(user))


#
# Create a user
#
@bp.route('/registerUser', methods=['POST'])
def create_user():
    try:
        body = UserRegistrationSchema().load(request.get_json())
        user = user_service.register(body, request.json.get('password'))
        return (UserSchema().dump(user), 201,
                {'Location': url_for('user.get_user', username=user.username, _external=True)})
    except ValidationError as err:
        return err.messages, 500








#
# Remove my account
#
@bp.route('/users/me', methods=['DELETE'])
@auth.login_required
def remove_user():
    user_service.delete_by_username(g.user.username)
    return '', 200


#
# Submit a post
#
@bp.route('/users/me/posts', methods=['POST'])
@auth.login_required
def add_post():
    try:
        message = request.json.get('message')
        if not message:
            abort(404)

        post = user_service.add_post(g.user, message)
        return PostSchema().dump(post), 201
    except ValidationError as err:
        return err.messages, 500