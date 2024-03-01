from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message="Username can't be blank")])
    password = PasswordField('Password', validators=[InputRequired(message="Password can't be blank")])
    email = EmailField('Email', validators=[InputRequired(message="Email can't be blank")])
    first_name = StringField('First Name', validators=[InputRequired(message="First Name can't be blank")])
    last_name = StringField('Last Name', validators=[InputRequired(message="Last Name can't be blank")])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message="Username can't be blank")])
    password = PasswordField('Password', validators=[InputRequired(message="Password can't be blank")])

class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(message="Title can't be blank")])
    content = StringField('Content', validators=[InputRequired(message="Content can't be blank")])