# Basic Models
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from typing import TYPE_CHECKING

db = SQLAlchemy()

class ToDoList(db.Model):
    """Model for to-do lists"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    lastmodified_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_do_list_item = db.relationship('ToDoListItem', backref='todolist', lazy=True, cascade='all, delete-orphan')
    # Typing-only constructor to satisfy static type checkers (Pylance/pyright).
    # This is ignored at runtime.
    if TYPE_CHECKING:
        def __init__(self, name: str, user_id: int, lastmodified_at: datetime | None = None, *args, **kwargs) -> None: ...

    def __repr__(self):
        return f'<ToDoList {self.name}>'

class ToDoListItem(db.Model):
    """Model for to-do list items"""
    id = db.Column(db.Integer, primary_key=True)
    icon_url = db.Column(db.String(250), nullable=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.String(500), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    due_time = db.Column(db.DateTime, nullable=True)
    list_id = db.Column(db.Integer, db.ForeignKey('to_do_list.id'), nullable=False)
    # Typing-only constructor to satisfy static type checkers (Pylance/pyright).
    # This is ignored at runtime.
    if TYPE_CHECKING:
        def __init__(self, title: str, list_id: int, icon_url: str | None = None, content: str | None = None, due_time: datetime | None = None, completed: bool = False, *args, **kwargs) -> None: ...

    def __repr__(self):
        return f'<ToDoListItem {self.title}>'

class User(UserMixin, db.Model):
    """Model for user accounts"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    lastmodified_at = db.Column(db.DateTime, default=datetime.utcnow)
    lists = db.relationship('ToDoList', backref='user', lazy=True)

    # Provide a typing-only __init__ signature so static type checkers (Pylance/pyright)
    # understand the constructor parameters. This block is ignored at runtime.
    if TYPE_CHECKING:
        def __init__(self, username: str, password: str, *args, **kwargs) -> None: ...

    def __repr__(self):
        return f'<User {self.username}>'
    