from flask import Blueprint
from app import auth

bp = Blueprint('user', __name__)


# Require authentication for this entire blueprint
@bp.before_request
@auth.login_required
def restrict_bp_to_admins():
    pass


from app.user import user_service, user_routes
