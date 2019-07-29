from flask import g, current_app, request, jsonify
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
    current_app.logger.info(request)
    # first try to authenticate by token
    [user, message] = verify_auth_token(username_or_token)
    verified_by_token = True
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        verified_by_token = False
        if not user or not user.verify_password(password):
            if(user):
                current_app.logger.error("message: \"login failed\", reason: \"incorrect password\", username: \"{}\", ip: \"{}\"".format(user.username, request.remote_addr))
                return False
            else:
                current_app.logger.error("message: \"login failed\", reason: \"incorrect username/{}\", ip: \"{}\"".format(message, request.remote_addr))
            return False
    g.user = user
    # If session times out, this prints the token
    if not verified_by_token:
        current_app.logger.info("message: \"login successful\", username: \"{}\", ip: \"{}\"".format(user.username, request.remote_addr))
    else:
        current_app.logger.info("message: \"logged in with token\", ip: \"{}\"".format(request.remote_addr))
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
        message = "expired token"
        return [None, message]  # valid token, but expired
    except BadSignature:
        message = "invalid token"
        return [None, message] # invalid token
    user = User.query.get(data['id'])
    return [user, ""]
