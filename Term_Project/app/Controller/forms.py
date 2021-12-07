from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, DateField
from wtforms.fields.core import BooleanField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo
from flask_login import current_user
from wtforms_sqlalchemy.fields import  QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.widgets.core import CheckboxInput, ListWidget
from app.Model.models import Faculty, ProgramLanguageTag, ResearchTopicTag, User, ElectiveTag, Application
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms import widgets

from app.Model.models import User, Tag

#write the query_factory and get_label functions here 
def queryFactory():
    return Tag.query.all()
def getLabel(tagName):
    return tagName.name

def queryFactoryElectiveTag():
    return ElectiveTag.query.all()
def getLabelElective(tagname):
    return tagname.name

def queryFactoryProgramLanguageTag():
    return ProgramLanguageTag.query.all()
def getLabelProgramLanguage(tagname):
    return tagname.name

def queryFactoryResearchTopicTag():
    return ResearchTopicTag.query.all()
def getLabelResearchTopic(tagname):
    return tagname.name

class PostForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired()]) #where the user types in the title
    description = TextAreaField('Brief description of the Project Goals and Objectives', validators = [DataRequired()]) #where the user types in the body
    start = DateField('Start at',validators=[DataRequired()], format = "%m/%d/%Y")
    end = DateField('End at', validators = [DataRequired()], format = "%m/%d/%Y")
    requiredTime = SelectField('Time Required', choices = [('5 Hours'), ('10 Hours'), ('15 Hours'), ('20 Hours'), ('25 Hours'), ('30 Hours'), ('35 Hours'), ('40 Hours')])
    qualifications = TextAreaField('Qualifications Needed', validators = [DataRequired()])
    researchFields = QuerySelectMultipleField( 'Research Fields', query_factory = queryFactory , get_label = getLabel , widget = ListWidget(prefix_label=False), option_widget=CheckboxInput() ) 
    # facultyFirst = StringField('Faculty First Name', validators=[DataRequired()])
    # facultyLast = StringField('Faculty Last Name', validators=[DataRequired()])
    submit = SubmitField('Post') #submit button

class ApplicationForm(FlaskForm):
    firstName = StringField('Reference First Name',validators=[DataRequired()])
    lastName = StringField('Reference Last Name',validators=[DataRequired()])
    email = StringField('Reference Email',validators=[DataRequired(), Email()])
    body = TextAreaField('Why are You Interested?', validators = [DataRequired()])
    submit = SubmitField('Submit Application')

class EditForm(FlaskForm):
    firstname = StringField('First Name',validators=[DataRequired()])
    lastname = StringField('Last Name',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        users = User.query.filter_by(email = email.data).all()
        for user in users:
            if (user.id != current_user.id):
                raise ValidationError('The emial is already associated with another account! Please use a different email address.')

class TagForm(FlaskForm):
    newField = StringField('New Research Field')
    submit = SubmitField('Add Tag')
    
class StudentEditForm(EditForm):
    major = StringField('Major', validators=[DataRequired()])
    GPA = StringField('GPA', validators=[DataRequired()])
    gradDate = StringField('Graduation Date', validators=[DataRequired()])
    #electives = StringField('Technical Electives', validators=[DataRequired()])
    electives = QuerySelectMultipleField('Technical Electives', query_factory = queryFactoryElectiveTag, get_label = getLabelElective, widget =  ListWidget(prefix_label=False), option_widget =  CheckboxInput())
    researchTopics = QuerySelectMultipleField('Research Topics', query_factory = queryFactoryResearchTopicTag, get_label = getLabelResearchTopic, widget =  ListWidget(prefix_label=False), option_widget =  CheckboxInput())
    programLanguages = QuerySelectMultipleField('Programming Languages', query_factory = queryFactoryProgramLanguageTag, get_label = getLabelProgramLanguage, widget =  ListWidget(prefix_label=False), option_widget =  CheckboxInput())
    experience = StringField('Prior Research Experience', validators=[DataRequired()])

class FacultyEditForm(EditForm):
    officehours = StringField('Office Hours', validators=[DataRequired()])

class RecommendedSearchForm(FlaskForm):
    boolField = BooleanField("Recommended Positions")
    refresh = SubmitField("Refresh")
class SortForm(FlaskForm):
    choice = BooleanField("Your Applicants")
    refresh = SubmitField('Refresh')
class ApplicationStatusForm(FlaskForm):
    mychoices = ['Hired', 'Not Hired']
    statusfield = SelectField('Status', choices = mychoices, validators = [DataRequired()])
    submit = SubmitField('Update')
