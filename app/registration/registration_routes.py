#
# Blueprint: Registration
#
# >> Make sure to import bp as the correct blueprint <<
#
from app.registration import bp

import re

from flask import request, url_for, current_app;
from marshmallow import ValidationError
from app import db
from app.schemas import UserRegistrationSchema, UserSchema

#
# Register a new user
#
@bp.route('/registerUser', methods=['POST'])
def create_user():
    try:
        userinfo = request.get_json()

        # Verify Username
        user = UserRegistrationSchema().load(userinfo)
        user.id = None

        # Encrypt password
        user.set_password(request.json.get('password'))

        # Create user
        db.session.add(user)
        db.session.commit()
        return (UserSchema().dump(user), 201,
                {'Location': url_for('user.get_user', username=user.username, _external=True)})
    except ValidationError as err:
        current_app.logger.info(err.messages)
        return err.messages, 500

