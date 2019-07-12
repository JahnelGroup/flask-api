#
# Blueprint: Error
#
# >> Make sure to import bp as the correct blueprint <<
#
from app.error import bp
from app import db


@bp.app_errorhandler(404)
def not_found_error(error):
    return 'Not found.', 404


@bp.app_errorhandler(401)
def not_found_error(error):
    return 'Unauthorized', 401


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return '', 500
