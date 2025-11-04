from flask import Blueprint, redirect, render_template, request, url_for
from datetime import datetime
from models import ToDoList

main_bp = Blueprint('main', __name__)
 
# Main routes
@main_bp.route('/')
def index():
    """Home page showing to-do lists start page """
    return render_template('index.html')


