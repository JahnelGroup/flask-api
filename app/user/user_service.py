from app import db
from app.models import User, Post


#
# Save a user
#
def save(user):
    db.session.add(user)
    db.session.commit()
    return user


#
# Delete a user by username
#
def delete_by_username(username):
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    return True


#
# Add a post to user
#
def add_post(user, message):
    post = Post(user_id=user.id, message=message)
    db.session.add(post)
    db.session.commit()
    return post
