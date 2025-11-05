from typing import Optional
from urllib import response
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from models import db, User, ToDoList, ToDoListItem
from forms import LoginForm, RegistrationForm, ToDoListForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def _print_form_debug_info(form):
    """Helper to print request and form debug information for nested WTForms debugging.

    Not invoked by default. Call manually when investigating form validation issues.
    """
    print('--- form debug helper ---')
    try:
        print('request.method:', request.method)
        print('request.path:', request.path)
        print('request.form keys:', list(request.form.keys()))
    except Exception as e:
        print('request.form access error:', e)

    # CSRF presence (if using Flask-WTF)
    csrf_attr = getattr(form, 'csrf_token', None)
    try:
        print('form.csrf_token present:', bool(csrf_attr))
        if csrf_attr is not None:
            print('csrf token value (masked):', str(csrf_attr.data)[:6] + '...' if getattr(csrf_attr, 'data', None) else None)
    except Exception as e:
        print('csrf inspect error:', e)

    is_post = (request.method == 'POST')
    print('is_post:', is_post)
    try:
        validation_result = form.validate()
        print('form.validate() ->', validation_result)
        print('form.errors ->', form.errors)
    except Exception as e:
        print('form.validate() raised exception:', e)


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
            # Respect 'next' parameter if present so user returns to intended page
            next_page = request.args.get('next') or request.form.get('next') or None
            if next_page:
                return redirect(next_page)
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
        password = str(form.password.data)
        hash_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        user = User(
            username=username,
            password=hash_password
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
    """User can add a new todo list in db"""
    
    form = ToDoListForm()
    # Debug helper available: call _print_form_debug_info(form) when investigating validation issues.
    # Example (manual): _print_form_debug_info(form)

    if form.validate_on_submit():
        # Create new todolist
        new_todolist = ToDoList(
            name=form.name.data,
            user_id=current_user.id,
            lastmodified_at=datetime.utcnow()
        )
        db.session.add(new_todolist)
        db.session.flush()  # Get the ID for the todolist
        
        # Add all items to the todolist
        for item_data in form.items.data:
            if item_data['title']:  # Only add items with a title
                new_item = ToDoListItem(
                    icon_url=item_data.get('icon_url', ''),
                    title=item_data['title'],
                    content=item_data.get('content', ''),
                    due_time=item_data.get('due_time'),
                    completed=item_data.get('completed', False),
                    list_id=new_todolist.id
                )
                db.session.add(new_item)
        
        db.session.commit()
        flash('To-Do List created successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('auth/todolist.html', form=form, title='Create To-Do List', readonly=False)

@login_required
@auth_bp.route('/edit_todolist/<int:list_id>', methods=['GET', 'POST'])
def edit_todolist(list_id):
    """User can edit an existing todo list in db"""
    from datetime import datetime
    
    # Get the existing todo list
    todo_list = ToDoList.query.get_or_404(list_id)
    
    # Check if the current user owns this list
    if todo_list.user_id != current_user.id:
        flash('You do not have permission to edit this list.', 'danger')
        return redirect(url_for('main.index'))
    
    form = ToDoListForm()
    
    if form.validate_on_submit():
        # Update the todolist name and last modified time
        todo_list.name = form.name.data
        todo_list.lastmodified_at = datetime.utcnow()
        
        # Get existing items
        existing_items = {item.id: item for item in ToDoListItem.query.filter_by(list_id=list_id).all()}
        submitted_item_ids = set()
        
        # Update or create items from form
        for idx, item_data in enumerate(form.items.data):
            if item_data['title']:  # Only process items with a title
                # Try to match with existing item by index
                existing_item_list = list(existing_items.values())
                if idx < len(existing_item_list):
                    item = existing_item_list[idx]
                    submitted_item_ids.add(item.id)
                    # Update existing item
                    item.icon_url = item_data.get('icon_url', '')
                    item.title = item_data['title']
                    item.content = item_data.get('content', '')
                    item.due_time = item_data.get('due_time')
                    item.completed = item_data.get('completed', False)
                else:
                    # Create new item
                    new_item = ToDoListItem(
                        icon_url=item_data.get('icon_url', ''),
                        title=item_data['title'],
                        content=item_data.get('content', ''),
                        due_time=item_data.get('due_time'),
                        completed=item_data.get('completed', False),
                        list_id=list_id
                    )
                    db.session.add(new_item)
        
        # Delete items that were removed (only non-completed items can be deleted)
        for item_id, item in existing_items.items():
            if item_id not in submitted_item_ids:
                if not item.completed:
                    db.session.delete(item)
                else:
                    # Keep completed items even if not in submitted form
                    pass
        
        db.session.commit()
        flash('To-Do List updated successfully!', 'success')
        return redirect(url_for('main.index'))
    
    # Populate form with existing data for GET request
    if request.method == 'GET':
        form.name.data = todo_list.name
        existing_items = ToDoListItem.query.filter_by(list_id=list_id).all()
        
        # Clear and populate items
        while len(form.items) > 0:
            form.items.pop_entry()
        
        for item in existing_items:
            item_form = form.items.append_entry()
            item_form.icon_url.data = item.icon_url
            item_form.title.data = item.title
            item_form.content.data = item.content
            item_form.due_time.data = item.due_time
            item_form.completed.data = item.completed
    
    return render_template('auth/todolist.html', form=form, title='Edit To-Do List', readonly=False)

@login_required
@auth_bp.route('/delete_todolist/<int:list_id>')
def delete_todolist(list_id):
    """Delete a todo list"""
    todo_list = ToDoList.query.get_or_404(list_id)
    
    # Check if the current user owns this list
    if todo_list.user_id != current_user.id:
        flash('You do not have permission to delete this list.', 'danger')
        return redirect(url_for('main.index'))
    
    db.session.delete(todo_list)
    db.session.commit()
    flash('To-Do List deleted successfully!', 'success')
    return redirect(url_for('main.index'))
