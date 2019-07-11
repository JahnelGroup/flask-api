from sqlalchemy.orm import relationship

from app import db

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import Timestamp
import enum


#
# Enum: User Type
#
class UserType(enum.Enum):
    admin = "admin"
    user = "user"


#
# Model: Base
#
class BaseModel(db.Model, Timestamp):
    __abstract__ = True


#
# Model: User
#
class User(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    type = db.Column(db.String(128))
    posts = relationship("Post")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute.')

    # @password.setter
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def is_admin(self):
        return self.type == UserType.admin.value


#
# Model: Post
#
class Post(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.username)