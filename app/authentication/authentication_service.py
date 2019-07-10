from flask import g, current_app
from app import auth
from app.models import User
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


#
# Generates a new authentication token.
#
# This function is called from the /auth/token route.
#
def generate_auth_token(expiration=600):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': g.user.id})


#
# Verify basic authentication.
#
# This function is called automatically by Flask to verify basic authentication. The credentials will either
# the user's actual credentials or a generated token.
#
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


#
# Verify authentication token.
#
# This function will verify that a generated token is valid.
#
def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None    # valid token, but expired
    except BadSignature:
        return None    # invalid token
    user = User.query.get(data['id'])
    return user
