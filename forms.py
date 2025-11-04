from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FieldList, FormField, DateTimeLocalField
from wtforms.validators import Length, DataRequired, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class ToDoListItemForm(FlaskForm):
    """Form for individual todo list items"""
    icon_url = StringField('Icon URL', validators=[Optional(), Length(max=250)])
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=250)])
    content = StringField('Content', validators=[Optional(), Length(max=500)])
    due_time = DateTimeLocalField('Due Time', validators=[Optional()], format='%Y-%m-%dT%H:%M')
    completed = BooleanField('Completed', default=False)

class ToDoListForm(FlaskForm):
    """Form for todo list with multiple items"""
    name = StringField('To-Do List Name', validators=[DataRequired(), Length(min=2, max=250)])
    items = FieldList(FormField(ToDoListItemForm), min_entries=1)
    submit = SubmitField('Save To-Do List')  
