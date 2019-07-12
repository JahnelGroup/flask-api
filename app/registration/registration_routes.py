#
# Blueprint: Registration
#
# >> Make sure to import bp as the correct blueprint <<
#
from app.registration import bp

from flask import request, url_for
from marshmallow import ValidationError
from app import db
from app.schemas import UserRegistrationSchema, UserSchema

#
# Register a new user
#
@bp.route('/registerUser', methods=['POST'])
def create_user():
    try:
        user = UserRegistrationSchema().load(request.get_json())
        user.id = None
        user.set_password(request.json.get('password'))
        db.session.add(user)
        db.session.commit()
        return (UserSchema().dump(user), 201,
                {'Location': url_for('user.get_user', username=user.username, _external=True)})
    except ValidationError as err:
        return err.messages, 500
