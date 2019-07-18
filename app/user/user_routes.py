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
from app.user import user_service as user_service


#
# Get all users
#
@bp.route('/users')
@filters.is_admin
def get_users():
    users = User.query.all()
    return UserSchema().jsonify(users, many=True)


#
# Get user by username
#
@bp.route('/users/<string:username>')
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    return UserSchema().jsonify(user)


#
# Remove user by username
#
@bp.route('/users/<string:username>', methods=['DELETE'])
def remove_user(username):
    if g.user.username != username and not g.user.is_admin():
        abort(401)

    user_service.delete_by_username(username)
    return '', 200


#
# Submit a post for me
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
# Get posts by username
#
@bp.route('/users/<string:username>/posts')
def get_user_posts(username):
    user = user_service.get_by_username(username)
    return PostSchema().jsonify(Post.query.filter_by(user_id=user.id), many=True)


#
# Get post by id
#
@bp.route('/users/<string:username>/posts/<int:post_id>')
def get_post(username, post_id):
    return PostSchema().jsonify(Post.query.get_or_404(post_id))


#
# Remove post by id
#
@bp.route('/users/<string:username>/posts/<int:post_id>', methods=['DELETE'])
def remove_post(username, post_id):
    if g.user.username != username and not g.user.is_admin():
        abort(401)

    user = user_service.get_by_username(username)
    post = Post.query.get_or_404(post_id)
    if post.user_id != user.id:
        abort(401)

    user_service.delete_post(user, post_id)
    return '', 200
