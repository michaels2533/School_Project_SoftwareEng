from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, DateField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo
from flask_login import current_user

from wtforms import widgets

from app.Model.models import User

class PostForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired()]) #where the user types in the title
    description = TextAreaField('Brief description of the Project Goals and Objectives', validators = [DataRequired()]) #where the user types in the body
    start = DateField('Start at',validators=[DataRequired()], format = "%m/%d/%Y")
    end = DateField('End at', validators = [DataRequired()], format = "%m/%d/%Y")
    requiredTime = SelectField('Time Required', choices = [('5 Hours'), ('10 Hours'), ('15 Hours'), ('20 Hours'), ('25 Hours'), ('30 Hours'), ('35 Hours'), ('40 Hours')])
    qualifications = TextAreaField('Qualifications Needed', validators = [DataRequired()])
    researchFields = StringField('Fields of Research')
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

    def validate_email(self, email):
        users = User.query.filter_by(email = email.data).all()
        for user in users:
            if (user.id != current_user.id):
                raise ValidationError('The emial is already associated with another account! Please use a different email address.')
