from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo
from flask_login import current_user
from wtforms.widgets.core import CheckboxInput, ListWidget
from app.Model.models import Faculty, ProgramLanguageTag, ResearchTopicTag, User, ElectiveTag
from wtforms_sqlalchemy.fields import QuerySelectMultipleField

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
    title = StringField('Title', validators=[DataRequired()]) #where the user types in the title
    body = TextAreaField('Body', validators = [DataRequired()]) #where the user types in the body
    submit = SubmitField('Post') #submit button

class ApplicationForm(FlaskForm):
    firstName = StringField('First', validators=[DataRequired()])
    lastName = StringField('Last', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    phoneNum = StringField('Phone', validators = [DataRequired()])
    body = TextAreaField('Resume', validators = [DataRequired()])
    submit = SubmitField('Submit Application')

class EditForm(FlaskForm):
    firstname = StringField('First Name',validators=[DataRequired()])
    lastname = StringField('Last Name',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

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
    pass
    
    def validate_email(self, email):
        users = User.query.filter_by(email = email.data).all()
        for user in users:
            if (user.id != current_user.id):
                raise ValidationError('The emial is already associated with another account! Please use a different email address.')
