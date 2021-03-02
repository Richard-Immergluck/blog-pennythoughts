from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, InputRequired
from pennythoughts.models import User

# Some of the code in this file was taken from the CMT120 Flask Practical Exercises and corresponding .pfd documentation.
# The documents are available (with access privileges) at:
# https://learningcentral.cf.ac.uk/webapps/blackboard/content/listContent.jsp?course_id=_399846_1&content_id=_5432888_1&mode=reset

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=40)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=40)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Regexp('^(?=.*\d).{8,20}$', message='Your password should be between 8 and 20 characters and contain at least one number.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', 'Your passwords do not match')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Your username already exists, please choose a different one.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                'Your email already exists, please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid Email Address/Password')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError('Invalid Email Address/Password')


class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[InputRequired()])
    submit = SubmitField('Post comment')


class ContactForm(FlaskForm):
    name = TextField("Name", validators=[DataRequired("Please enter your name")])
    email = TextField("Email", validators=[DataRequired(), Email("Please include your Email Address")])
    subject = TextField("Subject", validators=[DataRequired("Please include a Subject")])
    message = TextAreaField("Message", validators=[DataRequired("Please enter a message")])
    submit = SubmitField("Send")
