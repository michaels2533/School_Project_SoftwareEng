from datetime import datetime
from enum import unique
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import backref
from app import db
from flask_login import UserMixin
from app import login

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #id of user
    username = db.Column(db.String(64), unique = True)
    email =  db.Column(db.String(120), unique = True)
    password_hash = db.Column(db.String(128))
    #posts = db.relationship('Post', backref='writer', lazy='dynamic')

    def __repr__(self):
        return '<User {} - {} - {};'.format(self.id, self.username, self.email)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def get_password(self, password):
        return check_password_hash(self.password_hash, password)
   # def get_user_posts(self):
      #  return self.posts
