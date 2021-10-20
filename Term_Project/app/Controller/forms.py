from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()]) #where the user types in the title
    body = TextAreaField('Body', validators = [DataRequired()]) #where the user types in the body
    submit = SubmitField('Post') #submit button