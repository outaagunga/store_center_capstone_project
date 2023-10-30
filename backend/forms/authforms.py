from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(Form):
    username = StringField('Username', [
        DataRequired(message="Username is required"),
        Length(min=4, max=25, message="Username must be between 4 to 25 characters")
    ])
    email = StringField('Email Address', [
        DataRequired(message="Email is required"),
        Email(message="Invalid email address"),
        Length(min=6, max=50, message="Email must be between 6 to 50 characters")
    ])
    password = PasswordField('Password', [
        DataRequired(message="Password is required"),
        Length(min=6, max=50, message="Password must be between 6 to 50 characters"),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    
class LoginForm(Form):
    email = StringField('Email Address', [
        DataRequired(message="Email is required"),
        Email(message="Invalid email address"),
        Length(min=6, max=50, message="Email must be between 6 to 50 characters")
    ])
    password = PasswordField('Password', [
        DataRequired(message="Password is required")
    ])
    
class ResetPasswordForm(Form):
    email = StringField('Email Address', [
        DataRequired(message="Email is required"),
        Email(message="Invalid email address"),
        Length(min=6, max=50, message="Email must be between 6 to 50 characters")
    ])
    password = PasswordField('New Password', [
        DataRequired(message="Password is required"),
        Length(min=6, max=50, message="Password must be between 6 to 50 characters"),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat New Password')