from app import ma
from app.models import User
from marshmallow import fields


#
# Validates inbound user registrations.
#
class UserRegistrationSchema(ma.ModelSchema):
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    type = fields.String(required=True)

    class Meta:
        model = User


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        exclude = ['password']
