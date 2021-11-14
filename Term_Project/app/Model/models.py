from datetime import datetime
from enum import unique
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import backref
from app import db
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

eTags = db.Table('eTags', 
                db.Column('student_id', db.Integer, db.ForeignKey('student.id')), 
                db.Column('elective_id', db.Integer, db.ForeignKey('electivetag.id')))
pTags = db.Table('pTags', 
                db.Column('student_id', db.Integer, db.ForeignKey('student.id')), 
                db.Column('programlanguage_id', db.Integer, db.ForeignKey('programlanguagetag.id')))
rTags = db.Table('rTags', 
                db.Column('student_id', db.Integer, db.ForeignKey('student.id')), 
                db.Column('researchtopic_id', db.Integer, db.ForeignKey('researchtopictag.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) #id of user
    username = db.Column(db.String(64), unique = True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email =  db.Column(db.String(120), unique = True)
    #WSU_ID = db.Column(db.String(64), unique = True)
    password_hash = db.Column(db.String(128))
    userType = db.Column(db.String(64))
    posts = db.relationship('Post', backref='writer')

    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':userType
    }

    def __repr__(self):
        return '<User {} - {} - {} - {};'.format(self.id, self.username, self.email, self.userType)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def get_password(self, password):
        return check_password_hash(self.password_hash, password)
   # def get_user_posts(self):
      #  return self.posts


class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    major = db.Column(db.String(64))
    GPA = db.Column(db.String(64))
    gradDate = db.Column(db.String(64))
    #researchTopics = db.Column(db.String(64))
    #programLanguages = db.Column(db.String(64))
    experience = db.Column(db.String(64))
    #electives = db.Column(db.String(64))

    elective_tag = db.relationship("ElectiveTag", secondary = eTags, primaryjoin=(eTags.c.student_id == id), 
                                                  backref=db.backref('estudent', lazy='dynamic'), lazy='dynamic')
    programlangauge_tag = db.relationship("ProgramLanguageTag", secondary = pTags, primaryjoin=(pTags.c.student_id == id), 
                                                  backref=db.backref('pstudent', lazy='dynamic'), lazy='dynamic')
    researchtopic_tag = db.relationship("ResearchTopicTag", secondary = rTags, primaryjoin=(rTags.c.student_id == id), 
                                                  backref=db.backref('rstudent', lazy='dynamic'), lazy='dynamic')

    def get_electiveTags(self):
        return self.elective_tag
    def get_programlanguageTags(self):
        return self.programlangauge_tag
    def get_researchtopicTags(self):
        return self.researchtopic_tag

    __mapper_args__ = {
        'polymorphic_identity':'student'
    }



class Faculty(User):
    __tablename__ = 'faculty'
    id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    officeHours = db.Column(db.String(64))
    __mapper_args__ = {
        'polymorphic_identity':'faculty'
    }


class ElectiveTag(db.Model):
    __tablename__ = 'electivetag'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    
    def __repr__(self):
        return 'ID - {} Name - {}'.format(self.id, self.name)

class ProgramLanguageTag(db.Model):
    __tablename__ = 'programlanguagetag'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return 'ID - {} Name - {}'.format(self.id, self.name)

class ResearchTopicTag(db.Model):
    __tablename__ = 'researchtopictag'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return 'ID - {} Name - {}'.format(self.id, self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) #holds post id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(150)) #holds post title
    body = db.Column(db.String(1500)) #holds post body
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) #records timestamp of when post was made
    username = db.Column(db.String(150)) #holds username
    applicants = db.relationship('Application', backref = 'jobPost')


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(26))
    lastName = db.Column(db.String(26))
    email = db.Column(db.String(120))
    phoneNum = db.Column(db.String(20))
    body = db.Column(db.String(1500))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))


