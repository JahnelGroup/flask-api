#
# Blueprint: User
#
# >> Make sure to import bp as the correct blueprint <<
#
from app.user import bp

from flask import jsonify, abort, request, g
from marshmallow import ValidationError
from app import filters
from app.models import User, Post
from app.schemas import UserSchema, PostSchema
import app.user.user_service as user_service


#
# Get all users
#
@bp.route('/users')
@filters.is_admin
def get_users():
    users = User.query.all()
    return UserSchema().jsonify(users, many=True)


#
# Get current logged in user
#
@bp.route('/users/me')
def get_me():
    return get_user(g.user.username)


#
# Get a user by username
#
@bp.route('/users/<string:username>')
def get_user(username):
    if g.user.username != username and not g.user.is_admin():
        abort(401)

    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    return UserSchema().jsonify(user)


#
# Remove my account
#
@bp.route('/users/me', methods=['DELETE'])
def remove_user():
    user_service.delete_by_username(g.user.username)
    return '', 200


#
# Submit a post
#
@bp.route('/users/me/posts', methods=['POST'])
def add_post():
    try:
        message = request.json.get('message')
        if not message:
            abort(404)

        post = user_service.add_post(g.user, message)
        return PostSchema().dump(post), 201
    except ValidationError as err:
        return err.messages, 500


#
# Get all my posts
#
@bp.route('/users/me/posts')
def get_posts():
    return PostSchema().jsonify(Post.query.filter_by(user_id=g.user.id), many=True)


#
# Get a post
#
@bp.route('/users/me/posts/<int:post_id>')
def get_post(post_id):
    return Post.query.get_or_404(post_id)
