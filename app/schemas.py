from app import ma
from app.models import User, UserType, Post
from marshmallow import fields, validates, ValidationError


#
# Common representation of a User
#
class UserSchema(ma.ModelSchema):
    posts = fields.Nested('PostSchema', many=True)

    class Meta:
        model = User
        exclude = ['password']


#
# Validates user registration input.
#
class UserRegistrationSchema(ma.ModelSchema):
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    type = fields.String(required=True)

    @validates("type")
    def validate_quantity(self, value):
        if value not in UserType.__members__:
            raise ValidationError("Invalid value.")

    class Meta:
        model = User


#
# Common representation of a Post
#
class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post
