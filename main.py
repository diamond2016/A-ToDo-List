from flask import Blueprint, redirect, render_template, request, url_for
from datetime import datetime
from models import ToDoList
from forms import ToDoListForm

main_bp = Blueprint('main', __name__)
 
# Main routes
@main_bp.route('/')
def index():
    """Home page showing to-do lists start page """
    return render_template('index.html')

@main_bp.route('/new_todo', methods=['GET', 'POST'])
def new_todo():
    """Create a new to-do list and its items """
    form = ToDoListForm()
    if request.method == 'POST':
        title = request.form.get('title')
        if title:
            todo = ToDoList(title=title, created_at=datetime.now())
            todo.save()
            return redirect(url_for('main.index'))
    return render_template('auth/todolist.html', form=form)


