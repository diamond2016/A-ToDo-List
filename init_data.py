from datetime import datetime, timedelta
from models import db, ToDoList, ToDoListItem, User
from werkzeug.security import generate_password_hash

def init_sample_data():
    """Initialize database with sample data"""

    # Create some users
    user_data = [
        {'username': 'user1',  'password': 'user123'}
    ]
    todo_data = [
        {'user_id': 1, 'name': 'Personal'},
        {'user_id': 1, 'name': 'Work'},
        {'user_id': 2, 'name': 'Shopping'},
        {'user_id': 2, 'name': 'Chores'}
    ]
    todoitem_data = [
        {'title': 'Buy groceries', 'content': 'Milk, Bread, Eggs', 'due_time': datetime.utcnow() + timedelta(days=1)},
        {'title': 'Read a book', 'content': 'The Great Gatsby', 'due_time': datetime.utcnow() + timedelta(days=7)}
    ]

    for user in user_data:
        existing_user = User.query.filter_by(username=user['username']).first()
        if not existing_user:
            user['password'] = generate_password_hash(user['password'], method="pbkdf2:sha256", salt_length=8)
            new_user = User(**user)
            db.session.add(new_user)
    db.session.commit()

    # add some user todos for user1 and user2 2 todos per user selected from table todo
    user1 = User.query.filter_by(username='user1').first()
    for todo in todo_data:
        existing_todo = ToDoList.query.filter_by(name=todo['name'], user_id=todo['user_id']).first()
        if not existing_todo:
            new_todo = ToDoList(name=todo['name'], user_id=todo['user_id'], lastmodified_at=datetime.utcnow())
            db.session.add(new_todo)
    db.session.commit()
    # add some todo items to the todos
    for item in todoitem_data:      
        new_item = ToDoListItem(
            icon='📝',
            title=item['title'],
            content=item['content'],
            completed=False,
            due_time=item['due_time'],
            list_id=1  # associate with first todo list for simplicity
        )
        db.session.add(new_item)
    db.session.commit()
    
    print("Sample data initialized successfully!")

def reset_database():
    """Reset the database - USE WITH CAUTION!"""
    db.drop_all()
    db.create_all()
    print("Database reset completed!")

if __name__ == '__main__':
    from app import app
    with app.app_context():
        init_sample_data()