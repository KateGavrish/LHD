from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, DateField, SelectMultipleField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CheckForm(FlaskForm):
    url = StringField('URL')
    text = TextAreaField('Text')
    submit = SubmitField('Submit')


class MistakeForm(FlaskForm):
    text = TextAreaField('Something went wrong? leave your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
