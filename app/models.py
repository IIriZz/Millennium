# -*- coding: utf-8 -*-
# models.py

from hashlib import md5

from flask_login import UserMixin
from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), nullable=False)

    about_me = db.Column(db.String(140))

    def __repr__(self):
        return f'<users {self.id}>'

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email.encode("utf-8")).hexdigest() + '?d=mm&s=' + str(size)