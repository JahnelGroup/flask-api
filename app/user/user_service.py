from app import db
from flask import current_app
from app.models import User, Post, Activity


#
# Get user by username
#
def get_by_username(username):
    return User.query.filter_by(username=username).first()


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
    user = get_by_username(username)
    db.session.delete(user)
    db.session.commit()
    return True


#
# Add a post to user
#
def add_post(user, message):
    post = Post(user_id=user.id, message=message)
    db.session.add(post)
    db.session.flush()
    activity = Activity(verb='create', object=post)
    db.session.add(activity)
    db.session.commit()
    return post


#
# Remove post
#
def delete_post(user, post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.flush()
    activity = Activity(verb='delete', object=post)
    db.session.add(activity)
    db.session.commit()
    return True
