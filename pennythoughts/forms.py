from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, InputRequired
from pennythoughts.models import User

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired(), Length(min=2,max=40)])
    last_name = StringField('First Name', validators = [DataRequired(), Length(min=2,max=40)])
    username = StringField('Username', validators = [DataRequired(), Length(min=2,max=40)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password',validators = [DataRequired(), Regexp('^(?=.*\d).{8,20}$', message='Your password should be between 6 and 20 characters and contain at least one number.')])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')                                                                                                      

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Your username already exists, please choose a different one.')

    def validate_email(self, email):
        email = User.query.filter_by(email = email.data).first()
        if email:
            raise ValidationError('Your email already exists, please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[InputRequired()])
    submit = SubmitField('Post comment')

