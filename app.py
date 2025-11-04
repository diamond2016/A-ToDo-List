from flask import Flask, app
import os
from config import Config
from models import User, db
from flask_login import LoginManager
from init_data import init_sample_data

login_manager = LoginManager()

def create_app():
    global login_manager
    app = Flask(__name__)
    # not create db, we use the one provided
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = 'lavispateresa25$'
    
    # Initialize extensions
    db.init_app(app)
    # Configure Flask-Login
    login_manager.init_app(app)
    
    # Register blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()       
        # Initialize sample data if needed
        try:
            init_sample_data()
        except Exception as e:
            print(f"Sample data initialization: {e}")
    
    app.run(debug=True)
