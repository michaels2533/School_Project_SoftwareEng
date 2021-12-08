from datetime import datetime
from enum import unique
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import backref
from app import db
from flask_login import UserMixin
from app import login
from wtforms import DateField


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

#items from Models post and tags
createTags = db.Table('createTags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) #id of user
    #Info special to every user
    username = db.Column(db.String(64))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email =  db.Column(db.String(120), unique = True)
    password_hash = db.Column(db.String(128))
    userType = db.Column(db.String(64))
    posts = db.relationship('Post', backref='writer', lazy = 'dynamic')

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
    def get_user_posts(self):
       return self.posts
      
class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    #Application will hold the student who applied
    applied = db.relationship('Application', backref = 'whoApplied')
    #Will display students major, gpa, gradDate, and Expierence
    major = db.Column(db.String(64))
    GPA = db.Column(db.String(64))
    gradDate = db.Column(db.String(64))
    experience = db.Column(db.String(64))
    #Will display all the Tag's the Student has available to them
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

    def isApplied(self, newJob):
        print(Application.query.filter_by(post_id=newJob.id).all())
        print(Application.query.filter_by(student_id = self.id).all())
        return (Application.query.filter_by(post_id=newJob.id).filter_by(student_id = self.id).count())

    def withdraw(self, post):
        if self.isApplied(post):
            status =  Application.query.filter_by(student_id=self.id).filter_by(post_id=post.id).first()
            db.session.delete(status)
            db.session.commit()

    __mapper_args__ = {
        'polymorphic_identity':'student'
    }



class Faculty(User):
    __tablename__ = 'Faculty'
    id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    officehours = db.Column(db.String(64))
    __mapper_args__ = {
        'polymorphic_identity':'Faculty'
    }


class ElectiveTag(db.Model):
    __tablename__ = 'electivetag'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    def __repr__(self):
        return '{}'.format(self.name)

class ProgramLanguageTag(db.Model):
    __tablename__ = 'programlanguagetag'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return '{}'.format(self.name)

class ResearchTopicTag(db.Model):
    __tablename__ = 'researchtopictag'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return '{}'.format(self.name)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True) #holds tag id's
    name = db.Column(db.String(20)) 

    def __repr__(self):
        return '{}'.format(self.name) #prints out id - name on post


class Post(db.Model):
    #Bellow is data we don't display
    id = db.Column(db.Integer, primary_key=True) #holds post id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(150)) #holds username
    
    #Application will hold the post that it was applied for
    applicants = db.relationship('Application', backref = 'jobPost')
    
    #Bellow is data that will be displayed
    title = db.Column(db.String(150)) #holds post title
    description = db.Column(db.String(1500)) #holds post body
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) #records timestamp of when post was made
    startDate = db.Column(db.String(20)) # will hold start date for job
    endDate = db.Column(db.String(20)) # will hold end date for job
    requiredTime = db.Column(db.Text) # will hold required amount of time 
    qualifications = db.Column(db.String(1500)) #will hold qualifications needed for the job
    researchFields = db.relationship('Tag', secondary =  createTags, primaryjoin = (createTags.c.post_id == id), backref=db.backref('createTags', lazy='dynamic'), lazy = 'dynamic')
    
    #will hold faculty first name / last name
    facultyFirst = db.Column(db.String(26))
    facultyLast = db.Column(db.String(26))
    facultyEmail = db.Column(db.String(26))
    facultyUsername = db.Column(db.String(26))

    def get_tags(self):
        return self.researchFields
    
   



class Application(db.Model):
    #Holds the id for a post that it was applied for
    id = db.Column(db.Integer, primary_key=True)
    #Bellow application will hold the id of the post it was applied for, as well as the id for the student who applied
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'))
    
    #will hold the username of the faculty memeber
    username = db.Column(db.String(26))
    
    #Holds reference's first name, last name, email, and a description for why they want the job
    firstName = db.Column(db.String(26))
    lastName = db.Column(db.String(26))
    email = db.Column(db.String(120))
    body = db.Column(db.String(1500))
    appStatus = db.Column(db.String(20))
    approved = db.Column(db.Boolean,default = False)
    def __repr__(self):
        return '{} - {} - {}'.format(self.id, self.post_id, self.student_id)


