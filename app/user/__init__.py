from flask import Blueprint, request, g
from app import auth

bp = Blueprint('user', __name__)


# Require authentication for this entire blueprint
@bp.before_request
@auth.login_required
def restrict_bp_to_admins():
    pass


# Translate 'me' to username
@bp.before_request
def translate_me_to_username():
    if 'username' in request.view_args:
        username = request.view_args['username']
        if username == 'me':
            request.view_args['username'] = g.user.username


from app.user import user_service, user_routes
