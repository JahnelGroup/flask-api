from flask import jsonify, abort, request, g, url_for
from app import auth, db
from app.users import bp
from app.models import User


#
# Get current logged in user
#
@bp.route('/users/me')
@auth.login_required
def get_me():
    user = User.query.filter_by(username=g.user.username).first()
    if not user:
        abort(404)
    return jsonify(user.serialize)


#
# Get a user by username
#
@bp.route('/users/<string:username>')
@auth.login_required
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    return jsonify(user.serialize)


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
    return (jsonify(user.serialize), 201,
            {'Location': url_for('users.get_user', username=user.username, _external=True)})
