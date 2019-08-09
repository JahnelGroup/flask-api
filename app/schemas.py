from app import ma
from flask import current_app
from app.models import User, UserType, Post
from marshmallow import fields, validates, validates_schema, ValidationError

import re


#
# Common representation of a User
#
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        exclude = ['password', 'posts']


#
# Validates user registration input.
#
class UserRegistrationSchema(ma.ModelSchema):
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    password2 = fields.String(require=True, load_only=True)
    type = fields.String(required=True)

    @validates_schema
    def validate_registration(self, data, **kwargs):
        # Create error
        userinfo = data
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
            valerr.messages["password"] = "Password is too short. Must be 8 or more characters"
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

        if "type" not in userinfo or userinfo["type"] not in UserType.__members__:
            valerr.messages["type"] = "Invalid value."
            foundError = True

        if foundError:
            raise valerr

    class Meta:
        model = User


#
# Common representation of a Post
#
class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post
        exclude = ['versions']


class PostWithUser(ma.ModelSchema):
    username = fields.String(required=True)
    post = fields.Nested(PostSchema)
    class Meta:
        model = Post
