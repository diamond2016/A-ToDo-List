# Basic Models
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class ToDoList(db.Model):
    """Model for to-do lists"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    lastmodified_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<ToDoList {self.name}>'

class ToDoListItem(db.Model):
    """Model for to-do list items"""
    id = db.Column(db.Integer, primary_key=True)
    icon_url = db.Column(db.String(250), nullable=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.String(500), nullable=True)
    completed = db.Column(db.Boolean, default=True)
    due_time = db.Column(db.DateTime, nullable=True)
    list_id = db.Column(db.Integer, db.ForeignKey('to_do_list.id'), nullable=False)

    def __repr__(self):
        return f'<ToDoListItem {self.content}>'

class User(UserMixin, db.Model):
    """Model for user accounts"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    lastmodified_at = db.Column(db.DateTime, default=datetime.utcnow)
    lists = db.relationship('ToDoList', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
    