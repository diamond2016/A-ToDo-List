from typing import Optional
from urllib import response
from flask import Blueprint, render_template, redirect, request, url_for, flash
from models import db, User, ToDoList, ToDoListItem
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired, Optional
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


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

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

     # Find user by username entered.
        result = db.session.execute(db.select(User).where(User.username == username))
        user: User = result.scalar()
        if not user:
            flash(f'User with username {username} does not exists in database, please retry')
            return redirect(url_for('auth.login'))
        
        if check_password_hash(user.password, password):
            login_user(user)
        else:
            flash('Sorry, password incorrect, please retry')
        return redirect(url_for('main.index'))
        
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = str(form.password.data)
        hash_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        user: User = User(
            username = username,
            password = hash_password
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.index'))

    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for('main.index'))


@login_required
@auth_bp.route('/my_todolist')
def my_todolist():
    """Page showing list of todolist of the current user"""
    todo_lists = current_user.todo_lists
    return render_template('auth/my_todolist.html', todo_lists=todo_lists)

@login_required
@auth_bp.route('/add_todolist', methods=['GET', 'POST'])
def add_todolist():
# TODO adjust logic!! itemlist is a list of items toi be attacjhed to the todolist
    """User can add a new todo list in db"""
    form = ToDoListForm()
    if request.method == 'POST':
   
        new_todolist = ToDoList(
            list_name = form.name.data,
            user_id = current_user.id
        )
        new_item = ToDoListItem(
            title = form.item_title.data,
            content = form.item_content.data,
            due_time = form.item_due_time.data,
            todo_list=new_todolist
        )
        db.session.add(new_todolist)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('auth/todolist.html', form=form)

