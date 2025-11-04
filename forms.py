from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class ToDoListForm(FlaskForm):
    name = StringField('To-Do List Name', validators=[DataRequired(), Length(min=2, max=100)])

    item_title = StringField('Item Title', validators=[DataRequired(), Length(min=2, max=100)])
    item_content = StringField('Item Content', validators=[DataRequired(), Length(min=2, max=500)])
    item_due_time = StringField('Item Due Time', validators=[Optional()])
    submit = SubmitField('Create')  
