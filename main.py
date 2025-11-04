from flask import Blueprint, redirect, render_template, request, url_for, flash, session
from datetime import datetime
from models import ToDoList, db
from forms import ToDoListForm
from flask_login import current_user

main_bp = Blueprint('main', __name__)
 
# Main routes
@main_bp.route('/')
def index():
    """Home page showing to-do lists start page """
    todos = []
    if current_user.is_authenticated:
        todos = ToDoList.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', todos=todos)

@main_bp.route('/new_todo', methods=['GET', 'POST'])
def new_todo():
    """Create a new to-do list and its items """
    form = ToDoListForm()
    
    if request.method == 'POST':
        # Check if user is authenticated before saving
        if not current_user.is_authenticated:
            # Store form data in session
            session['pending_todolist'] = {
                'name': request.form.get('name'),
                'items': []
            }
            # Collect all items from form
            for key in request.form:
                if key.startswith('items-'):
                    session['pending_todolist']['items'].append({
                        'key': key,
                        'value': request.form.get(key)
                    })
            flash('Please log in to save your to-do list.', 'warning')
            return redirect(url_for('auth.login', next=url_for('auth.add_todolist')))
        
        # If authenticated, redirect to add_todolist to handle saving
        return redirect(url_for('auth.add_todolist'))
    
    return render_template('auth/todolist.html', form=form, title='Create New To-Do List', readonly=False)


