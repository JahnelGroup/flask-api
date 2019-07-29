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

        current_app.logger.info(userinfo)

        # Create error
        valerr = ValidationError({})
        foundError = False

        if "username" not in userinfo or userinfo["username"] == "":
                valerr.messages["username"] = "Username field is blank."
                foundError = True
        elif len(userinfo["username"]) < 3:
                valerr.messages["username"] = "Username is too short."
                foundError = True

        if "email" not in userinfo or userinfo["email"] == "":
                valerr.messages["email"] = "Email field is blank."
                foundError = True
        elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", userinfo["email"]):
                valerr.messages["email"] = "Invalid email address."
                foundError = True

        if "password" not in userinfo or userinfo["password"] == "":
                valerr.messages["password"] = "Password field is blank."
                foundError = True
        elif len(userinfo["password"]) < 8:
                valerr.messages["password"] = "Password is too short. Must be more than 8 characters"
                foundError = True
        elif not (re.match("\w*[A-Z]", userinfo["password"])
                        and re.match("\w*[a-z]", userinfo["password"])
                        and re.match("\w*[0-9]", userinfo["password"])):
                valerr.messages["password"] = "Password must include an uppercase character, lowercase character, and number."
                foundError = True
        elif "password2" not in userinfo or userinfo["password2"] == "":
                valerr.messages["password2"] = "Please enter the password again."
                foundError = True
        elif userinfo["password"] != userinfo["password2"]:
                valerr.messages["password2"] = "Passwords must match."
                foundError = True

        if foundError:
                raise valerr

        # Otherwise, there are no errors, so proceed with creation
        del userinfo["password2"]
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
