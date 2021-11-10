from datetime import datetime
from enum import unique
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import backref
from app import db
from flask_login import UserMixin
from app import login
from wtforms import DateField


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #id of user
    username = db.Column(db.String(64), unique = True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email =  db.Column(db.String(120), unique = True)
    password_hash = db.Column(db.String(128))
    userType = db.Column(db.Text)
    posts = db.relationship('Post', backref='writer')

    def __repr__(self):
        return '<User {} - {} - {} - {};'.format(self.id, self.username, self.email, self.userType)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def get_password(self, password):
        return check_password_hash(self.password_hash, password)
   # def get_user_posts(self):
      #  return self.posts


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#items from Models post and tags
createTags = db.Table('createTags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

class Post(db.Model):
    #Bellow is data we don't display
    id = db.Column(db.Integer, primary_key=True) #holds post id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(150)) #holds username
    #Bellow is data that will be displayed
    title = db.Column(db.String(150)) #holds post title
    description = db.Column(db.String(1500)) #holds post body
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) #records timestamp of when post was made
    startDate = db.Column(db.String(20)) # will hold start date for job
    endDate = db.Column(db.String(20)) # will hold end date for job
    requiredTime = db.Column(db.Text) # will hold required amount of time 
    qualifications = db.Column(db.String(1500)) #will hold qualifications needed for the job
    researchFields = db.relationship('Tag', secondary =  createTags, primaryjoin = (createTags.c.post_id == id), backref=db.backref('createTags', lazy='dynamic'), lazy = 'dynamic')
    applicants = db.relationship('Application', backref = 'jobPost')

    def get_tags(self):
        return self.tags
    
   
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True) #holds tag id's
    name = db.Column(db.String(20)) # 
    def __repr__(self):
        return '{} - {}'.format(self.id, self.name) #prints out id - name on post


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(26))
    lastName = db.Column(db.String(26))
    email = db.Column(db.String(120))
    phoneNum = db.Column(db.String(20))
    body = db.Column(db.String(1500))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))