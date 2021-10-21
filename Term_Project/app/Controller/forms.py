from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

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