from flask import jsonify, abort, request, g, url_for
from app import auth, db
from app.user import bp
from app.models import User, UserSchema
import app.user.user_service as users_service

user_schema = UserSchema()
users_schema = UserSchema(many=True)

#
# Create a user
#
@bp.route('/registerUser', methods=['POST'])
def register_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    if username is None or password is None or email is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return (user_schema.dump(user).data, 201,
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
    return jsonify(user_schema.dump(user).data)


#
# Get a user by username
#
@bp.route('/users/<string:username>')
@auth.login_required
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    return jsonify(user_schema.dump(user).data)


#
# Get all users
#
@bp.route('/users')
@auth.login_required
def get_users():
    users = User.query.all()
    if not users:
        abort(404)
    return jsonify(users_schema.dump(users).data)


#
# Remove user
#
@bp.route('/users/me', methods=['DELETE'])
@auth.login_required
def remove_user():
    user = User.query.filter_by(username=g.user.username).first()
    if user is None:
        abort(404)  # missing arguments

    db.session.delete(user)
    db.session.commit()
    return '', 200
