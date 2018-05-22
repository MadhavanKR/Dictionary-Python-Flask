from flask_wtf import FlaskForm;
from wtforms import StringField,PasswordField,BooleanField,SubmitField;
from wtforms.validators import ValidationError,DataRequired,EqualTo,Length,Email;
from flask import request;
from app.models import User;

class LoginForm(FlaskForm):
    username = StringField('username', [DataRequired()]);
    password = PasswordField('password', [DataRequired()]);
    remember_me = BooleanField('remember me');
    submit = SubmitField('Sign in');
    

class RegistrationForm(FlaskForm):
    username = StringField('username', [DataRequired()]);
    email = StringField('Email',[DataRequired(), Email()]);
    password = PasswordField('Password', [DataRequired()]);
    password2 = PasswordField('Password', [DataRequired(), EqualTo('password')]);
    submit = SubmitField('Register');
    
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first();
        print(user);
        if user is not None:
            raise ValidationError('Please use a different username');
    
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first();
        print(user);
        if user is not None:
            raise ValidationError('Please use a different email address');
