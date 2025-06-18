from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Configuration
    # Load default configuration
    app.config.from_mapping(
        SECRET_KEY='dev', # Should be overridden in production
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'inventory.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass # Already exists

    # Initialize Flask extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # The route for the login page

    # Import and register blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .main import main_bp # ADD THIS LINE
    app.register_blueprint(main_bp) # ADD THIS LINE, registers at root '/' for dashboard

    # Import models here to ensure they are known to SQLAlchemy
    # before app context is needed for db.create_all()
    from . import models

    with app.app_context():
        db.create_all() # Create database tables if they don't exist

    # @app.route('/')
    # def index():
    #     return "Hello, World! This is the IT Inventory System."

    return app
