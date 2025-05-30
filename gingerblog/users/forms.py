from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_login import current_user
from gingerblog.models import User
import re

def password_complexity_check(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not re.search(r"[A-Z]", password):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r"[a-z]", password):
        raise ValidationError('Password must contain at least one lowercase letter.')
    if not re.search(r"\d", password):
        raise ValidationError('Password must contain at least one digit.')
    if not re.search(r"[@$!%*?&#]", password):
        raise ValidationError('Password must contain at least one special character (@, $, !, %, *, ?, &, or #).')



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min = 4, max = 20)])
    email = StringField('Email', validators=[DataRequired(),Email() ])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=8, max=16, message="Password must be between 8 and 16 characters"),
        password_complexity_check])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit_form = SubmitField('Sign Up')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different username.')
        
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email adress already exists. Please choose a different email.')




class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit_form = SubmitField('Login')



class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min = 4, max = 20)])
    email = StringField('Email', validators=[DataRequired(),Email() ])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg', 'png'])])
    submit_form = SubmitField('Update')

    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken. Please choose a different username.')
        
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email adress already exists. Please choose a different email.')
            

        
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()
            if user is None:
                raise ValidationError('There is no account with that Email. You must register first')



class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=8, max=16, message="Password must be between 8 and 16 characters"),
        password_complexity_check])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Reset Password')