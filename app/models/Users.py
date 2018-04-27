from flask_login import UserMixin, AnonymousUserMixin
from app import db

import uuid

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(40), unique=False, nullable=False)
    user_id = db.Column(db.String(36), unique=True, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.user_id = str(uuid.uuid4())

    @staticmethod
    def from_username(username):
        print('called from_username')
        return User.query.filter_by(username=username).first()

    @staticmethod
    def from_id(user_id):
        print('called from_id')
        return User.query.filter_by(user_id=user_id).first()

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id


class AnonUser(AnonymousUserMixin):

    def __init__(self):
        self.username = 'anon'
        self.id = str(uuid.uuid4())

    def get_id(self):
        return self.id

    @staticmethod
    def create():
        return AnonUser()